#!/bin/bash

cd /home/finn/STM32-Discord-Bot/

touch print_launches_output.log

python print_launches.py >> print_launches_output.log 2>> print_launches_output.log &
