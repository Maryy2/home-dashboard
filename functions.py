import os
import subprocess
from dotenv import load_dotenv
from tapo import ApiClient

#check if running on Raspberry Pi
is_raspberry_pi = os.path.exists("/sys/firmware/devicetree/base/model")

#LED informations
load_dotenv()
TAPO_EMAIL = os.getenv("TAPO_EMAIL")
TAPO_PASSWORD = os.getenv("TAPO_PASSWORD")
TAPO_DEVICE_IP = os.getenv("TAPO_DEVICE_IP")

def get_temp(): 
    if is_raspberry_pi:
        temp = subprocess.check_output(["vcgencmd", "measure_temp"])
        temp = temp.decode()
        temp = temp.replace("temp=","").replace("'C\n","")
        return temp
    else:
        return "N/A"
    
async def tapo_on():
    client = ApiClient(TAPO_EMAIL, TAPO_PASSWORD)
    device = await client.p110(TAPO_DEVICE_IP)
    await device.on()

async def tapo_off():
    client = ApiClient(TAPO_EMAIL, TAPO_PASSWORD)
    device = await client.p110(TAPO_DEVICE_IP)
    await device.off()