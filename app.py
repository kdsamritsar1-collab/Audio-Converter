import streamlit as st
from pydub import AudioSegment, effects
import numpy as np
import matplotlib.pyplot as plt
import io
import os

st.set_page_config(page_title="Ruhani Pro Editor", layout="wide")

# Professional Dark Theme
st.markdown("""
    <style>
    .main { background-color: #121212; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #1DB954; color: white; border: none; height: 50px; font-weight: bold; }
    .waveform-container { border: 1px solid #333; border-radius: 10px; padding: 10px; background: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Ruhani Advanced Audio Studio")

uploaded_file = st.file_uploader("Upload Audio", type=['mp3', 'wav', 'm4a'], label_visibility="collapsed")

if uploaded_file:
    # --- FILE NAME LOGIC ---
    base_name = os.path.splitext(uploaded_file.name)[0]
    final_filename = f"{base_name}_wav.wav"

    # 1. Load Audio
    audio = AudioSegment.from_file(uploaded_file)
    duration = len(audio) / 1000.0
    
    # 2. Waveform Visual
    st.subheader(f"📊 Editing: {uploaded_file.name}")
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2: samples = samples.reshape((-1, 2))[:, 0]
    
    with st.container():
        st.markdown('<div class="waveform-container">', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(15, 3))
        time_axis = np.linspace(0, duration, len(samples[::200]))
        ax.fill_between(time_axis, samples[::200], color='#1DB954', alpha=0.8)
        ax.set_xlim(0, duration)
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        ax.grid(color='#333', linestyle='--', linewidth=0.5)
        ax.tick_params(colors='white')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Precision Slider
    trim_range = st.slider("↔️ Drag to Select Trim Area", 0.0, float(duration), (0.0, float(duration)), step=0.01)
    start_s, end_s = trim_range
    
    st.write("---")

    # 4. Effects & Processing
    col_play, col_effects = st.columns([1, 1])
    
    with col_play:
        st.write("### 🎮 Preview")
        preview_audio = audio[start_s*1000 : end_s*1000]
        p_buffer = io.BytesIO()
        preview_audio.export(p_buffer, format="wav")
        st.audio(p_buffer, format="audio/wav")

    with col_effects:
        st.write("### 🛠️ Professional Touch")
        boost = st.select_slider("Volume Boost (dB)", options=[0, 3, 6, 10, 15], value=3)
        fade = st.checkbox("Add Smooth Fade (In/Out)", value=True)
        
        if st.button("🚀 Render Master File"):
            with st.spinner("Processing..."):
                # Apply Effects
                final = preview_