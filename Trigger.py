import keyboard
import subprocess

def execute_command(e):

    if e.event_type == keyboard.KEY_DOWN and keyboard.is_pressed('Ctrl+Shift+F'):
        print("Ctrl+Shift+F was pressed.")
        # Command to execute
        command = "python CaptureImproved.py"
        
        # Run the command using subprocess
        subprocess.run(command, shell=True)

keyboard.hook(execute_command)
print("Listening for Ctrl+Shift+F. Press it to execute the command.")

# Keep the program running to listen to the hotkey
keyboard.wait('esc')
