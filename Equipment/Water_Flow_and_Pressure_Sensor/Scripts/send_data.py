#!/usr/bin/env python

from __future__ import division

import pika
import time
import argparse
import urllib2

# User settings
# Flow meter is configured for 1 V = 0 gpm and 5 V = 200 gpm, or 50 gpm/V
# This is done by scaling the 4 mA to 20 mA signal using a 250 ohm resistor
voltage_scaling_factor = 50 # gpm/V
zero_voltage = 1 # V
retry_timer = 30 # s

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('broker', help='Network or IP address of message broker')
parser.add_argument('logger_id', help='Logger name or ID')
parser.add_argument('log_file', help='Location of log file')
args = parser.parse_args()


def read_voltage(channel):
    # Read voltage from specified ADC channel over REST API
    response = urllib2.urlopen('http://localhost/arduino/adc/' + str(channel))
    voltage = response.read()
    response.close()
    # Convert mV to V and round to 1 decimal place
    voltage = round(float(voltage)/1000, 1)
    return voltage


def calculate_flow_rate(voltage):
    # Calculate flow rate
    flow_rate = (voltage - zero_voltage) * voltage_scaling_factor
    return flow_rate

# Attemps to connect to server and run data broadcast loop.
# If it fails to connect to the broker, it will wait some time
# and attempt to reconnect indefinitely.
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=args.broker))
        channel = connection.channel()
        channel.exchange_declare(exchange='logs', type='fanout')

        # Send voltage and flow rate data
        while True:
            # Read voltage from ADC channel
            voltage = read_voltage(1)

            # Calculate flow rate
            flow_rate = calculate_flow_rate(voltage)
            
            # Construct message for log
            message = (time.ctime()+',%s,%0.1f,%0.1f') % (args.logger_id, voltage, flow_rate)
            channel.basic_publish(exchange='logs',
                                  routing_key='',
                                  body=message)
            print 'Sent %r' % (message)
            with open(args.log_file, 'a+') as text_file:
                text_file.write(message+'\n')
            time.sleep(1)

        connection.close()
    except:
        print 'No broker found. Retrying in 30 seconds...'
        
        timer = 0
        while timer < retry_timer:
            # Read voltage from ADC channel
            voltage = read_voltage(1)

            # Calculate flow rate
            flow_rate = calculate_flow_rate(voltage)

            # Construct message for log
            message = (time.ctime()+',%s,%0.1f,%0.1f') % (args.logger_id, voltage, flow_rate)
            with open(args.log_file, 'a+') as text_file:
                text_file.write(message+'\n')
            time.sleep(1)
            timer += 1
