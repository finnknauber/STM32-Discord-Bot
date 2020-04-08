#!/bin/bash

cd /home/finn/STM32-Discord-Bot/

git add -u
git commit -m "Serverlog"
git push

send "discordstm32bot!"
