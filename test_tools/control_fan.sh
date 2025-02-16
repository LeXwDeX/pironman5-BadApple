#!/bin/bash

# Raspberry Pi 5 + Pironman5 RGB Fan Control Script
# 检查是否提供了参数
if [ -z "$1" ]; then
  echo "Usage: $0 [on|off]"
  exit 1
fi

# 设置 GPIO 引脚编号
GPIO_PIN=6

# 根据参数设置 GPIO 状态
if [ "$1" == "on" ]; then
  echo "Turning fan ON (GPIO $GPIO_PIN HIGH)"
  sudo pinctrl set $GPIO_PIN op dh
elif [ "$1" == "off" ]; then
  echo "Turning fan OFF (GPIO $GPIO_PIN LOW)"
  sudo pinctrl set $GPIO_PIN op dl
else
  echo "Invalid argument: $1"
  echo "Usage: $0 [on|off]"
  exit 1
fi
