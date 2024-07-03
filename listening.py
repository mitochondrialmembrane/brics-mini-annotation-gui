import keyboard

def main():
    print("Program started. Listening for 'Control + Space'...")

    # Define a callback function that will be called when 'Control + Space' is pressed
    def on_activate():
        print("Control + Space detected! Exiting program...")
        exit()  # Exit the program

    # Create a hotkey that listens for 'Control + Space'
    keyboard.add_hotkey('ctrl+space', on_activate)

    # Block the program and keep it running
    keyboard.wait()

if __name__ == "__main__":
    main()
