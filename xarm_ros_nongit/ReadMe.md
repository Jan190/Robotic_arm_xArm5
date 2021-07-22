# Uvod
&ensp;&ensp;	U nastavku ReadMe slijedi detaljan opis kako iz postojećeg xarm_description napraviti svoju simulaciju modela robota u Gazebu i Rvizu kako bi se mogli isprobavati različiti kontroleri. Istim postupkom moguće je napraviti simulaciju u Gazebu i kinematičli model pomoću Moveit-a za bilo koju ruku. U slučaju nedostatka URDF datoteke robota moguće ju je generirati uz pomoć SOLIDWORKS paketa 

## Izrada moveit_configure datoteke

	$  roslaunch moveit_setup_assistant setup_assistant.launch
	
	
## motion_ctrl  
&ensp;&ensp;To enable or disable the servo control of any joint.(message type: ***xarm_msgs::SetAxis***)  
## set_mode  
&ensp;&ensp;To set operation mode. (message type: ***xarm_msgs::SetInt16***)  
&ensp;&ensp;* 0 for POSE mode, the robot will be position controlled. Trajectory will be planned by XArm Controller.  
&ensp;&ensp;* 1 for SERVOJ mode, the robot will be commanded by servo_j function, fast & immediate execution like a step response, use this if user can generate properly interpolated trajectory.  
&ensp;&ensp;* 2 for TEACH_JOINT mode, Gravity compensated mode, no position control.  

## set_state   
&ensp;&ensp;To set robot state. (message type: ***xarm_msgs::SetInt16***)  
&ensp;&ensp;* 0 for READY/START state, robot must be in this state to perform any motion.  
&ensp;&ensp;* 3 for PAUSE state, robot motion will be suspended.  
&ensp;&ensp;* 4 for STOP state, if error occurs or configuration changes, robot will switch to this state.  

## go_home  
&ensp;&ensp;Robot will go to home position with specified velocity and acceleration.(message type: ***xarm_msgs::Move***)  

## move_line   
&ensp;&ensp;Robot TCP will move to Caetesian target point with a straight line trajectory. Under specified Cartesian velocity and acceleartion. (message type: ***xarm_msgs::Move***)  

## move_lineb  
&ensp;&ensp;Given a set of targets, robot will move to final target through middle points, at each middle point, 2 straight-line trajectory will be blended with specified radius. (message type: ***xarm_msgs::Move***)  

## move_joint    
&ensp;&ensp;Given all desired joint positions, and max joint angular velocity/acceleration, robot will move to joint space target. (message type: ***xarm_msgs::Move***)  

## move_servoj:   
&ensp;&ensp;Used in SERVOJ mode, and if user have trajectory planned, call this service with high enough rate. Each trajectory point will be executed fast and immediately. (message type: ***xarm_msgs::Move***)  

***Please check the inside [srv](./srv/) files for detailed data information.***

# Feedback Status Message

Refer to [RobotMsg](./msg/RobotMsg.msg) for robot feedback information contents published through topic "/xarm/xarm_states".  

Refer to [CIOState](./msg/CIOState.msg) for the gpio of the control box feedback information contents published through topic "/xarm/xarm_cgpio_states".  
