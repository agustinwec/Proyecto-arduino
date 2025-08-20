#include <PDM.h>

#define BUFFER_SIZE 512
short sampleBuffer[BUFFER_SIZE];
volatile int samplesRead;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  PDM.onReceive(onPDMdata);
  PDM.begin(1, 16000);  // 16kHz, mono
}

void loop() {
  if (samplesRead > 0) {
    Serial.write((byte*)sampleBuffer, samplesRead * 2);  // 16-bit samples
    samplesRead = 0;
  }
}

void onPDMdata() {
  int bytesAvailable = PDM.available();
  PDM.read(sampleBuffer, bytesAvailable);
  samplesRead = bytesAvailable / 2;
}
