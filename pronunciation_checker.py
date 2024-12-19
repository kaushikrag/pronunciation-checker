import streamlit as st
import random
import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
import os

# List of words to choose from
WORDS = ["apple", "banana", "cherry", "grape", "orange", "peach", "strawberry", "watermelon"]

def get_random_word():
    return random.choice(WORDS)

def record_audio(filename="audio.wav", duration=5, fs=44100):
    st.info("Recording... Please speak the word.")
    try:
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()  # Wait for the recording to finish
        write(filename, fs, audio_data)  # Save as WAV file
        st.success("Recording finished.")
        return filename
    except Exception as e:
        st.error(f"An error occurred while recording: {e}")
        return None

def recognize_speech_from_file(filename):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        st.error("Could not understand the audio. Please try again.")
        return None
    except sr.RequestError as e:
        st.error(f"Error with the recognition service: {e}")
        return None

# Streamlit app
st.title("Pronunciation Checker")
st.write("This app displays a random word and checks if you pronounce it correctly.")

if "random_word" not in st.session_state:
    st.session_state.random_word = get_random_word()

st.write(f"Your word is: **{st.session_state.random_word}**")

if st.button("Record and Check Pronunciation"):
    audio_file = record_audio()
    if audio_file:
        user_pronunciation = recognize_speech_from_file(audio_file)
        if user_pronunciation:
            st.write(f"You said: **{user_pronunciation}**")
            if user_pronunciation.lower() == st.session_state.random_word.lower():
                st.success("Correct pronunciation!")
            else:
                st.error("Incorrect pronunciation. Try again.")
        os.remove(audio_file)

if st.button("Get a New Word"):
    st.session_state.random_word = get_random_word()
    st.experimental_rerun()

st.write("**Note:** This app works best on a device with a microphone. For mobile users, open this app in your browser.")
