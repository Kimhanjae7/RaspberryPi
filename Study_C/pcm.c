#include <stdint.h>  // 표준 정수형 정의
#include <avr/io.h>  // ATmega 시리즈의 레지스터 정의
#include <util/delay.h>  // 딜레이 함수 사용

#define MOTOR_PWM_PIN PD6  // PWM 신호를 출력할 핀 (Arduino Uno의 D6 핀)
#define PWM_MAX 255        // PWM 최대값 (8비트)
#define PWM_MIN 0          // PWM 최소값

void pwm_init() {
    // 타이머0을 PWM 모드로 설정 (Fast PWM, Non-Inverting Mode)
    TCCR0A |= (1 << WGM01) | (1 << WGM00);  // Fast PWM 모드 설정
    TCCR0A |= (1 << COM0A1);  // Non-Inverting 모드 (0에서 PWM 출력)

    // 타이머 클럭 설정 (분주비 64, 16MHz / 64 = 250kHz)
    TCCR0B |= (1 << CS01) | (1 << CS00);  

    // PWM 핀을 출력으로 설정
    DDRD |= (1 << MOTOR_PWM_PIN);
}

void set_motor_speed(uint8_t speed) {
    OCR0A = speed;  // PWM 듀티 사이클 변경
}

int main() {
    pwm_init();  // PWM 초기화

    while (1) {
        for (uint8_t speed = PWM_MIN; speed <= PWM_MAX; speed += 5) {
            set_motor_speed(speed);  // 점점 빠르게
            _delay_ms(50);
        }

        for (uint8_t speed = PWM_MAX; speed >= PWM_MIN; speed -= 5) {
            set_motor_speed(speed);  // 점점 느리게
            _delay_ms(50);
        }
    }
}
