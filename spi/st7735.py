# -*- coding: UTF-8 -*-
from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from luma.core.render import canvas
import logging
import time
from PIL import ImageFont

logging.getLogger('PIL').setLevel(logging.ERROR)

def main():
    serial = spi(port=0, device=0)
    device = st7735(serial, width=160, height=128, rotate=0, h_offset=0, v_offset=0, bgr=False)

    print(f'bounding box', device.bounding_box)
    fontSize=14
    FontTemp = ImageFont.truetype('/home/tony/spi/font/Roboto-Medium.ttf', fontSize)
    price = 0.3
    while True:
        with canvas(device) as draw:
            draw.text((0,0), "SPOT_WOO_USDC: 0.3", fill="red", font=FontTemp)
        
        time.sleep(5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass