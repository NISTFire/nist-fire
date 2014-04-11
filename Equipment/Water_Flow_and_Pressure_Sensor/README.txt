Arduino Config, Setup, and Data Logging

The Arduinos record voltage data locally, and they transmit voltage data to the host computer via the AMQP messaging protocol. The host computer uses RabbitMQ to act as a broker. Python scripts and the pika module send and receive AMQP messages. The following steps setup the host computer and Arduinos for this purpose.
Server (Host Computer)

Note: the following assumes that the server/host computer’s address is 192.168.1.100. It’s best to configure the host computer with a static IP address using static DHCP or manually.

Host Computer (RabbitMQ)

1) Install RabbitMQ for your platform and start the RabbitMQ server (./sbin/rabbitmq-server on Mac or Linux).

https://www.rabbitmq.com/

2) Copy the receive_data.py script from the NIST-FIRE repository to the data logging computer.

https://code.google.com/p/nist-fire/source/browse/trunk#trunk%2FProjects%2FSmart_Firefighting%2FArduino

3) Install Python (Anaconda from Continuum Analytics is recommended)

4) Install the pika module for Python using

pip install pika

5) Run the receive_data.py script as

python receive_data.py 192.168.1.100 output.csv

Host Computer (NTP Time Server)

On Windows, download and install the NTP server

http://www.meinbergglobal.com/english/sw/ntp.htm

Mac and Linux use NTP natively.

Client (Arduino)

Install Bridge Sketch on the Arduino

1) Install Arduino IDE

http://arduino.cc/

2) Plug the Arduino Yun into the USB port of the host computer.

3) Set the Tools > Board to Arduino Yun and the Tools > Port to the /dev/ttyusbmodemXXXXXX setting that matches the plugged-in Arduino.

4) Using the Arduino IDE, install the Bridge sketch on Arduino from File > Examples > Bridge > Bridge. This enables the reading and writing of data from pins using the REST API on the Arduino.

Configure the Arduino

1) Unplug the Arduino from the computer, and power on the Arduino from the battery.

2) Connect to the Arduino WiFi network. Access the Arduino web interface (http://arduino.local) with the default password of “arduino”. Set the Arduino name (referred to as <arduino_name> in the following steps), time zone, and WiFi network information on the Arduino web config. Also, set the “REST API Access” to be “Open”.

3) SSH to the Arduino at root@<arduino_name>.local and install the SFTP server, ntpclient, pip, and pika (for AMQP) on the Arduino

opkg update
opkg install openssh-sftp-server ntpclient distribute python-openssl
easy_install pip
pip install pika

4) By default, the microSD card on the Arduino is mounted at /mnt/sda1. Copy the send_data.py script from the NIST-FIRE repository to /mnt/sda1 on the Arduino.

https://code.google.com/p/nist-fire/source/browse/trunk#trunk%2FProjects%2FSmart_Firefighting%2FArduino

5) Go to System > Startup > Local Startup in the Arduino web config and add a startup line to the Local Config section (/etc/rc.local)

python /mnt/sda1/send_data.py 192.168.1.100 <arduino_name> /mnt/sda1/output.csv

6) The default NTP service is not very robust, so we will replace it with ntpclient and have it sync with the NTP server every 2 minutes. Disable the default NTP service using

/etc/init.d/sysntpd disable

Configure the ntpclient service by editing /etc/config/ntpclient to be

config ntpserver
        option hostname '192.168.1.100'
        option port     '123'

config ntpserver
        option hostname '0.pool.ntp.org'
        option port     '123'

config ntpserver
        option hostname '1.pool.ntp.org'
        option port     '123'

config ntpserver
        option hostname '2.pool.ntp.org'
        option port     '123'

config ntpserver
        option hostname '3.pool.ntp.org'
        option port     '123'

config ntpdrift                                 
        option freq     '0'                     
                                                
config ntpclient                                
        option interval 120

7) Reset power to the Arduino, and then it should start broadcasting data values within about 2 minutes of booting.

