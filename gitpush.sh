#!/bin/bash

cd /home/finn/STM32-Discord-Bot/

git add -u
git commit -m "Serverlog"
git push

expect "Enter passphrase for key '/home/finn/.ssh/id_rsa': "
send "discordstm32bot!"
