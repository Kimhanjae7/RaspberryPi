// main31.c 설치파일 참고

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <alsa/asoundlib.h>
#include <gpiod.h>
#include "vosk_api.h"  // Vosk 헤더 파일 포함

#define SAMPLE_RATE 16000  // 오디오 샘플링 레이트
#define GPIO_CHIP "/dev/gpiochip0"  // GPIO 컨트롤러
#define LED_RED 21   // 빨간색 LED (BCM 21번 핀)
#define LED_BLUE 20  // 파란색 LED (BCM 20번 핀)
#define LED_GREEN 16 // 녹색 LED (BCM 16번 핀)

// GPIO 초기화 함수
struct gpiod_chip *chip;
struct gpiod_line *red_led, *blue_led, *green_led;

void setup_gpio() {
    chip = gpiod_chip_open(GPIO_CHIP);
    if (!chip) {
        perror("GPIO 칩 열기 실패");
        exit(1);
    }

    red_led = gpiod_chip_get_line(chip, LED_RED);
    blue_led = gpiod_chip_get_line(chip, LED_BLUE);
    green_led = gpiod_chip_get_line(chip, LED_GREEN);

    if (!red_led || !blue_led || !green_led) {
        perror("GPIO 핀 가져오기 실패");
        gpiod_chip_close(chip);
        exit(1);
    }

    gpiod_line_request_output(red_led, "led_control", 0);
    gpiod_line_request_output(blue_led, "led_control", 0);
    gpiod_line_request_output(green_led, "led_control", 0);
}

// LED 제어 함수
void control_led(const char *text) {
    printf("You said: %s\n", text);

    if (strstr(text, "빨간색")) {
        gpiod_line_set_value(red_led, 1);
        gpiod_line_set_value(blue_led, 0);
        gpiod_line_set_value(green_led, 0);
        printf("빨간색 LED가 켜졌습니다.\n");
    } 
    else if (strstr(text, "파란색")) {
        gpiod_line_set_value(red_led, 0);
        gpiod_line_set_value(blue_led, 1);
        gpiod_line_set_value(green_led, 0);
        printf("파란색 LED가 켜졌습니다.\n");
    } 
    else if (strstr(text, "녹색")) {
        gpiod_line_set_value(red_led, 0);
        gpiod_line_set_value(blue_led, 0);
        gpiod_line_set_value(green_led, 1);
        printf("녹색 LED가 켜졌습니다.\n");
    } 
    else if (strstr(text, "꺼")) {
        gpiod_line_set_value(red_led, 0);
        gpiod_line_set_value(blue_led, 0);
        gpiod_line_set_value(green_led, 0);
        printf("모든 LED가 꺼졌습니다.\n");
    } 
    else {
        printf("알 수 없는 명령어입니다.\n");
    }
}

int main() {
    setup_gpio();  // GPIO 설정

    VoskModel *model = vosk_model_new("model");  // 한국어 모델 로드
    if (!model) {
        fprintf(stderr, "모델 로드 실패!\n");
        return 1;
    }

    VoskRecognizer *recognizer = vosk_recognizer_new(model, SAMPLE_RATE);
    if (!recognizer) {
        fprintf(stderr, "인식기 생성 실패!\n");
        vosk_model_free(model);
        return 1;
    }

    // ALSA를 사용하여 마이크 오디오 캡처
    snd_pcm_t *pcm_handle;
    snd_pcm_open(&pcm_handle, "default", SND_PCM_STREAM_CAPTURE, 0);
    snd_pcm_set_params(pcm_handle, SND_PCM_FORMAT_S16_LE, SND_PCM_ACCESS_RW_INTERLEAVED, 1, SAMPLE_RATE, 1, 500000);

    printf("음성을 말하세요 (Ctrl+C로 종료)\n");

    char buffer[4000];
    int read_size;

    while (1) {
        read_size = snd_pcm_readi(pcm_handle, buffer, sizeof(buffer) / 2);
        if (read_size < 0) {
            snd_pcm_recover(pcm_handle, read_size, 0);
            continue;
        }

        if (vosk_recognizer_accept_waveform(recognizer, buffer, read_size * 2)) {
            const char *result = vosk_recognizer_result(recognizer);
            control_led(result);
        } else {
            printf("음성 인식 중...\n");
        }
    }

    // 리소스 해제
    snd_pcm_close(pcm_handle);
    vosk_recognizer_free(recognizer);
    vosk_model_free(model);
    gpiod_chip_close(chip);
    
    return 0;
}
