import speech_recognition as sr  # 음성 인식 라이브러리
import RPi.GPIO as GPIO  # 라즈베리파이 GPIO 제어 라이브러리

# LED 핀 번호 설정 (BCM 모드)
greenLed = 16
blueLed = 20
redLed = 21

# GPIO 설정
GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BCM) 
GPIO.setup(greenLed, GPIO.OUT)  
GPIO.setup(blueLed, GPIO.OUT)  
GPIO.setup(redLed, GPIO.OUT)    

try:
    while True:
        r = sr.Recognizer()  # 음성 인식 객체 생성

        with sr.Microphone() as source:  # 마이크를 입력 소스로 사용
            print("Say Something!")  # 사용자에게 음성 입력을 요청
            audio = r.listen(source)  # 마이크에서 음성을 듣고 저장

        try:
            # Google Speech Recognition API를 사용하여 음성을 텍스트로 변환 (한국어 설정)
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text)  # 인식된 텍스트 출력

            # LED 제어 로직
            if text == "빨간색":
                GPIO.output(greenLed, 0)  
                GPIO.output(blueLed, 0)  
                GPIO.output(redLed, 1)   
                print("빨간색 LED가 켜졌습니다.")

            elif text == "파란색":
                GPIO.output(greenLed, 0)
                GPIO.output(blueLed, 1)
                GPIO.output(redLed, 0)
                print("파란색 LED가 켜졌습니다.")

            elif text == "녹색":
                GPIO.output(greenLed, 1)  
                GPIO.output(blueLed, 0)
                GPIO.output(redLed, 0)
                print("녹색 LED가 켜졌습니다.")

            elif text == "꺼":
                GPIO.output(greenLed, 0)  
                GPIO.output(blueLed, 0)
                GPIO.output(redLed, 0)
                print("모든 LED가 꺼졌습니다.")

            else:
                print("명령어를 인식하지 못했습니다.")

        except sr.UnknownValueError:  # 음성을 인식할 수 없는 경우
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:  # Google API 요청 실패 시
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:  # 키보드 인터럽트(Ctrl + C) 발생 시 실행
    print("\n프로그램 종료")

finally:
    GPIO.cleanup()  # GPIO 핀 초기화
