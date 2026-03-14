import streamlit as st
from pydub import AudioSegment, effects
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Ruhani Pro Audio Editor", layout="wide")

# Custom CSS for better look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stSlider { padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Ruhani Advanced Audio Studio")
st.write("---")

uploaded_file = st.file_uploader("Upload your recording (MP3, WAV, M4A)", type=['mp3', 'm4a', 'wav', 'ogg'])

if uploaded_file:
    # 1. Load & Basic Info
    audio = AudioSegment.from_file(uploaded_file)
    duration = len(audio) / 1000.0
    
    # 2. Top Preview Player (Sunne ke liye)
    st.subheader("🎵 Listen to Original")
    st.audio(uploaded_file)
    
    # 3. Waveform Visualization
    st.subheader("📊 Audio Timeline Visual")
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        samples = samples.reshape((-1, 2))[:, 0]
    
    fig, ax = plt.subplots(figsize=(15, 3))
    # Timeline points for X-axis
    time_axis = np.linspace(0, duration, len(samples[::200]))
    ax.fill_between(time_axis, samples[::200], color='#1DB954', alpha=0.7)
    ax.set_xlabel("Time (Seconds)")
    ax.set_facecolor('#0e1117')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    st.pyplot(fig)

    # 4. Interactive Sliders & Controls
    st.write("---")
    col_trim, col_effects = st.columns([2, 1])

    with col_trim:
        st.subheader("✂️ Trim Settings")
        # Ye slider aapko "Slide" karne ki poori flexibility dega
        start_time, end_time = st.slider(
            "Set Start & End Points",
            0.0, float(duration), (0.0, float(duration)),
            step=0.1, format="%.1fs"
        )
        st.write(f"Selection: **{start_time}s** to **{end_time}s** (Total: {round(end_time-start_time, 2)}s)")

    with col_effects:
        st.subheader("🎚️ Enhancements")
        boost = st.select_slider("Volume Boost", options=[0, 3, 6, 10, 15, 20], value=5)
        do_norm = st.toggle("Auto-Normalize (Clean Sound)", value=True)

    # 5. Process & Download
    if st.button("🚀 Process Trimmed Audio", use_container_width=True):
        with st.spinner("Cutting and Enhancing..."):
            # Trimming
            cut = audio[start_time*1000 : end_time*1000]
            # Boosting
            if boost > 0: cut = cut + boost
            # Normalizing
            if do_norm: cut = effects.normalize(cut)
            
            # Result
            out = io.BytesIO()
            cut.export(out, format="wav")
            
            st.success("Trimmed & Enhanced Version Ready!")
            st.audio(out, format="audio/wav")
            st.download_button("📥 Download Pro WAV", out.getvalue(), f"ruhani_pro_{start_time}s.wav")