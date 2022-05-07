import argparse
import os
import pathlib
import subprocess
import time

parser = argparse.ArgumentParser(description="Program a controller.")
parser.add_argument("id", type=int, help="ID number of controller")

args = parser.parse_args()

con_num = args.id

ip = [192, 168, 10, 100 + con_num]
mac = [0x92, 0x44, 0x4f, 0x4d, 0x45, con_num]

def_ip = "#define IP {{{},{},{},{}}}".format(*ip)
def_mac = "#define MAC {{0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x}}}".format(*mac)

arduino_dir = os.path.join(os.getenv("programfiles(x86)"), "Arduino")


stlink_exe = os.path.join(arduino_dir, "hardware\\Arduino_STM32-master\\tools\\win\\stlink\\ST-LINK_CLI.exe")
stlink_args = ["-c", "SWD", "-P", "generic_boot20_pc13.bin", "0x8000000", "-Rst", "-Run", "-NoPrompt"]

build_temp_dir = "temp\\arduino-build"
pathlib.Path(build_temp_dir).mkdir(parents=True, exist_ok=True)
build_exe = os.path.join(arduino_dir, "arduino-builder")
build_args = [
    "-logger=machine", 
    "-hardware", os.path.join(arduino_dir, "hardware"), 
    "-hardware", os.path.join(os.getenv("localappdata"), "Arduino15\\packages"), 
    "-tools", os.path.join(arduino_dir, "tools-builder"), 
    "-tools", os.path.join(arduino_dir, "hardware\\tools\\avr"),
    "-tools", os.path.join(os.getenv("localappdata"), "Arduino15\\packages"),
    "-built-in-libraries", os.path.join(arduino_dir, "libraries"),
    "-fqbn=Arduino_STM32-master:STM32F1:genericSTM32F103C:device_variant=STM32F103C8,upload_method=STLinkMethod,cpu_speed=speed_72mhz,opt=osstd",
    "-ide-version=10812",
    "-build-path", build_temp_dir,
    "-warnings=none", 
    "-build-cache", os.path.join(os.getenv("LOCALAPPDATA", "arduino_cache_342428")), 
    "-prefs=build.warn_data_percentage=75"
    ]

arduino_exe = os.path.join(arduino_dir, "Arduino\\arduino_debug.exe")
arduino_args = ["--upload"]
arduino_file = "temp/temp.ino"
arduino_final = "stmstrand\\stmstrand.ino"

args = [stlink_exe] + stlink_args
input("Move boot0 to 1...")
subprocess.run(args, env=os.environ.copy())

with open("eepromflash\\eepromflash.ino", "r") as eeprom_file:
    with open("temp\\temp.ino", "w") as temp_file:
        temp_file.write(def_ip + "\n")
        temp_file.write(def_mac + "\n")
        for line in eeprom_file.readlines():
            if "define IP" in line or "define MAC" in line:
                continue
            temp_file.write(line)

input("Move boot0 to 0...")

## Build eeprom
args = [build_exe] + build_args + [arduino_file]
subprocess.run(args, env=os.environ.copy())

## Flash eeprom
stlink_args[3] = os.path.join(build_temp_dir, "temp.ino.bin")
args = [stlink_exe] + stlink_args
subprocess.run(args, env=os.environ.copy())


time.sleep(3)

## build final script
args = [build_exe] + build_args + [arduino_final]
subprocess.run(args, env=os.environ.copy())


## Flash final script
stlink_args[3] = os.path.join(build_temp_dir, "stmstrand.ino.bin")
args = [stlink_exe] + stlink_args
subprocess.run(args, env=os.environ.copy())