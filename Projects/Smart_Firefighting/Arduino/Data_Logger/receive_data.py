#!/usr/bin/env python

import pika
import sys
import time

# Attemps to connect to server and run data receiving loop.
# If it fails to connect to the broker, it will wait some time
# and attempt to reconnect infinitely.
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs',
                                 type='fanout')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='logs',
                           queue=queue_name)

        print ' [*] Waiting for logs. To exit press CTRL+C'

        def callback(ch, method, properties, body):
            print " [x] %r" % (body,)

        channel.basic_consume(callback,
                              queue=queue_name,
                              no_ack=True)

        channel.start_consuming()
    except:
        print "No broker found. Retrying in 5 seconds..."
        time.sleep(5)