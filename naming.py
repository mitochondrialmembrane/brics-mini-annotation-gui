# pip install SpeechRecognition pygame keyboard
import os
import json
import pygame
import speech_recognition as sr
import keyboard


# Initialize Pygame for audio playback
pygame.init()
pygame.mixer.init()

def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    data_dict = {}
    for tab_type in data:
        for scene in tab_type['scenes']:            
            for activity in scene['activities']:                 
                for action in activity['actions']:
                    action_id = int(action["action_id"])
                    text = action["text"]
                    data_dict[action_id] = text
    return data_dict

def load_names(file_path):
    with open(file_path, 'r') as file:
        names = file.readlines()
    names = [name.strip() for name in names]
    return names

def play_audio(audio_file):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def record_audio(output_file):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print('Start recording...')
        audio = recognizer.listen(source)
    # print(audio)
    with open(output_file, "wb") as f:
        f.write(audio.get_wav_data())
    try:
        text = recognizer.recognize_google(audio, language = "en-US")
        return text, output_file
    except sr.UnknownValueError:
        return "Could not understand audio", output_file
    except sr.RequestError:
        return "Service unavailable", output_file

def send_control_space():
    keyboard.send("ctrl+space")

def log_video(name, output_file, log_file='video_log.txt'):
    with open(log_file, 'a') as file:
        file.write(f'{output_file}\t{name}\n')

def delete_log(log_file='video_log.txt'):
    with open(log_file, 'a') as file:
        file.write('delete' + '\n') 
           
# Main execution logic
audio_naming_file = 'audio_txt/0004_Entertaining/0020_Paying with a Puppy Dog.txt'
audio_new = 'scene19'
log_video_file = 'scene19.txt'
os.makedirs(audio_new, exist_ok=True)
input_json_file = 'script.json'
names = load_names(audio_naming_file)
data_dict = read_json(input_json_file)
ori_names_iter = iter(names)
new_names_count = 0
last_logged_name = 'None'
name = next(ori_names_iter)
action_id = int(name.split('/')[-1].split('.')[0])
while True:
    print(f"Option 1: Load the next name #{data_dict[action_id]}")
    print("Option 2: Record a new audio.")
    print(f"Option 3: Remove the last logged name: {last_logged_name}.")
    choice = input("Enter your choice (1 or 2 or 3): ")
    if choice == '1':
        play_audio(name)  # Ensure audio files match the name format
        log_video(data_dict[action_id], name, log_video_file)
        last_logged_name = data_dict[action_id]
        name = next(ori_names_iter)
        action_id = int(name.split('/')[-1].split('.')[0])
    elif choice == '2':
        new_name, output_file = record_audio(f'{audio_new}/{new_names_count}.wav')
        new_names_count += 1
        log_video(new_name, output_file, log_video_file)
        last_logged_name = new_name
    elif choice == '3':
        delete_log(log_video_file)
        last_logged_name = 'None'
    
    # input("Press Enter to continue...")  # Wait for user confirmation
    print('='*24)
    # send_control_space()  # Send ctrl+space to start video recording
