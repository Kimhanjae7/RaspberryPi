import time  # 시간 관련 라이브러리
import datetime  

try:
    while True:  # 무한 반복복
        now = datetime.datetime.now()  # 현재 날짜와 시간 가져오기
        nowSec = now.second  # 현재 시간의 초 단위 가져오기

        # 현재 초가 0일 때 (즉, 1분마다다)
        if nowSec == 0:
            # 현재 시간을 지정된 형식으로 문자열로 변환
            nowTime = now.strftime("%H시 %M분 %S초 입니다.")
            print(nowTime)  # 현재 시간 출력

        time.sleep(1)  # 1초 대기

except KeyboardInterrupt: 
    pass  
