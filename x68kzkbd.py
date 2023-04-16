#!/usr/bin/env python3
# pyUSB による X68000Z Keyboard LED 制御デモ
# Copyright 2023 Yuichi Nakamura (@yunkya2)

import usb.core
import time
import platform

# デモ用のLED制御パターン
# 下位から8ビットずつ、かな:ローマ字:コード入力:CAPS:INS:ひらがな:全角 LEDの輝度
demo_pattern = [
  0x00000000000000, 0x000000000000ff, 0x0000000000ffff, 0x00000000ffffff, 0x000000ffffffff, \
  0x0000ffffffffff, 0x00ffffffffffff, 0xffffffffffffff, 0xffffffffffff00, 0xffffffffff0000, \
  0xffffffff000000, 0xffffff00000000, 0xffff0000000000, 0xff000000000000, 0x00000000000000, \
  0x00000000000000, 0x10101010101010, 0x20202020202020, 0x30303030303030, 0x40404040404040, \
  0x50505050505050, 0x80808080808080, 0xf0f0f0f0f0f0f0, 0xffffffffffffff, 0xf0f0f0f0f0f0f0, \
  0x80808080808080, 0x50505050505050, 0x40404040404040, 0x30303030303030, 0x20202020202020, \
  0x10101010101010, 0x00000000000000, \
  0x00000000000010, 0x00000000001020, 0x00000000102030, 0x00000010203040, 0x00001020304050, \
  0x00102030405080, 0x102030405080f0, 0x2030405080f0ff, 0x30405080f0fff0, 0x405080f0fff080, \
  0x5080f0fff08050, 0x80f0fff0805040, 0xf0fff080504030, 0xfff08050403020, 0xf0805040302010, \
  0x80504030201000, 0x50403020100000, 0x40302010000000, 0x30201000000000, 0x20100000000000, \
  0x10000000000000, 0x00000000000000 \
]

def demo():
    dev = usb.core.find(idVendor=0x33dd, idProduct=0x0011)

    if dev is None:
        raise ValueError('Device not found')

    if platform.system() == 'Linux':
        # Linuxの場合はUSBデバイスの制御をpyUSBに移す
        if dev.is_kernel_driver_active(0):
            dev.detach_kernel_driver(0)
        if dev.is_kernel_driver_active(1):
            dev.detach_kernel_driver(1)

    dev.set_configuration()

    data = bytearray(65)
    data[0] = 10
    data[1] = 0xf8

    while True:
        for p in demo_pattern:
            n = 7
            for i in range(7):
                data[n] = p & 0xff
                p = p >> 8
                n += 1
                if n == 12:
                    n += 1
            # HIDクラスリクエスト SET_REPORT を発行
            dev.ctrl_transfer(0x21, 9, wValue=0x30a, wIndex=1, data_or_wLength=data)
            time.sleep(0.1)

if __name__ == '__main__':
    demo()
