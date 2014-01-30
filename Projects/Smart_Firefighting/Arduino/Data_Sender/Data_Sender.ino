/*
  Data Sender
  2014-01-29
  Kristopher Overholt

 Sends all standard spacebrew data types, and a custom data type.
 
 The circuit:
 - No circuit required
 
 More information about Spacebrew is available at: 
 http://spacebrew.cc/
 
 */

#include <Bridge.h>
#include <SpacebrewYun.h>

// create a variable of type SpacebrewYun and initialize it with the constructor
SpacebrewYun sb = SpacebrewYun("ArduinoPumper", "Pumper Pressure and Flow");

// create variables to manage interval between each time we send a string
long last = 0;
int interval = 1000;

int counter = 0;

int flow_rate = 0;

void setup() { 

	// start the serial port
	Serial.begin(57600);

	// for debugging, wait until a serial console is connected
	// delay(4000);
        // while (!Serial) { ; }

	// start-up the bridge
	Bridge.begin();

	// configure the spacebrew object to print status messages to serial
    // sb.verbose(true);

	// configure the spacebrew publisher and subscriber
	sb.addPublish("string test", "string");
	sb.addPublish("range test", "range");
	sb.addPublish("boolean test", "boolean");
	sb.addPublish("custom test", "crazy");
	sb.addPublish("Pump Flow Rate (gpm)", "range");
	sb.addPublish("Pump Pressure (psi)", "range");
	// sb.addSubscribe("string test", "string");
	// sb.addSubscribe("range test", "range");
	// sb.addSubscribe("boolean test", "boolean");
	// sb.addSubscribe("custom test", "crazy");

	// register the string message handler method 
	// sb.onRangeMessage(handleRange);
	// sb.onStringMessage(handleString);
	// sb.onBooleanMessage(handleBoolean);
	// sb.onCustomMessage(handleCustom);

	// connect to cloud spacebrew server at "sandbox.spacebrew.cc"
	sb.connect("192.168.1.5");

	// we give some time to arduino to connect to sandbox, otherwise the first sb.monitor(); call will give an error
	delay(1000);
} 


void loop() { 
	// monitor spacebrew connection for new data
	sb.monitor();

	// connected to spacebrew then send a string every 2 seconds
	if ( sb.connected() ) {

		// check if it is time to send a new message
		if ( (millis() - last) > interval ) {
			String test_str_msg = "testing, testing, ";
			test_str_msg += counter;
			counter ++;
            flow_rate = counter;

			sb.send("string test", test_str_msg);
			sb.send("range test", 500);
			sb.send("boolean test", true);
			sb.send("custom test", "you're loco");
			sb.send("Pump Flow Rate (gpm)", flow_rate);
			sb.send("Pump Pressure (psi)", 200);

			last = millis();

		}
	}
	delay(1000);
} 

// define handler methods, all standard data type handlers take two appropriate arguments

//void handleRange (String route, int value) {
//	Serial.print("Range msg ");
//	Serial.print(route);
//	Serial.print(", value ");
//	Serial.println(value);
//}

//void handleString (String route, String value) {
//	Serial.print("String msg ");
//	Serial.print(route);
//	Serial.print(", value ");
//	Serial.println(value);
//}

//void handleBoolean (String route, boolean value) {
//	Serial.print("Boolen msg ");
//	Serial.print(route);
//	Serial.print(", value ");
//	Serial.println(value ? "true" : "false");
//}

// custom data type handlers takes three String arguments

//void handleCustom (String route, String value, String type) {
//	Serial.print("Custom msg ");
//	Serial.print(route);
//	Serial.print(" of type ");
//	Serial.print(type);
//	Serial.print(", value ");
//	Serial.println(value);
//}

