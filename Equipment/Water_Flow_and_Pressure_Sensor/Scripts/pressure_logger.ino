#include <Wire.h>
#include <Adafruit_ADS1015.h>
#include <FileIO.h>

 Adafruit_ADS1115 ads;  /* Use this for the 16-bit version */
//Adafruit_ADS1015 ads;     /* Use this for the 12-bit version */

void setup(void)
{
  // Setup Bridge (needed every time we communicate with the Arduino Yún)
  Bridge.begin();
  Serial.begin(9600);

  // Setup File IO
  FileSystem.begin();
  
  Serial.println("Getting differential reading from AIN0 (P) and AIN1 (N)");
  Serial.println("ADC Range: +/- 6.144V (1 bit = 3mV/ADS1015, 0.1875mV/ADS1115)");
  
  // The ADC input range (or gain) can be changed via the following
  // functions, but be careful never to exceed VDD +0.3V max, or to
  // exceed the upper and lower limits if you adjust the input range!
  // Setting these values incorrectly may destroy your ADC!
  //                                                                ADS1015  ADS1115
  //                                                                -------  -------
  ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
  // ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
  // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
  // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
  // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV
  
  ads.begin();
}

void loop(void)
{
  // Open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  File dataFile = FileSystem.open("/mnt/sda1/datalog.txt", FILE_APPEND);
  
  int16_t results;
  
  /* Be sure to update this value based on the IC and the gain settings! */
  //float   multiplier = 3.0F;    /* ADS1015 @ +/- 6.144V gain (12-bit results) */
  float multiplier = 0.1875F; /* ADS1115  @ +/- 6.144V gain (16-bit results) */
 
  while(true) {
    diff1 = ads.readADC_Differential_0_1();
    diff2 = ads.readADC_Differential_2_3();
  
    // Make a string that start with a timestamp for assembling the data to log:
    String dataString;
    dataString += getTimeStamp();
    dataString += ", ";
    dataString += diff1 * multiplier;
    dataString += ", ";
    dataString += diff2 * multiplier;
  
    // if the file is available, write to it:
    if (dataFile) {
      dataFile.println(dataString);
      // Print to the serial port (for diagnostics)
      Serial.println(dataString);
    }  
    // If the file isn't open, then raise an error:
    else {
      Serial.println("Error opening /mnt/sda1/datalog.txt");
    }
  
    delay(500);
  }
dataFile.close();
}

String getTimeStamp() {
  String result;
  Process time;
  // date is a command line utility to get the date and the time 
  // in different formats depending on the additional parameter 
  time.begin("date");
  time.addParameter("+%D %T");  // parameters: D for the complete date mm/dd/yy
                                //             T for the time hh:mm:ss    
  time.run();  // run the command

  // read the output of the command
  while(time.available()>0) {
    char c = time.read();
    if(c != '\n')
      result += c;
  }

  return result;
}

