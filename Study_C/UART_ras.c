#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>

#define UART_DEV "/dev/serial0"  // 라즈베리파이의 UART 포트

int main() {
    int uart_fd;
    struct termios options;
    
    // UART 장치 열기
    uart_fd = open(UART_DEV, O_RDWR | O_NOCTTY | O_NDELAY);
    if (uart_fd == -1) {
        perror("UART 장치 열기 실패");
        return 1;
    }

    // UART 설정 가져오기
    tcgetattr(uart_fd, &options);
    cfsetispeed(&options, B9600);  // 수신 속도 설정
    cfsetospeed(&options, B9600);  // 송신 속도 설정
    options.c_cflag = CS8 | CLOCAL | CREAD;  // 8비트 데이터, 로컬 연결, 읽기 활성화
    options.c_iflag = IGNPAR;  // 패리티 없음
    tcsetattr(uart_fd, TCSANOW, &options);  // 설정 적용

    // 송신 (PC 터미널에 "Hello from Raspberry Pi" 출력)
    char tx_buffer[] = "Hello from Raspberry Pi!\n";
    write(uart_fd, tx_buffer, sizeof(tx_buffer));

    // 수신 (데이터가 도착할 때까지 대기)
    char rx_buffer[256];
    int rx_length = read(uart_fd, rx_buffer, sizeof(rx_buffer) - 1);
    if (rx_length > 0) {
        rx_buffer[rx_length] = '\0';  // 문자열 종료 문자 추가
        printf("Received: %s\n", rx_buffer);
    } else {
        printf("데이터 수신 실패\n");
    }

    // UART 장치 닫기
    close(uart_fd);
    return 0;
}
