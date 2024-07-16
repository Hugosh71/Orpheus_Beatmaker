import streamlit as st
import replicate
import requests
import os
from datetime import datetime
import uuid

st.set_page_config(page_title="AI Music Generator", page_icon="🎵", layout="wide")

st.markdown("# 🎵 AI Music Generator")
st.markdown("## Generate music based on your inputs like mood, genre, and tempo.")

# Define the Replicate model and API key
MODEL_ENDPOINT = "riffusion/riffusion"
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]

with st.sidebar:
    st.header("Music Generation Parameters")
    prompt_text = st.text_input("Enter prompt", "saxophone solo with jazzy background")
    duration = st.slider("Duration (seconds)", min_value=5, max_value=30, value=10)
    generate_button = st.button("Generate Music")

def generate_music(prompt, duration):
    response = replicate.run(
        MODEL_ENDPOINT,
        input={"prompt": prompt, "duration": duration},
        api_token=REPLICATE_API_TOKEN
    )
    audio_url = response[0]
    return audio_url

if generate_button:
    with st.spinner('Generating your music...'):
        try:
            audio_url = generate_music(prompt_text, duration)
            st.success("Music generated successfully!")
            st.audio(audio_url, format='audio/wav')
            response = requests.get(audio_url)
            audio_data = response.content
            output_path = os.path.join("outputs", f"{uuid.uuid4()}.wav")
            with open(output_path, "wb") as f:
                f.write(audio_data)
            st.download_button(
                label="Download Music",
                data=audio_data,
                file_name=f"{uuid.uuid4()}.wav",
                mime="audio/wav"
            )
        except Exception as e:
            st.error(f"Error generating music: {e}")
