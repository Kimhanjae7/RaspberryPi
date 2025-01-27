// libgpiod 설치 및 확인
// sudo apt install -y gpiod libgpiod-dev
// gpiodetect
// libgpiod 이외에도 sysfs와 WiringPi도 존재

#include <gpiod.h>  // libgpiod 헤더 파일 포함
#include <stdio.h>
#include <unistd.h>  // sleep 함수 사용을 위해

#define GPIO_CHIP "/dev/gpiochip0"  // GPIO 컨트롤러 디바이스 경로
#define LED1 16  // GPIO 핀 번호 (BCM 모드)
#define LED2 20  // GPIO 핀 번호 (BCM 모드)
#define LED3 21  // GPIO 핀 번호 (BCM 모드)

int main() {
    struct gpiod_chip *chip;
    struct gpiod_line *line1, *line2, *line3;
    int ret;

    // GPIO 컨트롤러 열기
    chip = gpiod_chip_open(GPIO_CHIP);
    if (!chip) {
        perror("Failed to open GPIO chip");
        return 1;
    }

    // GPIO 라인 가져오기
    line1 = gpiod_chip_get_line(chip, LED1);
    line2 = gpiod_chip_get_line(chip, LED2);
    line3 = gpiod_chip_get_line(chip, LED3);
    if (!line1 || !line2 || !line3) {
        perror("Failed to get GPIO line");
        gpiod_chip_close(chip);
        return 1;
    }

    // GPIO 라인을 출력으로 요청
    ret = gpiod_line_request_output(line1, "led_blink", 0);
    if (ret < 0) {
        perror("Failed to request line1 as output");
        gpiod_chip_close(chip);
        return 1;
    }
    ret = gpiod_line_request_output(line2, "led_blink", 0);
    if (ret < 0) {
        perror("Failed to request line2 as output");
        gpiod_chip_close(chip);
        return 1;
    }
    ret = gpiod_line_request_output(line3, "led_blink", 0);
    if (ret < 0) {
        perror("Failed to request line3 as output");
        gpiod_chip_close(chip);
        return 1;
    }

    printf("Press Ctrl+C to stop the program.\n");

    // LED 깜빡이기
    while (1) {
        printf("LEDs ON\n");
        gpiod_line_set_value(line1, 1);  // LED1 ON
        gpiod_line_set_value(line2, 1);  // LED2 ON
        gpiod_line_set_value(line3, 1);  // LED3 ON
        sleep(1);  

        printf("LEDs OFF\n");
        gpiod_line_set_value(line1, 0);  // LED1 OFF
        gpiod_line_set_value(line2, 0);  // LED2 OFF
        gpiod_line_set_value(line3, 0);  // LED3 OFF
        sleep(1);  
    }

    // 리소스 해제 (프로그램 종료 시)
    gpiod_line_release(line1);
    gpiod_line_release(line2);
    gpiod_line_release(line3);
    gpiod_chip_close(chip);

    return 0;
}
