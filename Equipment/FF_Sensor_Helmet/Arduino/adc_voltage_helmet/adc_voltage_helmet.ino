#include <Wire.h>
#include <Adafruit_ADS1015.h>
#include <Bridge.h>
#include <YunServer.h>
#include <YunClient.h>

 Adafruit_ADS1115 ads;   /* Use this for the 16-bit version */
//Adafruit_ADS1015 ads;  /* Use this for the 12-bit version */

// Listen on default port 5555, the webserver on the Yun
// will forward there all the HTTP requests for us.
YunServer server;

void setup(void)
{
  // Setup Bridge (needed every time we communicate with the Arduino Yún)
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Bridge.begin();
  digitalWrite(13, HIGH);
  
  // The ADC input range (or gain) can be changed via the following
  // functions, but be careful never to exceed VDD +0.3V max, or to
  // exceed the upper and lower limits if you adjust the input range!
  // Setting these values incorrectly may destroy your ADC!
  //                                                                ADS1015  ADS1115
  //                                                                -------  -------
  // ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
  // ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
  // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
  ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
  // ads.setGain(GAIN_SIXTEEN);       // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV
  
  ads.begin();
  
  // Listen for incoming connections only from localhost
  server.listenOnLocalhost();
  server.begin();
}

void loop() {
  // Get clients connecting to the server
  YunClient client = server.accept();

  // There is a new client
  if (client) {
    // Process request
    process(client);

    // Close connection and free resourcems.
    client.stop();
  }

  delay(50); // Poll every 50 ms
}

void process(YunClient client) {
  // Read the command
  String command = client.readStringUntil('/');
    
  // "adc" command
  if (command == "adc"){
    adcCommand(client);
  }
}

void adcCommand(YunClient client) {
  int channel;
  int16_t value;
  float multiplier, voltage;

  // Read channel
  channel = client.parseInt();
  
  /* Be sure to update this value based on the IC and the gain settings! */
  // multiplier = 3.0;    /* ADS1015 @ +/- 6.144V gain (12-bit results) */
  multiplier = 0.015625;   /* ADS1115  @ +/- 1.024V gain (16-bit results) */

  if (channel == 1) {
    value = ads.readADC_Differential_0_1();
  }
  else if (channel == 2) {
    value = ads.readADC_Differential_2_3();
  }
  
  voltage = value * multiplier;

  // Send feedback to client
  client.print(voltage);

  // Update datastore key with the current channel value
  String key = "C";
  key += channel;
  Bridge.put(key, String(voltage));
}



