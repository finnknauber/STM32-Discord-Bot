#!/bin/bash

cd /home/finn/STM32-Discord-Bot/

git fetch >> output.log 2>> output.log
git checkout origin/master -- README.md >> output.log 2>> output.log
