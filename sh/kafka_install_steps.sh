#!/bin/sh
sudo su root
yum install java
yum install wget
yum install tar
useradd kafka
passwd kafka
cd /home/kafka
wget http://www-eu.apache.org/dist/kafka/0.9.0.1/kafka_2.11-0.9.0.1.tgz
tar -zxvf kafka_2.11-0.9.0.1.tgz
mv kafka_2.11-0.9.0.1/ kafka_901/
cd /home/kafka/kafka_901
bin/zookeeper-server-start.sh config/zookeeper.properties
#ctrl+z
bg
/home/kafka/kafka_901/bin/kafka-server-start.sh /home/kafka/kafka_901/config/server.properties