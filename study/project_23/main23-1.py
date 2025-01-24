# tkinter: GUI 라이브러리
# RPi.GPIO: 라즈베리파이 GPIO 핀 제어 라이브러리
import tkinter
import tkinter.font
import RPi.GPIO as GPIO

# 빨간색, 초록색 LED가 연결된 GPIO 핀 번호
redLedPin = 23
greenLedPin = 24

# GPIO 설정
GPIO.setwarnings(False)  # 경고 메시지 비활성화
GPIO.setmode(GPIO.BCM)  # BCM 핀 번호 사용
GPIO.setup(redLedPin, GPIO.OUT)  # 빨간 LED 출력 모드 설정
GPIO.setup(greenLedPin, GPIO.OUT)  # 초록 LED 출력 모드 설정

# 팬 모터가 연결된 GPIO 핀 번호
motorAIA = 20
motorAIB = 21

# 팬 모터 핀을 출력 모드로 설정
GPIO.setup(motorAIA, GPIO.OUT)
GPIO.setup(motorAIB, GPIO.OUT)

# 팬 모터 PWM 설정 (주파수: 500Hz)
motorAIAPwm = GPIO.PWM(motorAIA, 500)
motorAIAPwm.start(0)  # 초기 듀티 사이클: 0% (정지 상태)

motorAIBPwm = GPIO.PWM(motorAIB, 500)
motorAIBPwm.start(0)  # 초기 듀티 사이클: 0% (정지 상태)

# 빨간색 LED 켜기 함수
def redLedOn():
    GPIO.output(redLedPin, 1)  # GPIO 핀에 HIGH 신호 출력 (LED 켜기)

# 빨간색 LED 끄기 함수
def redLedOff():
    GPIO.output(redLedPin, 0)  # GPIO 핀에 LOW 신호 출력 (LED 끄기)

# 초록색 LED 켜기 함수
def greenLedOn():
    GPIO.output(greenLedPin, 1)  # GPIO 핀에 HIGH 신호 출력 (LED 켜기)

# 초록색 LED 끄기 함수
def greenLedOff():
    GPIO.output(greenLedPin, 0)  # GPIO 핀에 LOW 신호 출력 (LED 끄기)

# 팬 속도 제어 함수 (슬라이더 값에 따라 변경)
def fanSpeed(self):
    value = scale.get()  # 슬라이더 값 가져오기
    print(value)  # 현재 슬라이더 값 출력 (디버깅용)
    motorAIAPwm.ChangeDutyCycle(0)  # AIA 핀 듀티 사이클: 0 (정지)
    motorAIBPwm.ChangeDutyCycle(value)  # AIB 핀 듀티 사이클: 슬라이더 값 설정

# Tkinter GUI 생성
window = tkinter.Tk()
window.title("LED FAN CONTROL")  # 창 제목 설정
window.geometry("400x400")  # 창 크기 설정
window.resizable(False, False)  # 창 크기 조정 비활성화

# 폰트 설정
font = tkinter.font.Font(size=15)

# 빨간색 LED 컨트롤 버튼 및 레이블 생성
redLedLabel = tkinter.Label(window, text="RED LED", font=font)  # 레이블: "RED LED"
redLedOnBtn = tkinter.Button(window, width=6, height=2, text="on", command=redLedOn)  # 빨간 LED 켜기 버튼
redLedOffBtn = tkinter.Button(window, width=6, height=2, text="off", command=redLedOff)  # 빨간 LED 끄기 버튼

# 초록색 LED 컨트롤 버튼 및 레이블 생성
greenLedLabel = tkinter.Label(window, text="GREEN LED", font=font)  # 레이블: "GREEN LED"
greenLedOnBtn = tkinter.Button(window, width=6, height=2, text="on", command=greenLedOn)  # 초록 LED 켜기 버튼
greenLedOffBtn = tkinter.Button(window, width=6, height=2, text="off", command=greenLedOff)  # 초록 LED 끄기 버튼

# 팬 속도 제어 레이블과 슬라이더 생성
fanLabel = tkinter.Label(window, text="FAN SPEED", font=font)  # 팬 속도 레이블
var = tkinter.IntVar()  # 슬라이더 값 저장 변수
scale = tkinter.Scale(window, variable=var, command=fanSpeed, orient="horizontal", showvalue=False, tickinterval=10, to=100, length=300)
# 슬라이더 속성:
# - `orient="horizontal"`: 수평 방향
# - `to=100`: 최대 값 100
# - `length=300`: 슬라이더 길이 300px

# GUI 위젯 배치
redLedLabel.grid(row=0, column=0) 
redLedOnBtn.grid(row=0, column=1)  
redLedOffBtn.grid(row=0, column=2)  
greenLedLabel.grid(row=1, column=0) 
greenLedOnBtn.grid(row=1, column=1)  
greenLedOffBtn.grid(row=1, column=2) 
fanLabel.grid(row=2, column=0, columnspan=3) 
scale.grid(row=3, column=0, columnspan=3)  

window.mainloop()

GPIO.cleanup()
