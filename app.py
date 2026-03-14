import streamlit as st
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
import io

# Page Config for a Wide Studio Look
st.set_page_config(page_title="Ruhani WAV Zoom Studio", layout="wide")

st.markdown("""
    <style>
    .stSlider > div [data-baseweb="slider"] { height: 10px; }
    .stAudio { width: 100%; }
    .main { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ Ruhani Advanced WAV Studio (with Zoom)")
st.caption("Professional Precise Trimming for Ikjot Ruhani Records")

uploaded_file = st.file_uploader("Upload Audio (MP3, WAV, M4A)", type=['mp3', 'm4a', 'wav'])

if uploaded_file:
    # 1. Load Audio
    audio = AudioSegment.from_file(uploaded_file)
    duration = len(audio) / 1000.0
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        samples = samples.reshape((-1, 2))[:, 0]
    
    # Timeline points for the whole file
    time_axis_full = np.linspace(0, duration, len(samples[::200]))

    # --- Container 1: FULL WAVEFORM & TRIM SLIDER ---
    st.subheader("📊 Full Recording Timeline")
    
    # Plotting the whole file for context
    fig_full, ax_full = plt.subplots(figsize=(15, 2))
    ax_full.fill_between(time_axis_full, samples[::200], color='#1DB954', alpha=0.5)
    ax_full.set_xlim(0, duration)
    ax_full.set_axis_off()
    ax_full.set_facecolor('#0e1117')
    fig_full.patch.set_facecolor('#0e1117')
    st.pyplot(fig_full)

    # Full Range Slider
    trim_range = st.slider(
        "Select Range to ZOOM",
        min_value=0.0,
        max_value=float(duration),
        value=(0.0, float(duration)),
        step=0.1,
        format="%.1fs"
    )
    start_s, end_s = trim_range
    st.caption(f"Current Range for Zoom: {start_s:.2f}s — {end_s:.2f}s | Length: {end_s - start_s:.2f}s")
    
    st.write("---")

    # --- Container 2: ZOOMED WAVEFORM & FINE SLIDER ---
    if end_s > start_s: # Safety check
        st.subheader("🔍 Zoomed View (Fine-Tuning)")
        
        # Slicing the numpy samples for the zoomed view
        # Isse calculation efficient hoti hai
        start_sample = int(start_s * audio.frame_rate)
        end_sample = int(end_s * audio.frame_rate)
        zoomed_samples = samples[start_sample : end_sample]
        time_axis_zoom = np.linspace(start_s, end_s, len(zoomed_samples[::50]))

        # Zoomed Waveform Display
        fig_zoom, ax_zoom = plt.subplots(figsize=(15, 3))
        ax_zoom.fill_between(time_axis_zoom, zoomed_samples[::50], color='#1DB954', alpha=0.9)
        ax_zoom.set_xlim(start_s, end_s)
        ax_zoom.set_axis_off()
        ax_zoom.set_facecolor('#0e1117')
        fig_zoom.patch.set_facecolor('#0e1117')
        st.pyplot(fig_zoom)

        # Fine-Tuning Slider (सौवें हिस्से तक की बारीकी)
        # Ye slider Zoomed View ko modify nahi karta, balki Preview aur Output ke liye hai
        st.write("### ✂️ Fine Trim Selection")
        fine_trim = st.slider(
            "Final Selection (Move to fine-tune preview)",
            min_value=float(start_s),
            max_value=float(end_s),
            value=(float(start_s), float(end_s)),
            step=0.01, # Precise to 0.01s
            format="%.2fs"
        )
        final_start, final_end = fine_trim
        st.caption(f"🚀 Final Selection: {final_start:.2f}s — {final_end:.2f}s")

        # --- PREVIEW & EXPORT ---
        st.write("---")
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("🎧 Real-time Preview")
            # Update Preview Audio based on Fine Trim
            preview_audio = audio[final_start*1000 : final_end*1000]
            preview_buffer = io.BytesIO()
            preview_audio.export(preview_buffer, format="wav")
            st.audio(preview_buffer, format="audio/wav")

        with col2:
            st.subheader("✅ Confirm WAV Export")
            if st.button("🚀 Process & Download", use_container_width=True):
                # Export final buffer
                final_buffer = io.BytesIO()
                preview_audio.export(final_buffer, format="wav")
                st.download_button("📥 Download Final WAV", final_buffer.getvalue(), "ruhani_pro_zoom_cut.wav")