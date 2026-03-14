import streamlit as st
from pydub import AudioSegment, effects
import numpy as np
import matplotlib.pyplot as plt
import io
import os  # File name extraction ke liye

st.set_page_config(page_title="Ruhani Pro Editor", layout="wide")

# Professional Dark Theme
st.markdown("""
    <style>
    .main { background-color: #121212; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #1DB954; color: white; }
    .waveform-container { border: 1px solid #333; border-radius: 10px; padding: 10px; background: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Ruhani Advanced Audio Studio")

uploaded_file = st.file_uploader("Upload Audio", type=['mp3', 'wav', 'm4a'], label_visibility="collapsed")

if uploaded_file:
    # --- FILE NAME LOGIC ---
    # Original name se extension hata kar '_wav' joda jayega
    base_name = os.path.splitext(uploaded_file.name)[0]
    final_filename = f"{base_name}_wav.wav"

    # 1. Load Audio
    audio = AudioSegment.from_file(uploaded_file)
    duration = len(audio) / 1000.0
    
    # 2. Professional Timeline Visual
    st.subheader(f"📊 Editing: {uploaded_file.name}")
    
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2: samples = samples.reshape((-1, 2))[:, 0]
    
    with st.container():
        st.markdown('<div class="waveform-container">', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(15, 3.5))
        time_axis = np.linspace(0, duration, len(samples[::150]))
        
        ax.fill_between(time_axis, samples[::150], color='#1DB954', alpha=0.9)
        ax.set_xlim(0, duration)
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        ax.grid(color='#333', linestyle='--', linewidth=0.5)
        ax.tick_params(colors='white')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Precision Slider (Timeline ke thik niche)
    trim_range = st.slider(
        "↔️ Drag to Select Trim Area",
        min_value=0.0, max_value=float(duration),
        value=(0.0, float(duration)),
        step=0.01
    )
    
    start_s, end_s = trim_range
    
    st.write("---")

    # 4. Preview & Export
    col_play, col_actions = st.columns([1, 1])
    
    with col_play:
        st.write("### 🎮 Preview Selection")
        preview_audio = audio[start_s*1000 : end_s*1000]
        preview_buffer = io.BytesIO()
        preview_audio.export(preview_buffer, format="wav")
        st.audio(preview_buffer, format="audio/wav")

    with col_actions:
        st.write("### 🚀 Final Export")
        boost = st.select_slider("Volume Boost", options=[0, 5, 10, 15], value=5)
        
        if st.button("Render Master File"):
            final = preview_audio + boost
            final = effects.normalize(final)
            final_buf = io.BytesIO()
            final.export(final_buf, format="wav")
            st.session_state.processed_wav = final_buf.getvalue()
            st.success(f"Ready to download as: {final_filename}")

    if "processed_wav" in st.session_state:
        st.download_button(
            label=f"📥 Download {final_filename}",
            data=st.session_state.processed_wav,
            file_name=final_filename,
            mime="audio/wav",
            use_container_width