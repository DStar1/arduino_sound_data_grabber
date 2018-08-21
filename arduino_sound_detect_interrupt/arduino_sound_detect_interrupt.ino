extern "C" {
  #include "user_interface.h"
}

os_timer_t myTimer;
const int soundPin = A0;
long start = 0;

void timerCallback(void *pArg)
{
//  Serial.print(micros() - start);
//  Serial.print(",");
//  Serial.println(analogRead(soundPin));
  Serial.write(analogRead(soundPin));
  Serial.write("\n");
}

void timer_init(void)
{
  os_timer_setfn(&myTimer, timerCallback, NULL);
  os_timer_arm(&myTimer, 1, true); //1ms interrupt => 1000Hz
}

void setup()
{
  Serial.begin(115200);
  start = micros();
  timer_init();
}

void loop()
{
}
