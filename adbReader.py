import subprocess
import time

p = subprocess.Popen("adb logcat -s hubmessageparser", stdout=subprocess.PIPE)

#time.sleep(4)
#p.kill()
av_current = 0

print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
for line in iter(p.stdout.readline,''):
    if not line:
        continue
    if "BATT_CURRENT" in line.decode("utf-8"):
        output_line = line.decode("utf-8").strip()
        hex_current = output_line[-4:]
        current_mA = (65535 - int(hex_current, 16))
        print(str(current_mA*0.001) + "A")

        