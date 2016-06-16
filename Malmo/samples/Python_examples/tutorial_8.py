# --------------------------------------------------------------------------------------------------------------------
# Copyright (C) Microsoft Corporation.  All rights reserved.
# --------------------------------------------------------------------------------------------------------------------
# Tutorial sample #8: The Classroom Decorator

import MalmoPython
import os
import sys
import time

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

missionXML='''<?xml version="1.0" encoding="UTF-8" ?>
<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://ProjectMalmo.microsoft.com Mission.xsd">
  <About>
    <Summary>Find the goal!</Summary>
  </About>

  <ServerSection>
    <ServerInitialConditions>
      <Time>
        <StartTime>14000</StartTime>
        <AllowPassageOfTime>false</AllowPassageOfTime>
      </Time>
    </ServerInitialConditions>
    <ServerHandlers>
      <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" />
      <ClassroomDecorator>
        <complexity>
          <building>0.5</building>
          <path>0.5</path>
          <division>1</division>
          <obstacle>1</obstacle>
          <hint>0</hint>
        </complexity>
      </ClassroomDecorator>
      <ServerQuitFromTimeUp timeLimitMs="30000" description="out_of_time"/>
      <ServerQuitWhenAnyAgentFinishes />
    </ServerHandlers>
  </ServerSection>

  <AgentSection mode="Survival">
    <Name>James Bond</Name>
    <AgentStart>
      <Placement x="-204" y="81" z="217"/>
    </AgentStart>
    <AgentHandlers>
      <ObservationFromFullStats />
      <ContinuousMovementCommands turnSpeedDegs="180">
        <ModifierList type="deny-list">
          <command>attack</command>
        </ModifierList>
      </ContinuousMovementCommands>
      <RewardForMissionEnd rewardForDeath="-10000">
        <Reward description="found_goal" reward="1000" />
        <Reward description="out_of_time" reward="-1000" />
      </RewardForMissionEnd>
      <RewardForTouchingBlockType>
        <Block type="gold_ore diamond_ore redstone_ore" reward="20" />
      </RewardForTouchingBlockType>
      <AgentQuitFromTouchingBlockType>
        <Block type="gold_block diamond_block redstone_block" description="found_goal" />
      </AgentQuitFromTouchingBlockType>
    </AgentHandlers>
  </AgentSection>
</Mission>'''

# Create default Malmo objects:
agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

if agent_host.receivedArgument("test"):
    num_repeats = 1
else:
    num_repeats = 10

for i in range(num_repeats):
    my_mission = MalmoPython.MissionSpec(missionXML, True)
    my_mission_record = MalmoPython.MissionRecordSpec()

    # Attempt to start a mission:
    try:
        agent_host.startMission( my_mission, my_mission_record )
    except RuntimeError as e:
        print "Error starting mission:",e
        exit(1)

    # Loop until mission starts:
    print "Waiting for the mission to start ",
    world_state = agent_host.getWorldState()
    while not world_state.is_mission_running:
        sys.stdout.write(".")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print "Error:",error.text

    print
    print "Mission running ",

    # Loop until mission ends:
    while world_state.is_mission_running:
        sys.stdout.write(".")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print "Error:",error.text

    print
    print "Mission ended"
    # Mission has ended.