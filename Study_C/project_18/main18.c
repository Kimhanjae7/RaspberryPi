#include <gpiod.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>  // sleep 함수 사용

#define GPIO_CHIP "/dev/gpiochip0"  // GPIO 컨트롤러 경로
#define LED_PIN 16  // 사용할 GPIO 핀 (BCM 16번 핀)

int main() {
    struct gpiod_chip *chip;
    struct gpiod_line *line;
    int ret;

    // GPIO 컨트롤러 열기
    chip = gpiod_chip_open(GPIO_CHIP);
    if (!chip) {
        perror("Failed to open GPIO chip");
        return 1;
    }

    // GPIO 라인 가져오기
    line = gpiod_chip_get_line(chip, LED_PIN);
    if (!line) {
        perror("Failed to get GPIO line");
        gpiod_chip_close(chip);
        return 1;
    }

    // GPIO 라인을 출력으로 설정
    ret = gpiod_line_request_output(line, "led_control", 0);
    if (ret < 0) {
        perror("Failed to request GPIO line as output");
        gpiod_chip_close(chip);
        return 1;
    }

    printf("Press Ctrl+C to stop the program.\n");

    while (1) {
        // 현재 시간을 가져오기
        time_t rawtime = time(NULL);
        struct tm *current_time = localtime(&rawtime);
        int now_sec = current_time->tm_sec;  // 초 단위 가져오기

        // 초가 0일 때 GPIO 핀 켜기
        if (now_sec == 0) {
            printf("%02d:%02d:%02d - LED ON\n", current_time->tm_hour, current_time->tm_min, now_sec);
            gpiod_line_set_value(line, 1);  // GPIO 핀 HIGH (LED 켜기)
        } else {
            gpiod_line_set_value(line, 0);  // GPIO 핀 LOW (LED 끄기)
        }

        usleep(100000);  // 0.1초 대기
    }

    // 리소스 해제
    gpiod_line_release(line);
    gpiod_chip_close(chip);

    return 0;
}
