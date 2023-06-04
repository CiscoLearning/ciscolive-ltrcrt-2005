#!/usr/bin/env bash

# Script to fast-forward lab solutions to prepare for the next task, if not
# all steps were completed.

TASK_NAME=tickets

SOURCE_DIR=~/ciscolive-ltrcrt-2005/code/solutions/fastforward
TARGET_DIR=~/event-lab
TARGET_FILE=main.py

SOURCE_FILE=${TASK_NAME}-${TARGET_FILE}

echo -n "Copying updated main.py to the working directory..."
cp -f ${SOURCE_DIR}/${SOURCE_FILE} ${TARGET_DIR}/${TARGET_FILE}
if [ "x${?}" = "x0" ]; then
  echo "OK"
else
  echo "Problem"
  echo "There was a problem copying the updated main.py file. Please ask "
  echo "your instructor for assistance."
fi
