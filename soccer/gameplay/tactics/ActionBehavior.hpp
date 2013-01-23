#pragma once

#include <gameplay/Behavior.hpp>

namespace Gameplay
{

class ActionBehavior : public SingleRobotBehavior
{
public:
	ActionBehavior(GameplayModule *gameplay)
		: SingleRobotBehavior(gameplay),
		  partner(0)
	{
	}

	// For synchronization between ActionBehaviors
	virtual bool isSettingUp() = 0;
	virtual bool isSetup() = 0;
	virtual bool isActing() = 0;
	virtual bool isDone() = 0;
	virtual void restart() = 0;

	Geometry2d::Point actionTarget;

	ActionBehavior *partner;
};

}
