import streamlit as st
from pydub import AudioSegment, effects
import librosa
import librosa.display
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Ruhani Audio Pro", page_icon="🎙️")

st.title("🎙️ Ruhani Advanced Audio Studio")
st.caption("Trim, Boost & Normalize for Ikjot Ruhani Records")

uploaded_file = st.file_uploader("Upload Audio File", type=['mp3', 'm4a', 'wav', 'ogg'])

if uploaded_file is not None:
    # 1. Load Audio
    audio = AudioSegment.from_file(uploaded_file)
    duration_secs = len(audio) / 1000.0

    # 2. Visualization
    st.subheader("🔊 Visual Waveform")
    y, sr = librosa.load(uploaded_file, sr=None)
    fig, ax = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y, sr=sr, ax=ax, color="#1DB954")
    st.pyplot(fig)

    # 3. Controls
    st.subheader("⚙️ Audio Processing")
    
    col1, col2 = st.columns(2)
    with col1:
        # Volume Boost in Decibels (dB)
        boost_db = st.slider("Volume Boost (dB)", 0, 20, 0, help="0 means original volume. 10 is much louder.")
    with col2:
        # Normalize: Puray audio ki volume ko ek level pe lana
        normalize = st.checkbox("Normalize Audio", value=True, help="Makes the quiet parts louder and loud parts consistent.")

    start_time, end_time = st.slider(
        "Select Trim Range (Seconds)",
        0.0, float(duration_secs), (0.0, float(duration_secs))
    )

    # 4. Processing Logic
    if st.button("Apply & Export to WAV"):
        with st.spinner("Processing..."):
            # A. Trim
            processed = audio[start_time * 1000 : end_time * 1000]
            
            # B. Boost Volume
            if boost_db > 0:
                processed = processed + boost_db
            
            # C. Normalize (Peak normalization)
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