/*
 * The MySensors Arduino library handles the wireless radio link and protocol
 * between your home built sensors/actuators and HA controller of choice.
 * The sensors forms a self healing radio network with optional repeaters. Each
 * repeater and gateway builds a routing tables in EEPROM which keeps track of the
 * network topology allowing messages to be routed to nodes.
 *
 * Created by Henrik Ekblad <henrik.ekblad@mysensors.org>
 * Copyright (C) 2013-2017 Sensnology AB
 * Full contributor list: https://github.com/mysensors/Arduino/graphs/contributors
 *
 * Documentation: http://www.mysensors.org
 * Support Forum: http://forum.mysensors.org
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * version 2 as published by the Free Software Foundation.
 */


#ifndef MyCapabilities_h
#define MyCapabilities_h

// Remote reset
#if defined(MY_DISABLE_REMOTE_RESET)
#define MY_CAP_RESET "N"
#else
#define MY_CAP_RESET "R"
#endif

// OTA firmware uodate feature
#if defined(MY_OTA_FIRMWARE_FEATURE)
#define MY_CAP_OTA_FW "O"
#else
#define MY_CAP_OTA_FW "N"
#endif

// Transport
#if defined(MY_RADIO_NRF24) || defined(MY_RADIO_NRF5_ESB)
#define MY_CAP_RADIO "N"
#elif defined(MY_RADIO_RFM69)
#if !defined(MY_RFM69_NEW_DRIVER)
// old RFM69 driver
#define MY_CAP_RADIO "R"
#else
// new RFM69 driver
#define MY_CAP_RADIO "P"
#endif
#elif defined(MY_RADIO_RFM95)
#define MY_CAP_RADIO "L"
#elif defined(MY_RS485)
#define MY_CAP_RADIO "S"
#else
#define MY_CAP_RADIO "-"
#endif

// Node type
#if defined(MY_GATEWAY_FEATURE)
#define MY_CAP_TYPE "G"
#elif defined(MY_REPEATER_FEATURE)
#define MY_CAP_TYPE "R"
#elif defined(MY_PASSIVE_NODE)
#define MY_CAP_TYPE "P"
#else
#define MY_CAP_TYPE "N"
#endif

// Architecture
#if defined(ARDUINO_ARCH_SAMD)
#define MY_CAP_ARCH "S"
#elif defined(ARDUINO_ARCH_NRF5)
#define MY_CAP_ARCH "N"
#elif defined(ARDUINO_ARCH_ESP8266)
#define MY_CAP_ARCH "E"
#elif defined(ARDUINO_ARCH_AVR)
#define MY_CAP_ARCH "A"
#elif defined(ARDUINO_ARCH_STM32F1)
#define MY_CAP_ARCH "F"
#elif defined(__arm__) && defined(TEENSYDUINO)
#define MY_CAP_ARCH "T"
#elif defined(__linux__)
#define MY_CAP_ARCH "L"
#else
#define MY_CAP_ARCH "-"
#endif

// Signing
#if defined(MY_SIGNING_ATSHA204)
#define MY_CAP_SIGN "A"
#elif defined(MY_SIGNING_SOFT)
#define MY_CAP_SIGN "S"
#else
#define MY_CAP_SIGN "-"
#endif

// RX queue
#if defined(MY_RX_MESSAGE_BUFFER_FEATURE)
#define MY_CAP_RXBUF "Q"
#else
#define MY_CAP_RXBUF "-"
#endif

// Radio encryption
#if defined(MY_RF24_ENABLE_ENCRYPTION) || defined(MY_RFM69_ENABLE_ENCRYPTION)
#define MY_CAP_ENCR "X"
#else
#define MY_CAP_ENCR "-"
#endif


#define MY_CAPABILITIES MY_CAP_RESET MY_CAP_RADIO MY_CAP_OTA_FW MY_CAP_TYPE MY_CAP_ARCH MY_CAP_SIGN MY_CAP_RXBUF MY_CAP_ENCR

#endif /* MyCapabilities_h */
