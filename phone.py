#!/usr/bin/python3
import subprocess
import RPi.GPIO as GPIO
import time
import os
import random

# Pin definitions
pulse_input_pin = 3
switch_hook_pin = 26

# Initialize variables
pulse_count = 0
last_pulse_time = 0
dialing_timeout = 5  # 5 seconds timeout
last_switch_hook_state = GPIO.LOW  # Assume the hook is down initially
last_pulse_state = GPIO.LOW

# GPIO setup
def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pulse_input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(switch_hook_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print("GPIO setup complete")

def play_random_file(number):
    folder_path = f"./{number}"  # Assuming folders are in the same directory as the script
    if os.path.exists(folder_path):
        audio_files = [f for f in os.listdir(folder_path) if f.endswith('.mp3') or f.endswith('.wav')]
        if audio_files:
            random_file = random.choice(audio_files)
            file_path = os.path.join(folder_path, random_file)
            print(f"Playing file: {file_path}")
            subprocess.run(["play", "-q", file_path])
        else:
            print(f"No audio files found in folder {number}")
    else:
        print(f"Folder {number} does not exist")

# Main loop
def main_loop():
    global pulse_count, last_pulse_time, last_switch_hook_state, last_pulse_state
    
    try:
        while True:
            current_switch_hook_state = GPIO.input(switch_hook_pin)
            current_pulse_state = GPIO.input(pulse_input_pin)
            
            # Check if switch hook state has changed
            if current_switch_hook_state != last_switch_hook_state:
                if current_switch_hook_state == GPIO.HIGH:
                    print("Switch hook lifted")
                    pulse_count = 0
                    last_pulse_time = time.time()
                else:
                    print("Switch hook replaced")
                    if pulse_count > 0:
                        print(f"\nNumber dialed: {pulse_count}")
                        play_random_file(pulse_count if pulse_count < 10 else 0)
                    pulse_count = 0
                last_switch_hook_state = current_switch_hook_state

            # Check for pulse (falling edge)
            if current_pulse_state == GPIO.LOW and last_pulse_state == GPIO.HIGH:
                current_time = time.time()
                if current_time - last_pulse_time > 0.05:  # Debounce
                    pulse_count += 1
                    print(f"Pulse detected. Count: {pulse_count}")
                    last_pulse_time = current_time
            last_pulse_state = current_pulse_state

            # If the hook is lifted, check for timeout
            if current_switch_hook_state == GPIO.HIGH and pulse_count > 0:
                current_time = time.time()
                time_left = max(0, dialing_timeout - (current_time - last_pulse_time))
                if time_left > 0:
                    print(f"Time left: {time_left:.1f} seconds", end='\r')
                else:
                    print(f"\nDialing timeout reached. Number dialed: {pulse_count}")
                    play_random_file(pulse_count if pulse_count < 10 else 0)
                    pulse_count = 0

            time.sleep(0.01)  # Short sleep to prevent CPU overuse
    except KeyboardInterrupt:
        print("\nExiting gracefully")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    setup_gpio()
    main_loop()
