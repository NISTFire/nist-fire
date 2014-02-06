#!/usr/bin/env python

import pika
import sys
import time

# Attemps to connect to server and run data broadcast loop.
# If it fails to connect to the broker, it will wait some time
# and attempt to reconnect infinitely.
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='192.168.1.100'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs',
                                 type='fanout')

        while 1:
            message = ' '.join(sys.argv[1:]) or "ArduinoPumper: "+time.ctime()
            channel.basic_publish(exchange='logs',
                                  routing_key='',
                                  body=message)
            time.sleep(1)
            print " [x] Sent %r" % (message,)

        connection.close()
    except:
        print "No broker found. Retrying in 30 seconds..."
        time.sleep(5)