#include <Wire.h>
#include <EEPROM.h>
#include <fuzzy_table.h>
#include <PID_Beta6.h>

#include <PinChangeInt.h>
#include <PinChangeIntConfig.h>

#include <MotorWheel.h>
#include <Omni3WD.h>

#include <SONAR.h>

#define FORWARD 1
#define RIGHT 2
#define BACK 3
#define LEFT 4
#define STOP 5


// Wheels

irqISR(irq1,isr1);
MotorWheel wheel1(9,8,6,7,&irq1);        // Pin9:PWM, Pin8:DIR, Pin6:PhaseA, Pin7:PhaseB

irqISR(irq2,isr2)
MotorWheel wheel2(10,11,14,15,&irq2);    // Pin10:PWM, Pin11:DIR, Pin14:PhaseA, Pin15:PhaseB

irqISR(irq3,isr3);
MotorWheel wheel3(3,2,4,5,&irq3);        // Pin3:PWM, Pin2:DIR, Pin4:PhaseA, Pin5:PhaseB

Omni3WD Omni(&wheel1,&wheel2,&wheel3);

unsigned long currMillis=0;
unsigned char action_number = 0;

int SLAVE_ADDRESS = 0x51;   //I2Cのアドレス『0x51』

/*setupは起動後ときに最小に呼び出される関数でここで初期化の処理を行います*/
void setup() {
  //シリアル通信の初期化しシリアルモニタへ文字列を出力できるようにする　9600はボーレート(通信速度)
  Serial.begin(9600);

  TCCR1B=TCCR1B&0xf8|0x01;    // Pin9,Pin10 PWM 31250Hz
  TCCR2B=TCCR2B&0xf8|0x01;    // Pin3,Pin11 PWM 31250Hz

  Omni.PIDEnable(0.26,0.02,0,10);
  Omni.setCarStop();

  //I2C接続を開始する 
  Wire.begin(SLAVE_ADDRESS);

  //I2Cで受信したときに呼び出す関数を登録する
  Wire.onReceive(ReceiveMassage);

}

/*setupの後、終了するまで繰り返し呼び出される関数です*/
void loop() {
  action(80);
}

/*setupの後、終了するまで繰り返し呼び出される関数です*/
void ReceiveMassage(int n){
  action_number = Wire.read();     //文字を読む
  Serial.println(action_number);       //シリアルポートにcmdを出力し表示する
  readaction();
}

int readaction()
{
  if(action_number == 0)
    return STOP;
  
  if(action_number == 'f')
    return FORWARD;
  else if(action_number == 'r')
    return RIGHT;
  else if(action_number == 'b')
    return BACK;
  else if(action_number == 'l')
    return LEFT;
  else if(action_number == 's')
    return STOP;
}

void action(unsigned int speedMMPS)
{
  int action =  readaction();
  switch (action) {
      case 1:
        Omni.setCarAdvance(speedMMPS); 
        break;
      case 2:
        Omni.setCarRight(speedMMPS); 
        break;
      case 3:
        Omni.setCarBackoff(speedMMPS); 
        break;
      case 4:
        Omni.setCarLeft(speedMMPS); 
        break;
      case 5:
        Omni.setCarStop(); 
        break;
      default:
        Omni.setCarStop();
        break;
     }
      Omni.PIDRegulate();
      if(millis()%100==0) Omni.debugger();
}
