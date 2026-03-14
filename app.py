import streamlit as st
from pydub import AudioSegment, effects
import numpy as np
import matplotlib.pyplot as plt
import io
import os

st.set_page_config(page_title="Ruhani Integrated Studio", layout="wide")

# Custom Dark Studio CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stSlider { margin-top: -10px; }
    .wave-container { 
        background-color: black; 
        border-radius: 10px; 
        padding: 10px; 
        border: 1px solid #333;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Ruhani Integrated Master Studio")

uploaded_file = st.file_uploader("Upload Audio", type=['mp3', 'wav', 'm4a'], label_visibility="collapsed")

if uploaded_file:
    # File Naming Logic
    base_name = os.path.splitext(uploaded_file.name)[0]
    final_filename = f"{base_name}_wav.wav"

    audio = AudioSegment.from_file(uploaded_file)
    duration = len(audio) / 1000.0
    
    # --- SIDEBAR CONTROLS (Processing) ---
    st.sidebar.header("🛠️ Mastering Tools")
    f_in = st.sidebar.slider("Fade In (s)", 0.0, 5.0, 1.0)
    f_out = st.sidebar.slider("Fade Out (s)", 0.0, 5.0, 2.0)
    boost = st.sidebar.slider("Volume Boost (dB)", 0, 20, 5)
    normalize = st.sidebar.checkbox("Auto-Normalize", value=True)

    # --- MAIN INTEGRATED SECTION ---
    st.subheader("✂️ Trim & Preview Dashboard")
    
    # 1. THE UNIFIED SLIDER
    trim_range = st.slider("↔️ Adjust Selection (Start & End)", 0.0, float(duration), (0.0, float(duration)), step=0.01)
    start_s, end_s = trim_range

    # 2. PROCESSING SAMPLES
    # Original segment for the 'Original' view
    orig_seg = audio[start_s*1000 : end_s*1000]
    
    # Apply effects for the 'Mastered' view
    master_seg = orig_seg + boost
    if f_in > 0: master_seg = master_seg.fade_in(int(f_in * 1000))
    if f_out > 0: master_seg = master_seg.fade_out(int(f_out * 1000))
    if normalize: master_seg = effects.normalize(master_seg)

    # 3. MERGED WAVEFORMS (Side by Side Comparison)
    col_a, col_b = st.columns(2)

    with col_a:
        st.caption("🔈 Original Segment")
        st.markdown('<div class="wave-container">', unsafe_allow_html=True)
        # Plotting Original
        fig_o, ax_o = plt.subplots(figsize=(10, 3))
        o_samps = np.array(orig_seg.get_array_of_samples())
        if orig_seg.channels == 2: o_samps = o_samps.reshape((-1, 2))[:, 0]
        ax_o.fill_between(np.linspace(start_s, end_s, len(o_samps[::100])), o_samps[::100], color='gray', alpha=0.5)
        ax_o.set_axis_off()
        fig_o.patch.set_facecolor('black')
        st.pyplot(fig_o)
        st.markdown('</div>', unsafe_allow_html=True)
        # Original Player
        o_buf = io.BytesIO()
        orig_seg.export(o_buf, format="wav")
        st.audio(o_buf, format="audio/wav")

    with col_b:
        st.caption("🔊 Mastered Preview")
        st.markdown('<div class="wave-container">', unsafe_allow_html=True)
        # Plotting Mastered
        fig_m, ax_m = plt.subplots(figsize=(10, 3))
        m_samps = np.array(master_seg.get_array_of_samples())
        if master_seg.channels == 2: m_samps = m_samps.reshape((-1, 2))[:, 0]
        ax_m.fill_between(np.linspace(start_s, end_s, len(m_samps[::100])), m_samps[::100], color='#1DB954', alpha=0.9)
        ax_m.set_axis_off()
        fig_m.patch.set_facecolor('black')
        st.pyplot(fig_m)
        st.markdown('</div>', unsafe_allow_html=True)
        # Mastered Player
        m_buf = io.BytesIO()
        master_seg.export(m_buf, format="wav")
        st.audio(m_buf, format="audio/wav")

    # 4. FINAL EXPORT BUTTON
    st.write("---")
    st.download_button(
        label=f"🚀 DOWNLOAD MASTERED WAV ({final_filename})",
        data=m_buf.getvalue(),
        file_name=final_filename,
        mime="audio/wav",
        use_container_width=True
    )

st.markdown("---")
st.caption("Ruhani Records All-in-One Audio Engine | v6.0 Fully Merged")