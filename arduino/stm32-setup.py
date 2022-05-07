import argparse
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


stlink_exe = "C:\\Program Files (x86)\\Arduino\\hardware\\Arduino_STM32-master\\tools\\win\\stlink\\ST-LINK_CLI.exe"
stlink_args = ["-c", "SWD", "-P", "generic_boot20_pc13.bin", "0x8000000", "-Rst", "-Run"]

build_exe = "C:\\Program Files (x86)\Arduino\\arduino-builder"
build_args = [
    "-logger=machine", 
    "-hardware", "C:\\Program Files (x86)\\Arduino\\hardware", 
    "-hardware", "C:\\Users\\redsw\\AppData\\Local\\Arduino15\\packages", 
    "-hardware", "C:\\Users\\redsw\\OneDrive\\Documents\\Arduino\\hardware", 
    "-tools", "C:\\Program Files (x86)\\Arduino\\tools-builder", 
    "-tools", "C:\\Program Files (x86)\\Arduino\\hardware\\tools\\avr",
    "-tools", "C:\\Users\\redsw\\AppData\\Local\\Arduino15\\packages",
    "-built-in-libraries", "C:\\Program Files (x86)\\Arduino\\libraries",
    "-libraries", "C:\\Users\\redsw\\OneDrive\\Documents\\Arduino\\libraries",
    "-fqbn=Arduino_STM32-master:STM32F1:genericSTM32F103C:device_variant=STM32F103C8,upload_method=STLinkMethod,cpu_speed=speed_72mhz,opt=osstd",
    "-ide-version=10812",
    "-build-path", "C:\\Workspace\\rgbdome\\arduino\\temp\\arduino-build",
    "-warnings=none", 
    "-build-cache", "C:\\Users\\redsw\\AppData\\Local\\Temp\\arduino_cache_342428", 
    "-prefs=build.warn_data_percentage=75"
    ]

arduino_exe = "C:\\Program Files (x86)\\Arduino\\arduino_debug.exe"
arduino_args = ["--upload"]
arduino_file = "temp/temp.ino"
arduino_final = "stmstrand\\stmstrand.ino"

args = [stlink_exe] + stlink_args
input("Move boot0 to 1...")
subprocess.run(args)

with open("eepromflash\\eepromflash.ino", "r") as eeprom_file:
    with open("temp\\temp.ino", "w") as temp_file:
        temp_file.write(def_ip + "\n")
        temp_file.write(def_mac + "\n")
        for line in eeprom_file.readlines():
            if "define IP" in line or "define MAC" in line:
                continue
            temp_file.write(line)

input("Move boot0 to 0...")

## Flash eeprom
args = [arduino_exe] + arduino_args + [arduino_file]
subprocess.run(args)

time.sleep(3)

## Flash final script
args = [arduino_exe] + arduino_args + [arduino_final]
subprocess.run(args)