#!/bin/bash

# 检查是否提供了参数
if [ -z "$1" ]; then
  echo "Usage: $0 [0|1|2|3|4]"
  echo "0: Always On"
  echo "1: Performance"
  echo "2: Cool"
  echo "3: Balanced"
  echo "4: Quiet (default)"
  exit 1
fi

# 设置风扇模式
FAN_MODE=$1

# 检查参数是否有效
if [[ "$FAN_MODE" =~ ^[0-4]$ ]]; then
  echo "Setting fan mode to $FAN_MODE"
  sudo pironman5 -gm $FAN_MODE
else
  echo "Invalid argument: $FAN_MODE"
  echo "Usage: $0 [0|1|2|3|4]"
  echo "0: Always On"
  echo "1: Performance"
  echo "2: Cool"
  echo "3: Balanced"
  echo "4: Quiet (default)"
  exit 1
fi
