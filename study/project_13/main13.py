import RPi.GPIO as GPIO
import time
import picamera
import datetime

# 스위치 핀이 연결된 GPIO 핀 번호 설정 (GPIO 14번 사용)
swPin = 14

# GPIO 경고 메시지 비활성화
GPIO.setwarnings(False)

# GPIO 모드 설정 (BCM 핀 번호 방식)
GPIO.setmode(GPIO.BCM)

# GPIO 핀 설정: 스위치 핀을 입력 모드로 설정하고, 풀다운 저항 연결
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 스위치의 이전 상태와 현재 상태를 저장할 변수 초기화
oldSw = 0
newSw = 0

# PiCamera 객체 생성 및 해상도 설정
camera = picamera.PiCamera()
camera.resolution = (1024, 768)  # 해상도: 1024x768

try:
    while True:  # 반복문
        # 현재 스위치 상태를 읽어 변수에 저장
        newSw = GPIO.input(swPin)

        # 스위치 상태가 이전 상태와 다를 때만 처리
        if newSw != oldSw:
            oldSw = newSw  # 현재 상태를 이전 상태로 갱신

            if newSw == 1:  # 스위치가 눌린 경우
                now = datetime.datetime.now()  # 현재 날짜와 시간 가져오기
                print(now)  # 현재 날짜와 시간 출력
                # 파일 이름을 현재 날짜와 시간으로 설정
                fileName = now.strftime('%Y-%m-%d %H:%M:%S')
                # 파일 이름으로 사진 촬영
                camera.capture(fileName + '.jpg')

            # 상태 변경 감지를 위한 대기 시간
            time.sleep(0.2)

except KeyboardInterrupt:  # 키보드 인터럽트(Ctrl + C) 발생 시 종료
    pass  

GPIO.cleanup()
