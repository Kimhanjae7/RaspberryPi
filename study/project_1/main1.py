# RPi.GPIO 모듈 (라즈베리파이 GPIO 핀 제어 라이브러리)
import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정 (BCM 모드 사용)
GPIO.setmode(GPIO.BCM)

# GPIO 핀 16, 20, 21번을 출력 모드로 설정
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

try:
    while 1:  # 반복
        # GPIO 핀 16, 20, 21번에 HIGH 신호 출력 (LED 켜기)
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.HIGH)
        time.sleep(1.0)  # 1초 대기
        
        # GPIO 핀 16, 20, 21번에 LOW 신호 출력 (LED 끄기)
        GPIO.output(16, GPIO.LOW)
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        time.sleep(1.0)  

except KeyboardInterrupt:  # 키보드 인터럽트(Ctrl + C) 발생 시 실행
    pass  # 아무 작업도 하지 않고 넘어감

# GPIO 설정 초기화 (모든 핀을 안전한 상태로)
GPIO.cleanup()
