import time
from adafruit_servokit import ServoKit

kit = [ServoKit(address=0x40, channels=16), ServoKit(address=0x41, channels=16)]

for c in range(16):
    kit[0].servo[c].actuation_range = 270
    kit[0].servo[c].set_pulse_width_range(500, 2500)
    kit[1].servo[c].actuation_range = 270
    kit[1].servo[c].set_pulse_width_range(500, 2500)
    
speed = 0.125

RB = []
RB.extend((kit[0].servo[0], kit[0].servo[1], kit[0].servo[2]))
RM = []
RM.extend((kit[0].servo[3], kit[0].servo[4], kit[0].servo[5]))
RF = []
RF.extend((kit[0].servo[6], kit[0].servo[7], kit[0].servo[8]))

LF = []
LF.extend((kit[1].servo[0], kit[1].servo[1], kit[1].servo[2]))
LM = []
LM.extend((kit[1].servo[3], kit[1].servo[4], kit[1].servo[5]))
LB = []
LB.extend((kit[1].servo[6], kit[1].servo[7], kit[1].servo[8]))

joint0 = [LB[0],LM[0],LF[0],RB[0],RM[0],RF[0]]
joint1 = [LB[1],LM[1],LF[1],RB[1],RM[1],RF[1]]
joint2 = [LB[2],LM[2],LF[2],RB[2],RM[2],RF[2]]

offset = -135
# Setting limits on movement ranges
max_angle_joint0 = 30
min_angle_joint0 = -30
max_angle_joint1 = 100
min_angle_joint1 = -100
max_angle_joint2 = 120
min_angle_joint2 = -120

def seg(joint,deg):
    
# Enforcing the limits on movement ranges
    if joint in joint0 and deg > max_angle_joint0:
        deg = max_angle_joint0    
    if joint in joint0  and deg < min_angle_joint0:
        deg = min_angle_joint0
    if joint in joint1 and deg > max_angle_joint1:
        deg = max_angle_joint1    
    if joint in joint1  and deg < min_angle_joint1:
        deg = min_angle_joint1
    if joint in joint2 and deg > max_angle_joint2:
        deg = max_angle_joint2    
    if joint in joint2  and deg < min_angle_joint2:
        deg = min_angle_joint2    
       
# Moving joints with tuning      
    if joint == LB[0]:
        tuning = 0
        joint.angle = abs(offset - deg - tuning)        
    if joint == LB[1]:
        tuning = 6
        joint.angle = abs(offset - deg - tuning)
    if joint == LB[2]:
        tuning = 8
        joint.angle = abs(offset - deg - tuning)        
        
    if joint == LM[0]:
        tuning = 0
        joint.angle = abs(offset - deg - tuning)        
    if joint == LM[1]:
        tuning = 8
        joint.angle = abs(offset - deg - tuning)
    if joint == LM[2]:
        tuning = 3
        joint.angle = abs(offset - deg - tuning) 

    if joint == LF[0]:
        tuning = 0
        joint.angle = abs(offset - deg - tuning)        
    if joint == LF[1]:
        tuning = 2
        joint.angle = abs(offset - deg - tuning)
    if joint == LF[2]:
        tuning = 0
        joint.angle = abs(offset - deg - tuning) 

    if joint == RB[0]:
        tuning = 0 
        joint.angle = abs(offset + deg + tuning)        
    if joint == RB[1]:
        tuning = 0 
        joint.angle = abs(offset + deg + tuning)   
    if joint == RB[2]:
        tuning = 7 
        joint.angle = abs(offset + deg + tuning)    
        
    if joint == RM[0]:
        tuning = 0 
        joint.angle = abs(offset + deg + tuning)        
    if joint == RM[1]:
        tuning = 5 
        joint.angle = abs(offset + deg + tuning)   
    if joint == RM[2]:
        tuning = 3 
        joint.angle = abs(offset + deg + tuning)            
        
    if joint == RF[0]:
        tuning = 0 
        joint.angle = abs(offset + deg + tuning)        
    if joint == RF[1]:
        tuning = 6
        joint.angle = abs(offset + deg + tuning)   
    if joint == RF[2]:
        tuning = 2 
        joint.angle = abs(offset + deg + tuning)                  

def triwalk(drift):
#if positive, walk straight with slight right drift and vice versa
    if drift > 0: #moving right
        R_drift = -drift
        L_drift = 0
    if drift < 0: #moving left
        R_drift = 0
        L_drift = drift
    elif drift == 0:
        R_drift = 0
        L_drift = 0
        
#Raise and Pivot legs LF LB  RM  
    seg(LF[0],20 + L_drift)
    seg(LF[1],10)
    seg(LF[2],-90)    
    
    seg(LB[0],20 + L_drift)
    seg(LB[1],10)
    seg(LB[2],-90)
    
    seg(RM[0],20 + R_drift)
    seg(RM[1],10)
    seg(RM[2],-90)
    
# Pivot legs LM RB RF      
    seg(LM[0],-20 - L_drift)
    seg(LM[1],-30)
    seg(LM[2],-60)
        
    seg(RB[0],-20 - R_drift)
    seg(RB[1],-30)
    seg(RB[2],-60)
     
    seg(RF[0],-20 - R_drift)
    seg(RF[1],-30)
    seg(RF[2],-60)
        
    time.sleep(speed)
                
#Lower legs LF LB RM  
    seg(LF[0],20 + L_drift)
    seg(LF[1],-30)
    seg(LF[2],-60)
       
    seg(LB[0],20 + L_drift)
    seg(LB[1],-30)
    seg(LB[2],-60)
     
    seg(RM[0],20 + R_drift)
    seg(RM[1],-30)
    seg(RM[2],-60)
        
    time.sleep(speed)
        
#Raise and Pivot legs LM RB RF
    seg(LM[0],20 + L_drift)
    seg(LM[1],10)
    seg(LM[2],-90)
        
    seg(RB[0],20 + R_drift)
    seg(RB[1],10)
    seg(RB[2],-90)
     
    seg(RF[0],20 + R_drift)
    seg(RF[1],10)
    seg(RF[2],-90)
        
# Pivot legs LF LB RM      
    seg(LF[0],-20 - L_drift)
    seg(LF[1],-30)
    seg(LF[2],-60)
       
    seg(LB[0],-20 - L_drift)
    seg(LB[1],-30)
    seg(LB[2],-60)
     
    seg(RM[0],-20 - R_drift)
    seg(RM[1],-30)
    seg(RM[2],-60)
    
    time.sleep(speed)      
    
#Lower legs LM RB RF   
    seg(LM[0],20 + L_drift)
    seg(LM[1],-30)
    seg(LM[2],-60)
        
    seg(RB[0],20 + R_drift)
    seg(RB[1],-30)
    seg(RB[2],-60)
     
    seg(RF[0],20 + R_drift)
    seg(RF[1],-30)
    seg(RF[2],-60)
    
    time.sleep(speed)   
            
def rotate(direction):
    if direction > 45: #limit max
        direction = 45
    if direction < -45: #limit min
        direction = -45
        
    r = -float(direction)/45
    l = float(direction)/45
           
#Raise and Pivot legs LF LB  RM  
    seg(LF[0],20 * l)
    seg(LF[1],10)
    seg(LF[2],-90)    
    
    seg(LB[0],20 * l)
    seg(LB[1],10)
    seg(LB[2],-90)
    
    seg(RM[0],20 * r)
    seg(RM[1],10)
    seg(RM[2],-90)
    
# Pivot legs LM RB RF      
    seg(LM[0],-20 * l)
    seg(LM[1],-30)
    seg(LM[2],-60)
        
    seg(RB[0],-20 * r)
    seg(RB[1],-30)
    seg(RB[2],-60)
     
    seg(RF[0],-20 * r)
    seg(RF[1],-30)
    seg(RF[2],-60)
        
    time.sleep(speed)
                
#Lower legs LF LB RM  
    seg(LF[0],20 * l)
    seg(LF[1],-30)
    seg(LF[2],-60)
       
    seg(LB[0],20 * l)
    seg(LB[1],-30)
    seg(LB[2],-60)
     
    seg(RM[0],20 * r)
    seg(RM[1],-30)
    seg(RM[2],-60)
        
    time.sleep(speed)
        
#Raise and Pivot legs LM RB RF
    seg(LM[0],20 * l)
    seg(LM[1],10)
    seg(LM[2],-90)
        
    seg(RB[0],20 * r)
    seg(RB[1],10)
    seg(RB[2],-90)
     
    seg(RF[0],20 * r)
    seg(RF[1],10)
    seg(RF[2],-90)
        
# Pivot legs LF LB RM      
    seg(LF[0],-20 * l)
    seg(LF[1],-30)
    seg(LF[2],-60)
       
    seg(LB[0],-20 * l)
    seg(LB[1],-30)
    seg(LB[2],-60)
     
    seg(RM[0],-20 * r)
    seg(RM[1],-30)
    seg(RM[2],-60)
    
    time.sleep(speed)      
    
#Lower legs LM RB RF   
    seg(LM[0],20 * l)
    seg(LM[1],-30)
    seg(LM[2],-60)
        
    seg(RB[0],20 * r)
    seg(RB[1],-30)
    seg(RB[2],-60)
     
    seg(RF[0],20 * r)
    seg(RF[1],-30)
    seg(RF[2],-60)
    
    time.sleep(speed)       
    
def test(leg):
    seg(leg,0)
    time.sleep(0.25)
    print("segment is moving!")
    seg(leg,10)
    time.sleep(0.25)
    seg(leg,-10)
    time.sleep(0.25)    
    seg(leg,0)
    time.sleep(0.25)   
    
def zero(x):  
    c = 0
    for c in range(3):
        seg(RB[c],x)
        seg(RM[c],x)
        seg(RF[c],x)
        
        seg(LB[c],x)
        seg(LM[c],x)
        seg(LF[c],x)

def standup():
    for j1 in joint1:
        seg(j1,90)
    for j2 in joint2:
        seg(j2,-110)
    time.sleep(1)
    
    for j1 in joint1:
        seg(j1,-30)
    time.sleep(0.25)
    for j2 in joint2:
        seg(j2,-60)
    time.sleep(1)
    
def squat(height): #0-10. 0 = body resting on ground
    rotate(0) #puts legs in safe position before squatting
    
    for j1 in joint1:
        seg(j1,-30)
    time.sleep(0.25)
    for j2 in joint2:
        seg(j2,-60)
    time.sleep(1)
    
    for j1 in joint1:
        seg(j1,90 - height*120/10)
    for j2 in joint2:
        seg(j2,-110 + height*50/10)
    time.sleep(1)
    
    
#zero(0)
#time.sleep(1)
#standup()   
#for x in range(4):
#    triwalk(-20)
#for x in range(4):
#    triwalk(20)    
#for x in range(2):
#    rotate(45)    
#for x in range(2):
#    rotate(-45)    
#for x in range(2):
#    rotate(22)    
#for x in range(2):
#    rotate(-22)    
    
##Segment Tester
#while True:  
#    segment = 0
#    x ='segment'    
#    exec("%s = %s" % (x,input("enter segment ")))
#    test(segment)
#zero()