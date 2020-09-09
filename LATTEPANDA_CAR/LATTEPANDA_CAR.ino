#include <Servo.h>

#define RFORWARD_SERVO 7        //define a pin for servo
#define RBACK_SERVO 8
#define LFORWARD_SERVO 9
#define LBACK_SERVO 10

Servo r1_servo;        // initialize  servo
Servo r2_servo;
Servo l1_servo;
Servo l2_servo;

#define FORWARD 5
#define RIGHT 2
#define BACK 3
#define LEFT 4
#define STOP 1

const int neutral = 1485;
const int forward = 2000;
const int backward = 1000;

unsigned char action_number = 0;


/*setupは起動後ときに最小に呼び出される関数でここで初期化の処理を行います*/
void setup() {
  //シリアル通信の初期化しシリアルモニタへ文字列を出力できるようにする　9600はボーレート(通信速度)
  Serial.begin(9600);
  pinMode (RFORWARD_SERVO, OUTPUT);  // want servo pin to be an output
  pinMode (RBACK_SERVO, OUTPUT);  // want servo pin to be an output
  pinMode (LFORWARD_SERVO, OUTPUT);  // want servo pin to be an output
  pinMode (LBACK_SERVO, OUTPUT);  // want servo pin to be an output
  r1_servo.attach(RFORWARD_SERVO);  // attach pin to the servo 
  r2_servo.attach(RBACK_SERVO);  // attach pin to the servo 
  l1_servo.attach(LFORWARD_SERVO);  // attach pin to the servo 
  l2_servo.attach(LBACK_SERVO);  // attach pin to the servo 
  go_stop();

}

/*setupの後、終了するまで繰り返し呼び出される関数です*/
void loop() {
  ReceiveMassage();
  action();
}

/*setupの後、終了するまで繰り返し呼び出される関数です*/
void ReceiveMassage(){
  action_number = Serial.read();     //文字を読む
  //Serial.println(action_number);       //シリアルポートにcmdを出力し表示する
  readaction();
}

int readaction()
{
  if(action_number == 0)
    return STOP;
  
  if(action_number == 's')
    return STOP;
  else if(action_number == 'r')
    return RIGHT;
  else if(action_number == 'b')
    return BACK;
  else if(action_number == 'l')
    return LEFT;
  else if(action_number == 'f')
    return FORWARD;
}

void action()
{
  int action =  readaction();
  switch (action) {
      case 1:
        go_stop(); 
        break;
      case 2:
        go_right(); 
        break;
      case 3:
        go_back(); 
        break;
      case 4:
        go_left(); 
        break;
      case 5:
        go_straight(); 
        break;
      default:
        go_stop();
        break;
     }
}

void go_straight(){
  r1_servo.writeMicroseconds(forward);
  r2_servo.writeMicroseconds(forward);
  l1_servo.writeMicroseconds(forward);
  l2_servo.writeMicroseconds(forward);
}

void go_right(){
  r1_servo.writeMicroseconds(backward);
  r2_servo.writeMicroseconds(backward);
  l1_servo.writeMicroseconds(forward);
  l2_servo.writeMicroseconds(forward);
}

void go_left(){
  r1_servo.writeMicroseconds(forward);
  r2_servo.writeMicroseconds(forward);
  l1_servo.writeMicroseconds(backward);
  l2_servo.writeMicroseconds(backward);
}

void go_back(){
  r1_servo.writeMicroseconds(backward);
  r2_servo.writeMicroseconds(backward);
  l1_servo.writeMicroseconds(backward);
  l2_servo.writeMicroseconds(backward);
}

void go_stop(){
  r1_servo.writeMicroseconds(neutral);
  r2_servo.writeMicroseconds(neutral);
  l1_servo.writeMicroseconds(neutral);
  l2_servo.writeMicroseconds(neutral);
}
