#!/bin/bash

cd /home/finn/STM32-Discord-Bot/

touch output.log

nohup python STM32-Discord-Bot/bot.py >> output.log 2>> output.log &
