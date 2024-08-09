import speech_recognition as sr
import threading
import time
from os import path
from pydub import AudioSegment 

def convert_mp3_to_wav():
    # assign files 
    input_file = "harvard.mp3"
    output_file = "harvard.wav"
    if not path.exists(output_file):
        # convert mp3 file to wav file 
        sound = AudioSegment.from_mp3(input_file)
        sound = sound.set_channels(1) # Convert to mono
        sound = sound.set_frame_rate(16000)
        sound.export(output_file, format="wav")
        print(f"Converted {input_file} to {output_file}")
    else:
        print(f"{output_file} already exists. Skipping conversion.")


def convert_wav_to_text():
    start_time = time.time()

    with sr.AudioFile("harvard.wav") as source:
        audio = sr.Recognizer().record(source)

    try:
        result = sr.Recognizer().recognize_google(audio, language="en-US")

        print("The audio file contains: " + result)
        
        with open("harvard_transcription.txt", "w") as file:
            file.write(result)
        print("Text saved to harvard_transcription.txt")
    
    except sr.UnknownValueError:
        print("could not understand the audio")
    
    except sr.RequestError as e:
        print(f"request failed; {e}")

    end_time = time.time()  # end the timer
    time_taken = end_time - start_time
    print(f"Time taken for conversion: {time_taken:.2f} seconds")

t1 = threading.Thread(target=convert_mp3_to_wav)
t2 = threading.Thread(target=convert_wav_to_text)
t1.start()
t1.join()
t2.start()
t2.join()