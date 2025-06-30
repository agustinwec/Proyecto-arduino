/*
    VoiceRecognition.ino
        Demonstrate the voice recognition technology.

   
  Para ejecutar la demo gratuita con un conjunto de palabras clave predefinido:
  1. Verifique y cargue el sketch GetSerialNumber.ino para obtener el número de serie de la placa (cada placa de arduino tiene un numero de serie diferente) e imprimirlo en la salida de la consola.
  2. Vaya a la página de licencias de la demo gratuita de DSpotter:
  https://tool.cyberon.com.tw/ArduinoDSpotterAuth/FDMain.php
  3. Ingrese el número de serie de la placa y haga clic en Enviar. Los datos de la licencia de la placa se mostrarán en la página web.
  4. Copie y pegue los datos de la licencia en el archivo CybLicense.h, en la carpeta de su sketch.
  5. Verifique y cargue el sketch en la placa.
  6. El reconocimiento de voz está listo.

  
*/
#include <Arduino.h>
#include <DSpotterSDK_MakerHL.h>
#include <LED_Control.h>

// The DSpotter License Data.
#include "CybLicense.h"
#define DSPOTTER_LICENSE g_lpdwLicense

// The DSpotter Keyword Model Data.
#if defined(TARGET_ARDUINO_NANO33BLE) || defined(TARGET_PORTENTA_H7) || defined(TARGET_NICLA_VISION)
// For ARDUINO_NANO33BLE and PORTENTA_H7
#include "Model_L1.h"             // The packed level one model file.
// For NANO_RP2040_CONNECT
#elif defined(TARGET_NANO_RP2040_CONNECT)
#include "Model_L0.h"             // The packed level zero model file.
#endif
#define DSPOTTER_MODEL g_lpdwModel

// The VR engine object. Only can exist one, otherwise not worked.
static DSpotterSDKHL g_oDSpotterSDKHL;

// Callback function for VR engine
// Callback function for VR engine
void VRCallback(int nFlag, int nID, int nScore, int nSG, int nEnergy)
{
  if (nFlag==DSpotterSDKHL::InitSuccess)
  {
      //ToDo
  }
  else if (nFlag==DSpotterSDKHL::GetResult)
  {
      /*
      When getting an recognition result,
      the following index and scores are also return to the VRCallback function:
          nID        The result command id
          nScore     nScore is used to evaluate how good or bad the result is.
                     The higher the score, the more similar the voice and the result command are.
          nSG        nSG is the gap between the voice and non-command (Silence/Garbage) models.
                     The higher the score, the less similar the voice and non-command (Silence/Garbage) models are.
          nEnergy    nEnergy is the voice energy level.
                     The higher the score, the louder the voice.
      */
      //ToDo
      switch(nID)
      {
          case 100:
            Serial.println("Dijiste Arduino?");
            break;
          case 10000:
            Serial.println("Se escucho abrir camara");
            break;
          case 10001:
            Serial.println("Vamos a tomar una foto");
            break;
          case 10002:
            Serial.println("Que comience la musica ");
            break;
          case 10003:
            Serial.println("Pausar la musica");
            break;
          case 10004:
            Serial.println("Canción anterior");
            break;
          case 10005:
            Serial.println("Siguiente cancion");
            break;
          default:
            break;
      }

  }
  else if (nFlag==DSpotterSDKHL::ChangeStage)
  {
      switch(nID)
      {
          case DSpotterSDKHL::TriggerStage:
            LED_RGB_Off();
            LED_BUILTIN_Off();
            break;
          case DSpotterSDKHL::CommandStage:
            LED_BUILTIN_On();
            break;
          default:
            break;
      }
  }
  else if (nFlag==DSpotterSDKHL::GetError)
  {
      if (nID == DSpotterSDKHL::LicenseFailed)
      {
          //Serial.print("DSpotter license failed! The serial number of your device is ");
          //Serial.println(DSpotterSDKHL::GetSerialNumber());
      }
      g_oDSpotterSDKHL.Release();
      while(1);//hang loop
  }
  else if (nFlag == DSpotterSDKHL::LostRecordFrame)
  {
      //ToDo
  }
}

void setup()
{
  // Init LED control
  LED_Init_All();

  // Init Serial output for show debug info
  Serial.begin(9600);
  while(!Serial);
  DSpotterSDKHL::ShowDebugInfo(true);

  // Init VR engine & Audio
  if (g_oDSpotterSDKHL.Init(DSPOTTER_LICENSE, sizeof(DSPOTTER_LICENSE), DSPOTTER_MODEL, VRCallback) != DSpotterSDKHL::Success)
    return;
}

void loop()
{
  // Do VR
  g_oDSpotterSDKHL.DoVR();
}

