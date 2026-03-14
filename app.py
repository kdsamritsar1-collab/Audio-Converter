# --- Step 1: Python 3.13/3.14 Compatibility Patch ---
import sys
try:
    import audioop
except ImportError:
    try:
        import audioop_lpm as audioop
        sys.modules['audioop'] = audioop
    except ImportError:
        st.error("Missing dependency: audioop-lpm. Please add it to requirements.txt")

# --- Step 2: Main Imports ---
import streamlit as st
from pydub import AudioSegment
import io
import zipfile

# --- Step 3: Web App UI ---
st.set_page_config(page_title="Ruhani Studio Converter", page_icon="🎧", layout="wide")

st.title("🎧 Ruhani Studio Audio Converter")
st.markdown("""
यह टूल आपकी MP3 फाइल्स को म्यूजिक डिस्ट्रीब्यूशन (DistroKid/Spotify) के लिए 
**16-bit, 44.1 kHz, Stereo WAV** फॉर्मेट में बदल देगा।
""")

# Sidebar for Settings
st.sidebar.header("Target Settings")
st.sidebar.info("Sample Rate: 44100 Hz\n\nChannels: Stereo\n\nBit Depth: 16-bit")

# File Uploader
uploaded_files = st.file_uploader("अपनी MP3 फाइलें यहाँ अपलोड करें", type=["mp3"], accept_multiple_files=True)

if uploaded_files:
    st.write(f"📂 {len(uploaded_files)} फाइलें चुनी गईं।")
    
    # Session state to store converted data
    if 'converted_data' not in st.session_state:
        st.session_state.converted_data = []

    if st.button("🚀 Start Bulk Conversion"):
        st.session_state.converted_data = [] # Reset old data
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for index, uploaded_file in enumerate(uploaded_files):
            try:
                status_text.text(f"Converting: {uploaded_file.name}...")
                
                # Load Audio
                audio = AudioSegment.from_file(uploaded_file, format="mp3")
                
                # Apply Studio Standards (This requires audioop.ratecv)
                audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
                
                # Export to Buffer
                wav_io = io.BytesIO()
                audio.export(wav_io, format="wav")
                wav_io.seek(0)
                
                # Store Result
                new_name = uploaded_file.name.replace(".mp3", "_studio.wav")
                st.session_state.converted_data.append({
                    "name": new_name,
                    "data": wav_io.getvalue()
                })
                
                # Update Progress
                progress_bar.progress((index + 1) / len(uploaded_files))
                
            except Exception as e:
                st.error(f"Error converting {uploaded_file.name}: {str(e)}")
        
        status_text.text("✅ सभी फाइलें सफलतापूर्वक कनवर्ट हो गईं!")

    # --- Step 4: Download Section ---
    if st.session_state.converted_data:
        st.divider()
        st.subheader("📥 डाउनलोड विकल्प")
        
        # Creating ZIP in memory
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for file in st.session_state.converted_data:
                zip_file.writestr(file["name"], file["data"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📦 Download All as ZIP",
                data=zip_buf.getvalue(),
                file_name="ruhani_studio_pack.zip",
                mime="application/zip",
                use_container_width=True
            )
            
        with col2:
            if st.button("🧹 Clear All"):
                st.session_state.converted_data = []
                st.rerun()

        # Individual File List
        with st.expander("Individually Download Files"):
            for file in st.session_state.converted_data:
                st.download_button(f"⬇️ {file['name']}", file['data'], file['name'], use_container_width=True)

st.divider()
st.caption("Developed for @ruhanijot | Studio Standard 16-bit/44.1kHz")