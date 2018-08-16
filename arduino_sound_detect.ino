const int ledPin = 13; //the led attach to 
const int soundPin = A0;

unsigned long start = 0;
String string1 = "";
void setup()
{
pinMode(ledPin,OUTPUT);
Serial.begin(115200);
start = micros();
}

void loop()
{
int value = analogRead(soundPin);
Serial.print(micros()-start);
Serial.print(',');

//string1 = start+","+value;
//Serial.println(string1);
Serial.println(value);
//if(value > 30)
//{
//digitalWrite(ledPin,HIGH);
//delay(200);
//}
//else
//{
//digitalWrite(ledPin,LOW);
//}
}