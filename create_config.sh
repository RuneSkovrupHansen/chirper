#!/bin/bash

touch config.ini

echo [chirper] >> config.ini
echo recipient = >> config.ini
echo earliest_hour = 9 >> config.ini
echo latest_hour = 11 >> config.ini

echo "config.ini created, please overwrite default values"