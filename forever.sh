#!/bin/bash
# Script to keep codebot going forever!
while true; do
python -u codebot.py &>> log
x=$( ps -aux | grep 'codebot')
y=$(echo $x | awk '{print $16}')
wait $y
DATE=`date`
echo "Process stopped at $DATE" &>> fail_log
done
