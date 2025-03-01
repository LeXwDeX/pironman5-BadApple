# Pironman 5 BadApple Display(Test)

Piroman 5 机箱上的小屏幕 `SSD1306_128_64` 显示`BadApple`的GIF图

目前项目代码改完了还没测试。

## Installation

For systems that don't have git, python3 pre-installed you need to install them first

```bash
sudo apt-get update
sudo apt-get install git python3 -y
```

Execute the installation script

```bash
cd ~
git clone https://github.com/LeXwDeX/pironman5-BadApple
cd ~/pironman5
sudo python3 install.py
```

## GIF图存放地址

GIF 图文件应存放在以下路径：
`/opt/pironman5/mgunnp.gif`
关闭OLED屏幕之后，可以运行test工具里的oled程序从而播放bad apple
请确保文件已正确放置在该目录下，以便程序能够正常显示。

## 备注

官方操作文档：
https://docs.sunfounder.com/projects/pironman5/en/latest/index.html
https://docs.sunfounder.com/projects/pironman5-max/en/latest/index.html

## 因为金属外壳切换为外置蓝牙处理流程（由gpt-o1模型生成，测试可靠可用）

## 在树莓派上禁用内置蓝牙并启用外置 USB 蓝牙适配器

### **前提条件**

- 已在树莓派上安装了官方推荐系统或全能模拟器系统。
- 内置蓝牙信号较弱，需要使用更强的外置蓝牙。希望禁用树莓派的内置蓝牙模块，启用外置的 USB 蓝牙适配器。
- `/boot` 分区是只读的，需要重新挂载为可读写。
- 使用 `vim` 编辑器。

---

### **步骤一：将 `/boot` 分区重新挂载为可读写**

1. **检查 `/boot` 分区的挂载点和状态**

   ```bash
   mount | grep boot
   ```

   您可能会看到类似以下的输出：

   ```
   /dev/mmcblk0p1 on /boot/firmware type vfat (ro, ...)
   ```

   这表明 `/boot/firmware` 是实际的挂载点，并且当前是只读的（`ro`）。

2. **重新挂载 `/boot` 分区为可读写**

   将 `/boot/firmware` 重新挂载为可读写：

   ```bash
   sudo mount -o remount,rw /boot/firmware
   ```

3. **验证挂载状态**

   再次检查：

   ```bash
   mount | grep boot
   ```

   现在应显示为 `rw`，表示可读写。

---

### **步骤二：禁用内置蓝牙**

1. **修改 `/boot/firmware/config.txt`**

   使用 `vim` 编辑配置文件：

   ```bash
   sudo vim /boot/firmware/config.txt
   ```

   在文件末尾添加：

   ```
   dtoverlay=disable-bt
   ```

   **说明**：`dtoverlay=disable-bt` 将禁用树莓派的内置蓝牙功能。

2. **修改 `/boot/firmware/cmdline.txt`**

   ```bash
   sudo vim /boot/firmware/cmdline.txt
   ```

   - 删除与串口通信相关的参数，如 `console=serial0,115200`。

   **注意**：`cmdline.txt` 文件内容必须在一行内，不得有换行。

3. **屏蔽蓝牙相关的内核模块（可选）**

   创建或编辑 `/etc/modprobe.d/raspi-blacklist.conf` 文件：

   ```bash
   sudo vim /etc/modprobe.d/raspi-blacklist.conf
   ```

   添加以下内容：

   ```
   blacklist btbcm
   blacklist hci_uart
   ```

   **说明**：这将屏蔽与内置蓝牙相关的内核模块，防止其加载。

4. **禁用蓝牙相关的服务**

   ```bash
   sudo systemctl disable bluetooth.service
   sudo systemctl disable hciuart.service
   ```

   **说明**：这将防止系统启动时自动加载内置蓝牙相关的服务。

5. **重启系统**

   ```bash
   sudo reboot
   ```

---

### **步骤三：验证内置蓝牙已禁用**

1. **检查蓝牙设备列表**

   ```bash
   hciconfig -a
   ```

   您不应再看到 `hci1`（内置蓝牙）设备，只剩下 `hci0`（外置 USB 蓝牙适配器）。

---

### **步骤四：启用外置 USB 蓝牙适配器**

1. **插入 USB 蓝牙适配器**

   将外置 USB 蓝牙适配器插入树莓派的 USB 接口。

2. **确认系统识别 USB 设备**

   ```bash
   lsusb
   ```

   您应能在列表中看到您的 USB 蓝牙适配器。

3. **检查蓝牙设备状态**

   ```bash
   hciconfig -a
   ```

   可能会看到 `hci0` 设备，但状态为 `DOWN`。

---

### **步骤五：解除 `rfkill` 对蓝牙的阻止**

1. **查看 `rfkill` 状态**

   ```bash
   sudo rfkill list all
   ```

   如果看到 `hci0` 的 `Soft blocked` 或 `Hard blocked` 为 `yes`，说明蓝牙设备被阻止了。

2. **解除阻止**

   ```bash
   sudo rfkill unblock bluetooth
   ```

   或解除所有设备的阻止：

   ```bash
   sudo rfkill unblock all
   ```

3. **验证解除成功**

   再次查看 `rfkill` 状态，确保 `hci0` 的 `Soft blocked` 和 `Hard blocked` 都为 `no`。

---

### **步骤六：启动外置 USB 蓝牙适配器**

1. **启动蓝牙设备**

   ```bash
   sudo hciconfig hci0 up
   ```

2. **验证设备已启动**

   ```bash
   hciconfig -a
   ```

   应显示 `hci0` 处于 `UP RUNNING` 状态。

---

### **步骤七：测试蓝牙功能**

1. **使用 `bluetoothctl` 进行测试**

   ```bash
   bluetoothctl
   ```

   在 `bluetoothctl` 交互界面中：

   - 输入 `list`，查看蓝牙控制器列表。
   - 输入 `show`，查看当前控制器信息。
   - 输入 `scan on`，开始扫描附近的蓝牙设备。
   - 输入 `devices`，查看已发现的设备列表。
   - 输入 `pair [设备MAC地址]`，与设备配对。
   - 输入 `connect [设备MAC地址]`，连接到设备。
   - 输入 `exit`，退出交互界面。

2. **验证蓝牙功能正常**

   确保您能够发现、配对和连接到蓝牙设备，证明外置 USB 蓝牙适配器工作正常。

---

### **步骤八：确保蓝牙设备在重启后依然解锁（可选）**

1. **创建系统服务**

   创建服务文件 `/etc/systemd/system/unblock-bluetooth.service`：

   ```bash
   sudo vim /etc/systemd/system/unblock-bluetooth.service
   ```

   添加以下内容：

   ```
   [Unit]
   Description=Unblock Bluetooth at startup
   After=bluetooth.service

   [Service]
   Type=oneshot
   ExecStart=/usr/sbin/rfkill unblock bluetooth

   [Install]
   WantedBy=multi-user.target
   ```

2. **启用并启动服务**

   ```bash
   sudo systemctl enable unblock-bluetooth.service
   sudo systemctl start unblock-bluetooth.service
   ```

   **说明**：这样可保证每次系统启动时，蓝牙设备都会被自动解锁。

---

### **步骤九：将 `/boot` 分区重新挂载为只读（可选）**

完成所有配置后，为了系统安全，可以将 `/boot` 分区重新挂载为只读：

```bash
sudo mount -o remount,ro /boot/firmware
```

---

### **步骤十：重启系统并验证**

1. **重启系统**

   ```bash
   sudo reboot
   ```

2. **验证配置生效**

   - **检查蓝牙设备状态**

     ```bash
     hciconfig -a
     ```

     确认只有 `hci0`（外置 USB 蓝牙适配器）存在，且处于 `UP RUNNING` 状态。

   - **测试蓝牙功能**

     使用 `bluetoothctl`，确保蓝牙功能正常。

---

### **可能的注意事项**

- **注意备份**：在修改系统配置文件前，建议备份原始文件以防止误操作。

- **权限问题**：在执行需要超级用户权限的命令时，确保使用 `sudo`。

- **系统更新**：保持系统和软件包更新，以获得最新的功能和修复：

  ```bash
  sudo apt update
  sudo apt full-upgrade
  ```

- **日志检查**：如果遇到问题，可以查看系统日志获取更多信息：

  ```bash
  sudo dmesg | grep -i bluetooth
  ```

- **内核模块兼容性**：禁用内置蓝牙可能会影响其他功能，请根据需要调整。

---

## **总结**

通过以上步骤，您已经成功地：

- 重新挂载了 `/boot` 分区为可读写，允许编辑配置文件。
- 禁用了树莓派内置的蓝牙模块，防止其干扰外置蓝牙设备。
- 解决了 `rfkill` 对外置蓝牙设备的阻止，使其能够正常工作。
- 启用了外置 USB 蓝牙适配器，并验证了其功能正常。
