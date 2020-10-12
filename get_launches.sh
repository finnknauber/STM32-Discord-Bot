#!/bin/bash

cd /home/finn/STM32-Discord-Bot/

touch get_launch_output.log

python get_launches.py >> get_launch_output.log 2>> get_launch_output.log &

