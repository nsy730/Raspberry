#include <Wire.h>
#include <Adafruit_MLX90614.h>

int treshold=500;       //잡음세기 500으로 설정
int gasPin;
int volume;
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

//SCL=A5,SDA=A4
 
void setup() {
  Serial.begin(9600);

  mlx.begin();  //mlx모듈을 읽어들이기 시작
  Wire.begin();
}

void loop() {
  gasPin=analogRead(A3);
  volume=analogRead(A0);
  Serial.print(mlx.readObjectTempC()+10);   //체온 출력
  Serial.print(",");

  Wire.requestFrom(0xA0 >> 1, 1);    
  while(Wire.available()) {              //읽을 값이 있다면
        unsigned char c = Wire.read();   //센서 값 읽기
        Serial.print(c, DEC);            //맥박 출력
    }

  Serial.print(",");

  Serial.print(volume);
  Serial.print(",");
  
  if(volume>=treshold) {
    Serial.print("ON");               //감지된 소리가 잡음보다 높다면 소리감지센서 ON
  }

  else if(volume<treshold){
    Serial.print("OFF");              //감지된 소리가 잡음보다 낮다면 소리감지센서 OFF
  }

  Serial.print(",");
  Serial.print(gasPin);
  Serial.print(",");
  
  if(gasPin>=200) {
    Serial.println("ON");             //gasPin이 200보다 높다면 가스센서 ON
  }
  else if(gasPin<200) {
    Serial.println("OFF");            //gasPin이 200보다 낮다면 가스센서 OFF
  }
 
  delay(1000);
}
