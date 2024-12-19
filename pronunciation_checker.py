import streamlit as st
import random
import speech_recognition as sr

# List of words to choose from
WORDS = ["apple", "banana", "cherry", "grape", "orange", "peach", "strawberry", "watermelon"]

def get_random_word():
    return random.choice(WORDS)

def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info("Listening... Please speak the word.")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            st.success("Audio captured. Processing...")
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            st.error("Listening timed out. Please try again.")
            return None
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
    user_pronunciation = recognize_speech()

    if user_pronunciation:
        st.write(f"You said: **{user_pronunciation}**")
        if user_pronunciation.lower() == st.session_state.random_word.lower():
            st.success("Correct pronunciation!")
        else:
            st.error("Incorrect pronunciation. Try again.")

if st.button("Get a New Word"):
    st.session_state.random_word = get_random_word()
    st.experimental_rerun()

st.write("**Note:** This app works best on a device with a microphone. For mobile users, open this app in your browser.")
