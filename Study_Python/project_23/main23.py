# tkinter: GUI 라이브러리
# RPi.GPIO: 라즈베리파이 GPIO 핀 제어 라이브러리
import tkinter
import tkinter.font
import RPi.GPIO as GPIO

# 빨간색과 초록색 LED가 연결된 GPIO 핀 번호
redLedPin = 23
greenLedPin = 24

GPIO.setwarnings(False)

# GPIO 모드 설정 (BCM 핀 번호 방식)
GPIO.setmode(GPIO.BCM)

# 빨간색과 초록색 LED 핀을 출력 모드로 설정
GPIO.setup(redLedPin, GPIO.OUT)
GPIO.setup(greenLedPin, GPIO.OUT)

# 빨간색 LED 켜기 함수
def redLedOn():
    GPIO.output(redLedPin, 1)  # GPIO 핀에 HIGH 신호 출력

# 빨간색 LED 끄기 함수
def redLedOff():
    GPIO.output(redLedPin, 0)  # GPIO 핀에 LOW 신호 출력

# 초록색 LED 켜기 함수
def greenLedOn():
    GPIO.output(greenLedPin, 1)  # GPIO 핀에 HIGH 신호 출력

# 초록색 LED 끄기 함수
def greenLedOff():
    GPIO.output(greenLedPin, 0)  # GPIO 핀에 LOW 신호 출력

# Tkinter 윈도우 생성
window = tkinter.Tk()
window.title("LED FAN CONTROL")  # 창 제목 설정
window.geometry("400x400")  # 창 크기 설정
window.resizable(False, False)  # 창 크기 조정 비활성화

font = tkinter.font.Font(size=15)

# 빨간색 LED 컨트롤 버튼 및 레이블 생성
redLedLabel = tkinter.Label(window, text="RED LED", font=font)  # 레이블: "RED LED"
redLedOnBtn = tkinter.Button(window, width=6, height=2, text="on", command=redLedOn)  # 빨간 LED 켜기 버튼
redLedOffBtn = tkinter.Button(window, width=6, height=2, text="off", command=redLedOff)  # 빨간 LED 끄기 버튼

# 초록색 LED 컨트롤 버튼 및 레이블 생성
greenLedLabel = tkinter.Label(window, text="GREEN LED", font=font)  # 레이블: "GREEN LED"
greenLedOnBtn = tkinter.Button(window, width=6, height=2, text="on", command=greenLedOn)  # 초록 LED 켜기 버튼
greenLedOffBtn = tkinter.Button(window, width=6, height=2, text="off", command=greenLedOff)  # 초록 LED 끄기 버튼

# 위젯을 화면에 배치 (Grid 레이아웃 사용)
redLedLabel.grid(row=0, column=0) 
redLedOnBtn.grid(row=0, column=1) 
redLedOffBtn.grid(row=0, column=2)  
greenLedLabel.grid(row=1, column=0)  
greenLedOnBtn.grid(row=1, column=1)  
greenLedOffBtn.grid(row=1, column=2)  

window.mainloop()

GPIO.cleanup()
