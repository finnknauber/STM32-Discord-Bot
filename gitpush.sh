#!/bin/bash

cd /home/finn/STM32-Discord-Bot/

git add -u
git commit -m "Serverlog"
git push

PS="discordstm32bot!"
install -vm700 <(echo "echo $PS") $PWD/my_pass
DISPLAY= SSH_ASKPASS=$PWD/my_pass ssh-add - && rm -v my_pass
