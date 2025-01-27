import pyaudio  # 오디오 스트림 처리 라이브러리
import wave  # WAV 파일 생성 및 처리 라이브러리

# 오디오 스트림 설정
CHUNK = 1024  # 오디오 데이터를 나누는 단위 (버퍼 크기)
FORMAT = pyaudio.paInt16  # 샘플 형식 (16비트 정수)
CHANNELS = 1  # 채널 수 (모노)
RATE = 44100  # 샘플링 레이트 (1초당 44100 샘플)
RECORD_SECONDS = 5  # 녹음 시간 (초)
WAVE_OUTPUT_FILENAME = "output.wav"  # 저장할 WAV 파일 이름

# PyAudio 객체 생성
p = pyaudio.PyAudio()

# 오디오 스트림 열기
stream = p.open(
    format=FORMAT,  # 오디오 데이터 형식
    channels=CHANNELS,  # 채널 수
    rate=RATE,  # 샘플링 레이트
    input=True,  # 입력 스트림 활성화
    frames_per_buffer=CHUNK  # 버퍼 크기
)

print("Start to record the audio.") 

frames = []  # 오디오 데이터를 저장할 리스트

# 녹음 루프
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)  # CHUNK 크기만큼 오디오 데이터 읽기
    frames.append(data)  # 읽은 데이터를 리스트에 추가

print("Recording is finished") 

# 스트림 종료
stream.stop_stream() 
stream.close()  
p.terminate()  

# WAV 파일 생성
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  # 쓰기 모드로 WAV 파일 열기
wf.setnchannels(CHANNELS)  # 채널 수 설정
wf.setsampwidth(p.get_sample_size(FORMAT))  # 샘플 크기 설정
wf.setframerate(RATE)  # 샘플링 레이트 설정
wf.writeframes(b' '.join(frames))  # 오디오 데이터를 파일에 쓰기
wf.close() 
