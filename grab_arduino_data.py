#!/Users/jchow/environments/py3_6_5/bin/python
# #### /usr/local/lib/python3.6
import  serial
import  time
import  csv

ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 115200)
# ser.open()
ser.flushInput()

while True:
    # try:
    #     # print("Trying")
    #     ser_bytes = ser.readline()
    #     print(ser_bytes)
    #     # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    #     # print(decoded_bytes)
    #     with open("test_data.csv","a") as f:
    #         writer = csv.writer(f,delimiter=' ',escapechar=' ', quoting=csv.QUOTE_NONE)#, quoting=csv.QUOTE_NONE,delimiter='|', quotechar='',escapechar='\'')
    #         writer.writerow([ser_bytes])#[time.time(),ser_bytes])#decoded_bytes])
    #         # writer.writerow(map(int, [ser_bytes]))
    # except:
    #     print("Keyboard Interrupt")
    #     break

    try:
        ser_bytes = ser.readline()
        print(ser_bytes)
        # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        # print(decoded_bytes)
        with open("test_data.csv","a") as f:
            writer = csv.writer(f,delimiter=' ',escapechar=' ', quoting=csv.QUOTE_NONE)#, quoting=csv.QUOTE_NONE,delimiter='|', quotechar='',escapechar='\'')
            writer.writerow([ser_bytes])#[time.time(),ser_bytes])#decoded_bytes])
            # writer.writerow(map(int, [ser_bytes]))
    except:
        print("Keyboard Interrupt")
        break


'''
#ARDUINO
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
'''