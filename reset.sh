#!/bin/sh
gpio -g mode 17 OUTPUT
gpio -g write 17 0
gpio -g write 17 1
