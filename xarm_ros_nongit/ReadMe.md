# Uvod
&ensp;&ensp;	U nastavku ReadMe slijedi detaljan opis kako iz postojećeg xarm_description napraviti svoju simulaciju modela robotske ruke u Gazebu i Rvizu kako bi se mogli isprobavati različiti kontroleri. Istim postupkom moguće je napraviti simulaciju u Gazebu i kinematičli model pomoću Moveit-a za bilo koju ruku. U slučaju nedostatka URDF datoteke robota moguće ju je generirati uz pomoć SOLIDWORKS paketa 

## Izrada moveit_configure datoteke

	$  roslaunch moveit_setup_assistant setup_assistant.launch
	
&ensp;&ensp;	Nakon pokretanja moveit asistenta potrebno je odabrati URDF datoteku robotske ruke.
	
![](ReadMe_image/Start.png)
	

&ensp;&ensp;	Poslije učuitavanja modela potrebno je definirati Self-Collisins. Ovdje je potrebno stisnuti na gumb ***Generate Collisions Matrix***

![](ReadMe_image/self_collision.png)


&ensp;&ensp;	U Planning groupu potrebno je definirati kinematički algoritam za rješavanje pozicije svih zglobova u prostoru. Najčešće korišteni algoritam je ***kdl_kinematics_plugin/KDLKinematicsPlugin***. 


![](ReadMe_image/Planning_groups.png)

&ensp;&ensp;	Zadnji korak koji je potreban unutar Planning Groups-a je definiranje svih Jointova unutar kinematičkog modela. U slučaju da se unutar robotske ruke nalazi i hvataljka potrebno je napraviti zasebni kinematički model za nju unutar Planning Groupsa te se za nju ne specificira Kinematic Solver.

![](ReadMe_image/add_joints.png)

&ensp;&ensp;	Unutar Robot Poses moguće je isprobati ispravnost pokretanja svih zglobova i spremiti glavne pozicije robota u kojima bi se on mogao nalaziti. U ovom slučaju spremljena je njegova početna pozicija. Treba stisnuti na gumb ***Add Pose***

![](ReadMe_image/nulta_pozicija.png)

&ensp;&ensp;	Unutar End Effectors-a definira se zadnji zglob na robotu. U ovom slučaju ne koristi se hvataljka te je njegov zadnji zglob joint5 unutar kinematičkog modela arm_controller.

![](ReadMe_image/end_effector.png)

&ensp;&ensp;	Unutar ROS Controla potrebno je definirati željeni kontroller pomoću ***Add Controller*** ili ***Auto Add Follow Joints Trajectory Controllers For Each Planning Groups***. Moguće je odabrati između više različitih vrsta controllera te je u ovom slučaju odabran pomoću ***Add Controller*** naredbe position_controllers/JointTrajectoryController. Te je na slici ispod moguće vidjeti kako se definira kontroler.

![](ReadMe_image/position_controller.png)

&ensp;&ensp;	Potrebno je definirati podatke autora. Zadnji dio generiranja robot_moveit_config paketa je odabrati gdje će datoteka biti spremljena i što sve želimo definirati. Ispravna nomenklatura za generiranje paketa je ***imerobota_moveit_conig***. 

![](ReadMe_image/Generate_configuration_files.png)
	
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
