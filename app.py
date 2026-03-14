import streamlit as st
from pydub import AudioSegment, effects
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Ruhani Audio Pro", page_icon="🎙️")

st.title("🎙️ Ruhani Advanced Audio Studio")
st.caption("Trim, Boost & Normalize for Ikjot Ruhani Records")

uploaded_file = st.file_uploader("Upload Audio File", type=['mp3', 'm4a', 'wav', 'ogg'])

if uploaded_file is not None:
    # 1. Load Audio using Pydub (Much more stable for Streamlit)
    with st.spinner("Loading audio..."):
        audio = AudioSegment.from_file(uploaded_file)
        duration_secs = len(audio) / 1000.0

    # 2. FIXED Visualization (No more Libsndfile Error)
    st.subheader("🔊 Visual Waveform")
    with st.spinner("Generating waveform..."):
        # Convert pydub audio to numpy array
        samples = np.array(audio.get_array_of_samples())
        
        # If stereo, take only one channel for plotting
        if audio.channels == 2:
            samples = samples.reshape((-1, 2))[:, 0]
        
        # Plotting the wave
        fig, ax = plt.subplots(figsize=(12, 3))
        # Plotting every 100th sample for speed
        ax.plot(samples[::100], color="#1DB954", linewidth=0.5)
        ax.set_axis_off()  # Cleaning up the look
        st.pyplot(fig)

    # 3. Processing Controls
    st.subheader("⚙️ Audio Processing")
    
    col1, col2 = st.columns(2)
    with col1:
        boost_db = st.slider("Volume Boost (dB)", 0, 20, 5, help="Increase loudness.")
    with col2:
        normalize = st.checkbox("Normalize Audio", value=True, help="Balances loud/quiet parts.")

    start_time, end_time = st.slider(
        "Select Trim Range (Seconds)",
        0.0, float(duration_secs), (0.0, float(duration_secs)),
        step=0.1
    )

    # 4. Processing Logic
    if st.button("🚀 Apply & Export to WAV"):
        with st.spinner("Processing..."):
            # A. Trim
            processed = audio[start_time * 1000 : end_time * 1000]
            
            # B. Boost Volume
            if boost_db > 0:
                processed = processed + boost_db
            
            # C. Normalize
            if normalize:
                processed = effects.normalize(processed)
            
            # D. Export to Buffer
            wav_buffer = io.BytesIO()
            processed.export(wav_buffer, format="wav")
            
            st.success("Audio Processed Successfully!")
            st.audio(wav_buffer, format="audio/wav")
            
            st.download_button(
                label="📥 Download Pro WAV",
                data=wav_buffer.getvalue(),
                file_name=f"pro_{uploaded_file.name.split('.')[0]}.wav",
                mime="audio/wav"
            )