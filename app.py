import streamlit as st
from pydub import AudioSegment, effects
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

st.set_page_config(page_title="Ruhani Pro Editor", layout="wide")

# Professional Studio Theme CSS
st.markdown("""
    <style>
    .main { background-color: #121212; color: white; }
    div[data-testid="stExpander"] { border: none !important; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #1DB954; color: white; border: none; }
    .waveform-container { border: 1px solid #333; border-radius: 10px; padding: 10px; background: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Ruhani Advanced Audio Studio")

uploaded_file = st.file_uploader("Upload Audio", type=['mp3', 'wav', 'm4a'], label_visibility="collapsed")

if uploaded_file:
    # 1. Load Audio
    audio = AudioSegment.from_file(uploaded_file)
    duration = len(audio) / 1000.0
    
    # 2. Professional Timeline Visual
    st.subheader("📊 Editing Timeline")
    
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2: samples = samples.reshape((-1, 2))[:, 0]
    
    # Waveform Display
    with st.container():
        st.markdown('<div class="waveform-container">', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(15, 3.5))
        time_axis = np.linspace(0, duration, len(samples[::150]))
        
        # Professional Gradient-like look
        ax.fill_between(time_axis, samples[::150], color='#1DB954', alpha=0.9, linewidth=0.5)
        ax.set_xlim(0, duration)
        ax.set_ylim(min(samples), max(samples))
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        
        # Grid lines like a DAW (Digital Audio Workstation)
        ax.grid(color='#333', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Floating-style Controls (Real-time Feel)
    st.write("---")
    
    # Hum 'Range Slider' ko bilkul Waveform ke niche rakhenge taaki ye timeline ki tarah kaam kare
    trim_range = st.slider(
        "↔️ Drag to Select Trim Area (Start & End)",
        min_value=0.0, max_value=float(duration),
        value=(0.0, float(duration)),
        step=0.01, # Extra precision
        help="Slide left to set start, slide right to set end"
    )
    
    start_s, end_s = trim_range
    
    # --- PRO PLAYER SECTION ---
    col_play, col_info = st.columns([1, 2])
    
    with col_play:
        st.write("### 🎮 Transport")
        preview_audio = audio[start_s*1000 : end_s*1000]
        preview_buffer = io.BytesIO()
        preview_audio.export(preview_buffer, format="wav")
        
        # Isse play button aur slider sync mehsoos honge
        st.audio(preview_buffer, format="audio/wav")

    with col_info:
        st.write("### 📝 Segment Info")
        dur = round(end_s - start_s, 2)
        st.markdown(f"**Start:** `{start_s}s` | **End:** `{end_s}s` | **Selection Length:** `{dur}s`")
        
    st.write("---")

    # --- ACTION BUTTONS ---
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        boost = st.select_slider("🔥 Volume Boost", options=[0, 5, 10, 15, 20], value=5)
    with col_b:
        st.write("###") # Spacer
        if st.button("🚀 Render & Export"):
            final = preview_audio + boost
            final = effects.normalize(final)
            final_buf = io.BytesIO()
            final.export(final_buf, format="wav")
            st.session_state.final_wav = final_buf.getvalue()
            st.success("WAV Rendered!")

    with col_c:
        st.write("###") # Spacer
        if "final_wav" in st.session_state:
            st.download_button("📥 Download Pro WAV", st.session_state.final_wav, "ruhani_master.wav")