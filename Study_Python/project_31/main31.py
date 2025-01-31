import speech_recognition as sr  # 음성 인식 라이브러리 가져오기

try:
    while True:  # 무한 반복
        r = sr.Recognizer()  # 음성 인식기 객체 생성

        with sr.Microphone() as source:  # 마이크를 입력 소스로 사용
            print("Say Something!")  # 사용자에게 음성 입력을 요청
            audio = r.listen(source)  # 마이크에서 음성을 듣고 저장

        try:
            # Google Speech Recognition API를 사용하여 음성을 텍스트로 변환 (한국어 설정)
            print("You said: " + r.recognize_google(audio, language='ko-KR'))

        except sr.UnknownValueError:  # 음성을 인식할 수 없는 경우
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:  # Google API 요청 실패 시
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt: 
    pass  
