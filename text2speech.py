from pathlib import Path
import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

def text_to_speech(text, voice_type="shimmer"):
  
  speech_file_path = Path(__file__).parent / "speech.mp3"
  response = client.audio.speech.create(
    model="tts-1-hd",
    voice=voice_type,
    input=text
  )

  response.stream_to_file(speech_file_path)
  return speech_file_path

def main():

  st.header("OMT Text-to-Speech")

  user_input = st.text_area("Enter text to convert to speech", max_chars=4096)
  # Voice selection dropdown
  voice_type = st.selectbox(
      "Choose the voice:",
      ["alloy", "echo", "fable", "onyx", "nova", "shimmer"])
  
  user_file_name = st.text_input("File name:")
  if not user_file_name:
    user_file_name = "speech.mp3"

  cost = 30.00 / 1000000 * len(user_input)
  string_cost = "Cost $" + str(cost)
  st.write(f":grey[{string_cost}]")

  # Convert button
  if st.button("Convert to Speech"):
    speech_file_path = text_to_speech(user_input, voice_type)
    if speech_file_path:
      # Display audio player and download link
      audio_file = open(speech_file_path, 'rb')
      audio_bytes = audio_file.read()
      st.audio(audio_bytes, format='audio/mp3')
      st.download_button(label="Download Speech",
                         data=audio_bytes,
                         file_name=user_file_name,
                         mime="audio/mp3")

if __name__ == "__main__":
  main()
