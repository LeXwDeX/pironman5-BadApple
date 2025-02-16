# 在 Pironman5 Case 下 Lakka OS 风扇控制

本文档总结了配置 GPIO 6 控制风扇默认状态的操作步骤，确保风扇在两种系统下默认关闭（低电平）。

---

## 目标

配置 GPIO 6 控制风扇默认状态，确保其在任何操作系统下默认关闭（低电平）。

---

## 操作步骤

### 1. 将 `/flash` 挂载为可写
Lakka 的 `/flash` 目录默认是只读的。为了进行修改，需要将其挂载为可写：
```bash
mount -o remount,rw /flash
```

---

### 2. 创建自定义设备树覆盖文件
创建一个设备树覆盖文件，将 GPIO 6 设置为输出模式并驱动为低电平。

#### 设备树源文件 (`gpio_default.dts`)：
```dts
/dts-v1/;
/plugin/;

/ {
    fragment@0 {
        target = <&gpio>;
        __overlay__ {
            gpio_default: gpio_default {
                brcm,pins = <6>;
                brcm,function = <1>;  // 输出模式
                brcm,pull = <0>;      // 无上下拉
            };
        };
    };
};
```

#### 编译设备树覆盖文件：
```bash
dtc -@ -I dts -O dtb -o gpio_default.dtbo gpio_default.dts
```

#### 将编译后的文件复制到 `/flash/overlays/`：
```bash
cp gpio_default.dtbo /flash/overlays/
```

---

### 3. 修改 `/flash/config.txt`
在 `[all]` 部分添加以下内容：
```txt
dtoverlay=gpio-fan,gpiopin=6,temp=60000
dtoverlay=gpio_default
```
- `gpio-fan`：将 GPIO 6 配置为风扇控制引脚，当温度超过 60°C 时开启风扇。
- `gpio_default`：将 GPIO 6 默认设置为低电平（关闭风扇）。

---

### 4. 重启系统
使用以下命令重启系统以应用更改：
```bash
reboot
```

---

### 5. 验证配置
重启后，使用以下命令验证配置是否生效：

#### 检查设备树覆盖是否加载：
```bash
dmesg | grep gpio
```

#### 检查 GPIO 6 的状态：
```bash
cat /sys/class/gpio/gpio6/value
```

---

## 结果

风扇的默认状态已成功配置为关闭（低电平），在 Lakka 系统下均可生效。

---

## 注意事项

- 修改完成后，将 `/flash` 挂载回只读模式：
  ```bash
  mount -o remount,ro /flash
  ```
- 如果需要进一步调整，请重复上述步骤。
