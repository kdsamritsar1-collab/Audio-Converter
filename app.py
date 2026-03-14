import streamlit as st
from pydub import AudioSegment, effects
import numpy as np
import matplotlib.pyplot as plt
import io
import os

st.set_page_config(page_title="Ruhani Comparison Studio", layout="wide")

# Dark Studio Theme
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .waveform-box { 
        border: 1px solid #333; 
        border-radius: 8px; 
        padding: 5px; 
        background: black;
        margin-bottom: 5px;
    }
    .stSlider { margin-top: -15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Ruhani Pro: Original vs Preview Studio")

uploaded_file = st.file_uploader("Upload Audio", type=['mp3', 'wav', 'm4a'], label_visibility="collapsed")

if uploaded_file:
    base_name = os.path.splitext(uploaded_file.name)[0]
    final_filename = f"{base_name}_wav.wav"

    audio = AudioSegment.from_file(uploaded_file)
    duration = len(audio) / 1000.0
    
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2: samples = samples.reshape((-1, 2))[:, 0]

    # --- 1. SELECTION AREA ---
    st.subheader("✂️ Step 1: Select Your Segment")
    trim_range = st.slider("Timeline Control", 0.0, float(duration), (0.0, float(duration)), step=0.01)
    start_s, end_s = trim_range
    
    # Process segments for comparison
    orig_segment = audio[start_s*1000 : end_s*1000]
    
    st.write("---")

    # --- 2. COMPARISON INTERFACE ---
    col_orig, col_prev = st.columns(2)

    with col_orig:
        st.markdown("### 🔈 Original")
        # Plot Original Wave
        st.markdown('<div class="waveform-box">', unsafe_allow_html=True)
        fig_o, ax_o = plt.subplots(figsize=(10, 3))
        o_samples = np.array(orig_segment.get_array_of_samples())
        if orig_segment.channels == 2: o_samples = o_samples.reshape((-1, 2))[:, 0]
        ax_o.fill_between(np.linspace(start_s, end_s, len(o_samples[::100])), o_samples[::100], color='gray', alpha=0.6)
        ax_o.set_xlim(start_s, end_s)
        ax_o.set_axis_off()
        fig_o.patch.set_facecolor('black')
        st.pyplot(fig_o)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Original Player
        o_buf = io.BytesIO()
        orig_segment.export(o_buf, format="wav")
        st.audio(o_buf, format="audio/wav")

    with col_prev:
        st.markdown("### 🔊 Preview (Mastered)")
        
        # Settings that reflect in real-time
        f_in = st.sidebar.slider("Fade In (s)", 0.0, 5.0, 1.0)
        f_out = st.sidebar.slider("Fade Out (s)", 0.0, 5.0, 2.0)
        boost = st.sidebar.slider("Boost (dB)", 0, 20, 5)
        
        # Apply Effects for Preview
        prev_segment = orig_segment + boost
        if f_in > 0: prev_segment = prev_segment.fade_in(int(f_in * 1000))
        if f_out > 0: prev_segment = prev_segment.fade_out(int(f_out * 1000))
        prev_segment = effects.normalize(prev_segment)

        # Plot Preview Wave (Notice how it looks "bigger/louder")
        st.markdown('<div class="waveform-box">', unsafe_allow_html=True)
        fig_p, ax_p = plt.subplots(figsize=(10, 3))
        p_samples = np.array(prev_segment.get_array_of_samples())
        if prev_segment.channels == 2: p_samples = p_samples.reshape((-1, 2))[:, 0]
        ax_p.fill_between(np.linspace(start_s, end_s, len(p_samples[::100])), p_samples[::100], color='#1DB954', alpha=0.9)
        ax_p.set_xlim(start_s, end_s)
        ax_p.set_axis_off()
        fig_p.patch.set_facecolor('black')
        st.pyplot(fig_p)
        st.markdown('</div>', unsafe_allow_html=True)

        # Preview Player
        p_buf = io.BytesIO()
        prev_segment.export(p_buf, format="wav")
        st.audio(p_buf, format="audio/wav")

    # --- 3. EXPORT ---
    st.write("---")
    if st.button("🚀 EXPORT FINAL MASTERED WAV", use_container_width=True):
        st.download_button(
            label=f"📥 Download {final_filename}",
            data=p_buf.getvalue(),
            file_name=final_filename,
            mime="audio/wav",
            use_container_width=True
        )

st.markdown("---")
st.caption("Ruhani Records: A/B Comparison Engine Enabled")