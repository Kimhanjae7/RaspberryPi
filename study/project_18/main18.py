import time
import datetime

try:
    while True:
        now = datetime.datetime.now()
        nowSec = now.second

        if nowSec == 0:
            nowTime = now.strftime("%H시 %M분 %S초 입니다.")
            print(nowTime)
        
        time.sleep(1)

except KeyboardInterrupt:
    pass
