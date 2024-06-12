# -*- coding: UTF-8 -*-
from luma.core.interface.serial import spi
from luma.lcd.device import st7735
from luma.core.render import canvas
import logging
logging.getLogger('PIL').setLevel(logging.ERROR)

import time

def main():
    serial = spi(port=0, device=0)
    device = st7735(serial, width=160, height=128, rotate=2, h_offset=1, v_offset=2, bgr=True)

    print(f'bounding box', device.bounding_box)

    while True:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="red", fill="black")
            draw.text((30, 40), "hello", fill="red")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass