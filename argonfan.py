#!/usr/bin/env python3
import sys, smbus, argparse
import time as t
bus = smbus.SMBus(1)
address=0x1a # address set for a fan in ArgonOne case for Raspberry Pi4

def set_values():
    parser = argparse.ArgumentParser(
        description="Powers Argon One case fan as requested.")
    parser.add_argument('-t', metavar='seconds',
                        help='''Number of seconds to power fan. Limited tp 600. 
                        Use -t 0 to shutdown fan''',
                        type=int, default=30)
    parser.add_argument('-s', metavar='speed',
                        type=int, default=50,
                        help='Fan speed in range 1-100.')
    args = parser.parse_args()
    if 0 > args.s or args.s > 100:
        print("Provided speed is not in allowed range. Setting to 50")
        args.s = 50
    return (args.s, args.t)

def power_fan(speed, time):
    try:
        bus.write_byte(address, speed)
        t.sleep(time)
        bus.write_byte(address, 0)
    except KeyboardInterrupt:
        bus.write_byte(address, 0)
        sys.exit()

if __name__ == '__main__':
    speed, time = set_values()
    if time == 0:
        print('Switching fan off...')
    else:
        print(f'Starting fan at {speed}%, for {time} seconds...')
    power_fan(speed, time)
    sys.exit()
