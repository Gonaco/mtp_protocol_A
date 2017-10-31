#!/bin/bash

# gcc -Wall -W -fPIC -g -pthread message_test.c rf24.o spi.o gpio.o compatibility.o tsqueue.o queue.o rf24Stats.o -o message_test

gcc -Wall -W -fPIC -g -pthread message_test.c libraries/RF24_fergul/src/rf24.o libraries/RF24_fergul/src/spi.o libraries/RF24_fergul/src/gpio.o libraries/RF24_fergul/src/compatibility.o libraries/RF24_fergul/src/tsqueue.o libraries/RF24_fergul/src/queue.o libraries/RF24_fergul/src/rf24Stats.o -o message_test

