#include <Servo.h>
Servo servo; 
String inByte;
int pos;

void setup(){
  servo.attach(9);
  servo.write(0);
  delay(1000);
  Serial.begin(9600);
}

void loop(){    
  if(Serial.available()){ 
    inByte = Serial.readStringUntil('\n'); 
    pos = inByte.toInt();    
    pos = map(pos,0,100,180,0);   
    servo.write(pos);
    Serial.print("Servo in position: ");  
    Serial.println(inByte);
  }
}
