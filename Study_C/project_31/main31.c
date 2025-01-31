// sudo apt install -y libasound2-dev alsa-utils sox ffmpeg
// wget https://alphacephei.com/vosk/models/vosk-model-small-ko-0.22.zip
// unzip vosk-model-small-ko-0.22.zip
// mv vosk-model-small-ko-0.22 model

// git clone https://github.com/alphacep/vosk-api
// cd vosk-api/src
// make -j4
// cd ..  

// 빌드 후 src/ 폴더 안에 libvosk.so 파일이 생성

// gcc -o speech_recognition speech_recognition.c -Ivosk-api/src -Lvosk-api/src -lvosk -lasound -lm

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <alsa/asoundlib.h>
#include "vosk_api.h"  // Vosk 라이브러리

#define SAMPLE_RATE 16000  // 오디오 샘플링 레이트

int main() {
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
            printf("You said: %s\n", vosk_recognizer_result(recognizer));
        } else {
            printf("Partial: %s\n", vosk_recognizer_partial_result(recognizer));
        }
    }

    snd_pcm_close(pcm_handle);
    vosk_recognizer_free(recognizer);
    vosk_model_free(model);
    
    return 0;
}
