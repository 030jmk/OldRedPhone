#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import subprocess
import os
import random

# Pin definitions
pulse_input_pin = 3
switch_hook_pin = 26

# Duration for counting pulses (in seconds)
pulse_count_duration = 5

# Initialize variables
pulse_count = 0
last_call_completed = True

# GPIO setup
def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pulse_input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(switch_hook_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print("GPIO setup complete")

def count_pulses(duration):
    global pulse_count
    pulse_count = 0
    end_time = time.time() + duration
    last_state = GPIO.input(pulse_input_pin)
    
    subprocess.run(["play", "-q", "AfterTheBeep.wav", "-t", "alsa"])  # Play before capturing pulses

    while time.time() < end_time:
        current_state = GPIO.input(pulse_input_pin)
        if current_state == GPIO.LOW and last_state == GPIO.HIGH:
            pulse_count += 1
            print(f"Pulse detected. Count: {pulse_count}")
        last_state = current_state
        time.sleep(0.01)  # Short sleep to prevent CPU overuse

    subprocess.run(["play", "-q", "AfterTheBeep.wav", "-t", "alsa"])  # Play after capturing pulses

def play_random_file_from_folder(folder):
    files = os.listdir(folder)
    if files:
        file_to_play = os.path.join(folder, random.choice(files))
        subprocess.run(["play", "-q", file_to_play, "-t", "alsa"])
    else:
        print(f"No files found in folder {folder}")

def main_loop():
    global last_call_completed
    try:
        while True:
            switch_hook_state = GPIO.input(switch_hook_pin)
            if switch_hook_state == GPIO.LOW and last_call_completed:  # Phone is lifted and last call was completed
                print("Switch hook is lifted")
                subprocess.run(["play", "-q", "dual_tone.wav", "-t", "alsa"])  # Play dual tone
                count_pulses(pulse_count_duration)  # Use the variable for duration
                print(f"Number of pulses captured: {pulse_count}")
                
                # Determine folder based on pulse count
                folder_name = str(pulse_count) if pulse_count > 0 else "0"
                if os.path.isdir(folder_name):
                    play_random_file_from_folder(folder_name)
                else:
                    print(f"Folder {folder_name} does not exist")
                
                subprocess.run(["play", "-q", "Gassenbesetztton.wav", "-t", "alsa"])  # Play Gassenbesetztton
                last_call_completed = False
            elif switch_hook_state == GPIO.HIGH:  # Switch hook is down
                print("Switch hook is down")
                last_call_completed = True
            else:
                print("Waiting for switch hook to be replaced")
            time.sleep(1)  # Check switch hook every second
    except KeyboardInterrupt:
        print("\nExiting gracefully")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    setup_gpio()
    main_loop()
