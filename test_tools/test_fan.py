# Only On Raspberry Pi 5 OS
# 需要进入虚拟环境 source /opt/pironman5/venv/
from pm_auto.fan_control import FanControl

# 初始化配置
config = {
    "gpio_fan_pin": 6,  # 根据实际 GPIO 引脚设置
    "gpio_fan_mode": 1,  # 模式设置
}

# 初始化 FanControl
fan_control = FanControl(config=config, fans=["gpio_fan_state"])

# 手动关闭风扇
fan_control.off()
