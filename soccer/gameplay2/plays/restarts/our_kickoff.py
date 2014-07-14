import play
import behavior
import robocup
import skills.line_kick
import main
import constants
import enum


class OurKickoff(play.Play):

    KickPower = 127
    ChipPower = 100


    class State(enum.Enum):
        setup = 1
        kick = 2

    def __init__(self):
        super().__init__(continuous=True)

        for state in OurKickoff.State:
            self.add_state(state, behavior.Behavior.State.running)

        self.add_transition(behavior.Behavior.State.start,
            OurKickoff.State.setup,
            lambda: True,
            'immediately')

        self.add_transition(OurKickoff.State.setup,
            OurKickoff.State.kick,
            lambda: not main.game_state().is_setup_state(),
            "on normal start")


        # TODO: verify that these values are right - I'm fuzzy on my matrix multiplication...
        idle_positions = [
            robocup.Point(0.7, constants.Field.Length / 2.0 - 0.2),
            robocup.Point(-0.7, constants.Field.Length / 2.0 - 0.2),
            robocup.Point(0.2, 1.5),
            robocup.Point(-0.2, 1.5)
        ]
        self.centers = []
        for i, pos_i in enumerate(idle_positions):
            center_i = skills.move.Move(pos_i)
            self.add_subbehavior(center_i, 'center' + str(i), required=False, priority=4-i)
            self.centers.append(center_i)

    @classmethod
    def score(cls):
        gs = main.game_state()
        return 0 if gs.is_setup_state() and gs.is_our_kickoff() else float("inf")

    def on_enter_setup(self):
        mover = skills.move.Move(robocup.Point(0, constants.Field.Length / 2.0 - 0.15))
        self.add_subbehavior(mover, 'kicker', required=False, priority=5)

    def execute_setup(self):
        for center in self.centers:
            if center.robot is not None:
                center.robot.face(main.ball().pos)

    def on_enter_kick(self):
        self.remove_subbehavior('kicker')
        kicker = skills.line_kick.LineKick()
        kicker.target = robocup.Segment(robocup.Point(-constants.Field.Width/2.0, constants.Field.Length),
            robocup.Point(constants.Field.Width/2.0, constants.Field.Length))
        kicker.use_chipper = True
        kicker.kick_power = OurKickoff.KickPower
        kicker.chip_power = OurKickoff.ChipPower
        self.add_subbehavior(kicker, 'kicker', required=True, priority=5)

    def execute_kick(self):
        # all centers should face the ball
        for center in self.centers:
            if center.robot is not None:
                center.robot.face(main.ball().pos)