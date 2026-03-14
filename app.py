import streamlit as st
from pydub import AudioSegment, effects
import numpy as np
import matplotlib.pyplot as plt
import io
import os

st.set_page_config(page_title="Ruhani Split-View Studio", layout="wide")

# Studio Theme CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .waveform-container { 
        border: 1px solid #333; 
        border-radius: 10px; 
        padding: 5px; 
        background: black;
        margin-bottom: 5px;
    }
    .stSlider { margin-top: -15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Ruhani Professional Split-View Studio")

uploaded_file = st.file_uploader("Upload Audio File", type=['mp3', 'wav', 'm4a'], label_visibility="collapsed")

if uploaded_file:
    base_name = os.path.splitext(uploaded_file.name)[0]
    final_filename = f"{base_name}_wav.wav"

    audio = AudioSegment.from_file(uploaded_file)
    duration = len(audio) / 1000.0
    
    # Audio data extraction
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2: samples = samples.reshape((-1, 2))[:, 0]

    # --- MAIN SPLIT INTERFACE ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🌐 Original Overview")
        st.markdown('<div class="waveform-container">', unsafe_allow_html=True)
        fig_orig, ax_orig = plt.subplots(figsize=(10, 3.5))
        time_axis_full = np.linspace(0, duration, len(samples[::300]))
        ax_orig.fill_between(time_axis_full, samples[::300], color='#1DB954', alpha=0.4)
        ax_orig.set_xlim(0, duration)
        ax_orig.set_axis_off()
        fig_orig.patch.set_facecolor('black')
        st.pyplot(fig_orig)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Unified Selection Slider
        trim_range = st.slider("Select Trim Area", 0.0, float(duration), (0.0, float(duration)), step=0.01)
        start_s, end_s = trim_range

    with col_right:
        st.subheader("🔍 Zoom-In Preview")
        # Extracting specific sample range for zoom view
        start_sample = int(start_s * audio.frame_rate)
        end_sample = int(end_s * audio.frame_rate)
        zoomed_samples = samples[start_sample:end_sample]
        
        st.markdown('<div class="waveform-container">', unsafe_allow_html=True)
        fig_zoom, ax_zoom = plt.subplots(figsize=(10, 3.5))
        if len(zoomed_samples) > 0:
            time_axis_zoom = np.linspace(start_s, end_s, len(zoomed_samples[::100]))
            ax_zoom.fill_between(time_axis_zoom, zoomed_samples[::100], color='#1DB954', alpha=0.9)
            ax_zoom.set_xlim(start_s, end_s)
        ax_zoom.set_axis_off()
        fig_zoom.patch.set_facecolor('black')
        st.pyplot(fig_zoom)
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption(f"Showing details from {start_s}s to {end_s}s")

    # --- PLAYBACK & CONTROLS ---
    st.write("---")
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.write("### 🎮 Preview Selection")
        preview_segment = audio[start_s*1000 : end_s*1000]
        p_buf = io.BytesIO()
        preview_segment.export(p_buf, format="wav")
        st.audio(p_buf, format="audio/wav")

    with c2:
        st.write("### 🛠️ Mastering Tools")
        f_in = st.slider("Fade In (s)", 0.0, 5.0, 1.0)
        f_out = st.slider("Fade Out (s)", 0.0, 5.0, 2.0)
        boost = st.slider("Volume Boost (dB)", 0, 20, 3)

    if st.button("🚀 MASTER & DOWNLOAD FINAL WAV", use_container_width=True):
        with st.spinner("Processing..."):
            final = preview_segment + boost
            if f_in > 0: final = final.fade_in(int(f_in * 1000))
            if f_out > 0: final = final.fade_out(int(f_out * 1000))
            final = effects.normalize(final)
            
            out_buf = io.BytesIO()
            final.export(out_buf, format="wav")
            
            st.download_button(
                label=f"📥 Download {final_filename}",
                data=out_buf.getvalue(),
                file_name=final_filename,
                mime="audio/wav",
                use_container_width=True
            )

st.markdown("---")
st.caption("Ruhani Split-View Studio | Ikjot Ruhani Records Edition")