#!/bin/bash

cd /home/finn/STM32-Discord-Bot/

touch output.log

nohup python bot.py >> output.log 2>> output.log &
