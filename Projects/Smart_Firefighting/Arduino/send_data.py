#!/usr/bin/env python

from __future__ import division

import pika
import time
import argparse
import urllib2
import re


def read_value(pin):
    # Read voltage from specified analog pin over REST API
    response = urllib2.urlopen('http://localhost/arduino/analog/' + str(pin))
    value = response.read()
    value = re.findall('\d+', value)
    response.close()
    return float(value[1])

def read_flow_rate(pin):
    # Read voltage from specified analog pin
    value = read_value(pin)
    # Scale reading of 0-1023 to 0-5 V range
    voltage = value * (5 / 1023)
    # Convert voltage to flow rate (gpm)
    flow_rate = 141.36*voltage**3 - 1657.6*voltage**2 + 6654.5*voltage - 9072
    return voltage, flow_rate

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('broker', help='Network or IP address of message broker')
parser.add_argument('logger_id', help='Logger name or ID')
parser.add_argument('log_file', help='Location of log file')
args = parser.parse_args()

# Attemps to connect to server and run data broadcast loop.
# If it fails to connect to the broker, it will wait some time
# and attempt to reconnect infinitely.
while True:
    try:
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=args.broker))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs',
                                 type='fanout')

        while True:
            # Read flow rate from pin 0
            voltage, flow_rate = read_flow_rate(0)
            # Construct message for log
            message = (time.ctime()+',%s,%0.2f,%0.2f') % (args.logger_id, voltage, flow_rate)
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
        retry_value = 30
        while timer < retry_value:
            # Read flow rate from pin 0
            voltage, flow_rate = read_flow_rate(0)
            # Construct message for log
            message = (time.ctime()+',%s,%0.2f,%0.2f') % (args.logger_id, voltage, flow_rate)
            with open(args.log_file, 'a+') as text_file:
                text_file.write(message+'\n')
            time.sleep(1)
            timer += 1