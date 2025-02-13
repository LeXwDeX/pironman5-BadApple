# 需要进入虚拟环境 source /opt/pironman5/venv/
from pm_auto.oled import OLED

def main():
    oled = OLED()
    if oled.is_ready():
        print("OLED is ready")
        oled.display_gif("/opt/pironman5/mgunnp.gif")
    else:
        print("OLED is not ready")

if __name__ == "__main__":
    main()
