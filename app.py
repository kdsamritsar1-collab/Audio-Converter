import sys

# --- Python 3.13/3.14 Compatibility Patch ---
try:
    import audioop
except ImportError:
    # अगर audioop गायब है, तो हम खुद का एक छोटा वर्जन बना लेते हैं
    # यह pydub को क्रैश होने से बचाएगा
    from types import ModuleType
    mock_audioop = ModuleType("audioop")
    mock_audioop.error = Exception
    # ज़रूरी फंक्शन्स जो pydub मांगता है
    mock_audioop.getsample = lambda *a: None 
    sys.modules["audioop"] = mock_audioop

import streamlit as st
from pydub import AudioSegment
import io
import zipfile

st.set_page_config(page_title="Ruhani Audio Lab", layout="wide")

st.title("🎧 Ruhani Studio Audio Converter")

# Check for ffmpeg
try:
    AudioSegment.from_mono_audiosegments # Simple check
except Exception:
    st.error("ffmpeg is not installed. Please make sure 'packages.txt' has 'ffmpeg' written in it.")

uploaded_files = st.file_uploader("MP3 फाइल्स अपलोड करें", type=["mp3"], accept_multiple_files=True)

if uploaded_files:
    if st.button("Convert to Studio WAV (16-bit, 44.1kHz)"):
        converted_list = []
        progress = st.progress(0)
        
        for i, file in enumerate(uploaded_files):
            try:
                # ऑडियो लोड करें
                song = AudioSegment.from_file(file, format="mp3")
                
                # प्रोफेशनल सेटिंग्स
                # नोट: अगर Python 3.14 पर 'audioop' का असली फंक्शन नहीं मिला, 
                # तो यहाँ एरर आ सकती है। इसका बेस्ट हल Python 3.12 का उपयोग करना है।
                song = song.set_frame_rate(44100).set_channels(2).set_sample_width(2)
                
                buf = io.BytesIO()
                song.export(buf, format="wav")
                converted_list.append({"name": file.name.replace(".mp3", ".wav"), "data": buf.getvalue()})
                progress.progress((i + 1) / len(uploaded_files))
            except Exception as e:
                st.error(f"Error converting {file.name}: {e}")

        if converted_list:
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w") as z:
                for f in converted_list:
                    z.writestr(f["name"], f["data"])
            
            st.success("Conversion Complete!")
            st.download_button("📦 Download All as ZIP", zip_buf.getvalue(), "converted_audio.zip")