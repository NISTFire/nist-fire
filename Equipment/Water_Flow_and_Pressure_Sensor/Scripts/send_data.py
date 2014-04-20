#!/usr/bin/env python

from __future__ import division

import pika
import time
import argparse
import urllib2
from math import sqrt

voltage_scaling_factor = 2.5 # psi/mV
flow_constant = 56 # 56 for 1.5 inch coupling, 143 for 2.5 inch coupling
calibration_timer = 30
retry_timer = 30

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
    voltage = float(voltage)
    return voltage


def convert_voltage(voltage, zero_voltage):
    # Convert voltage to pressure (psi)
    pressure = (voltage - zero_voltage) * voltage_scaling_factor
    return pressure


def calculate_flow_rate(pressure_1, pressure_2):
    # Calculate flow rate from pressure differential
    pressure_differential = pressure_1 - pressure_2
    try:
        flow_rate = flow_constant * sqrt(pressure_differential)
    except:
        return float('nan')
    return flow_rate

# Attemps to connect to server and run data broadcast loop.
# If it fails to connect to the broker, it will wait some time
# and attempt to reconnect indefinitely.
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=args.broker))
        channel = connection.channel()
        channel.exchange_declare(exchange='logs', type='fanout')

        # Read voltage value at zero flow/ambient pressure to calculate offset
        zero_voltage_1_list = []
        zero_voltage_2_list = []
        timer = 1
        while timer <= calibration_timer:
            # Read pressure from ADC channels
            voltage_1 = read_voltage(1)
            voltage_2 = read_voltage(2)
            zero_voltage_1_list.append(voltage_1)
            zero_voltage_2_list.append(voltage_2)

            # Construct message
            message = (time.ctime()+',%s %s (%i/%i),%0.2f,%0.2f,%0.2f,%0.2f,%0.2f') % (
                    args.logger_id, 'Calibration', timer, calibration_timer,
                    voltage_1, 0, voltage_2, 0, 0)
            channel.basic_publish(exchange='logs',
                                  routing_key='',
                                  body=message)
            print 'Sent %r' % (message)
            
            time.sleep(1)
            timer += 1

        # Calculate average of zero voltage value
        zero_voltage_1 = sum(zero_voltage_1_list) / len(zero_voltage_1_list)
        zero_voltage_2 = sum(zero_voltage_2_list) / len(zero_voltage_2_list)

        # Construct message
        message = (time.ctime()+',%s %s,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f') % (
                args.logger_id, 'Calibration complete',
                zero_voltage_1, 0, zero_voltage_2, 0, 0)
        channel.basic_publish(exchange='logs',
                              routing_key='',
                              body=message)
        print 'Sent %r' % (message)

        # Send voltage, pressure, and flow rate data
        while True:
            # Read voltage from ADC channels
            voltage_1 = read_voltage(1)
            voltage_2 = read_voltage(2)

            # Convert voltages to pressures
            pressure_1 = convert_voltage(voltage_1, zero_voltage_1)
            pressure_2 = convert_voltage(voltage_2, zero_voltage_2)

            # Calculate flow rate from pressure differential
            flow_rate = calculate_flow_rate(pressure_1, pressure_2)
            
            # Construct message for log
            message = (time.ctime()+',%s,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f') % (
                    args.logger_id, voltage_1, pressure_1, voltage_2,
                    pressure_2, flow_rate)
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
            # Read flow voltage from ADC channels
            voltage_1 = read_voltage(1)
            voltage_2 = read_voltage(2)
            # Construct message for log
            message = (time.ctime()+',%s,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f') % (
                  args.logger_id, voltage_1, 0, voltage_2, 0, 0)
            with open(args.log_file, 'a+') as text_file:
                text_file.write(message+'\n')
            time.sleep(1)
            timer += 1
