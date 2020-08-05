import socket
import os
import sys
from subprocess import call
from time import sleep

import serial
import pymysql

#IP주소와 PORT번호 설정
HOST = "172.20.10.3"
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
print ('Socket created')
s.bind((HOST, PORT))
print ('Socket bind complete')
s.listen(1)
print ('Socket now listening')
ser=serial.Serial('/dev/ttyUSB0',9600)

#데이터베이스 정보 입력    
db=pymysql.connect(host="localhost",
                   user="root",
                   passwd="raspberry",
                   db="mysql"
                   )
curs=db.cursor()

#파이 컨트롤 함수
def do_some_stuffs_with_input(input_string):
    
    #라즈베리파이를 컨트롤할 명령어 설정
    if input_string == "d_p":               #디스플레이 영상 실행
        input_string = "play mp4"
        os.system("omxplayer -o both /home/pi/Desktop/roro.mp4")
        
    if input_string == "d_s":               #디스플레이 영상 중지
        input_string = "stop"
        os.system("q")

    #등록되지 않은 명령어가 입력되면 no command 출력
    else :
        input_string = input_string + " no command"
    return input_string

while True:
    conn, addr = s.accept()         #소켓 함수 허용
    print("Connected by ", addr)    #클라이언트 IP 주소 출력
   
    a=ser.readline()            #시리얼 모니터 한줄 씩 읽기
    a=str(a)
    b=a.replace("\\","")
    c=b.replace("b","")
    #필요없는 쓰레기값은 공백으로 대체
    
    result=c.replace("rn","")
    result=result.split(",")

    temp1=result[0]                 #온도 센서 값
    temp2=temp1.replace("'","")
       
    bpm1=result[1]                  #맥박 센서 값
    bpm2=bpm1.replace("'","")
       
    sound=result[2]                 #소리감지 센서 값
    sound2=sound.replace("'","")
        
    gas=result[3]                   #가스 센서 값
    gas3=gas.replace("\r\n","")
    gas2=gas3.replace("'","")
    
    print(temp2, bpm2, sound2, gas2)

    #데이터베이스 갱신    
    sql="UPDATE sensor SET  temp=%s, bpm=%s, sound=%s, gas=%s;"

    try:
        curs.execute(sql,(temp2,bpm2,sound2,gas2))
        db.commit()
    except:
        print("ERROR")
        db.rollback()

    data = conn.recv(1024)
    data = data.decode("utf8").strip()
    
    print("Received: " + data)      #데이터 수신

    res = do_some_stuffs_with_input(data)   
    print("pi movement :" + res)    #수신한 데이터로 pi를 컨트롤

    conn.sendall(res.encode("utf-8"))   #클라이언트에게 답을 보냄
        
    conn.close()    #연결 닫기
s.close()


