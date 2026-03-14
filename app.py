import sys

# Python 3.13+ के लिए audioop का जुगाड़
try:
    import audioop
except ImportError:
    # अगर सिस्टम में audioop नहीं है, तो हम एक खाली डमी क्लास बना देंगे 
    # ताकि pydub क्रैश न हो (जब तक हम भारी काम नहीं कर रहे)
    class DummyAudioop:
        def __getattr__(self, name):
            def dummy(*args, **kwargs):
                raise NotImplementedError(f"audioop.{name} is not available in this Python version.")
            return dummy
    sys.modules['audioop'] = DummyAudioop()

import streamlit as st
from pydub import AudioSegment
import io
import zipfile

# ... बाकी का कोड ...

st.set_page_config(page_title="Ruhani Bulk Audio Lab", page_icon="🎚️")

st.title("🎚️ Ruhani Bulk Audio Converter")
st.write("एक साथ कई MP3 फाइल्स को **16-bit, 44.1 kHz, Stereo WAV** में बदलें।")

# फाइल अपलोडर
uploaded_files = st.file_uploader("MP3 फाइल्स चुनें", type=["mp3"], accept_multiple_files=True)

if uploaded_files:
    st.info(f"कुल {len(uploaded_files)} फाइलें अपलोड की गईं।")
    
    # कनवर्टेड फाइल्स को स्टोर करने के लिए लिस्ट
    converted_files = []
    
    if st.button("Start Bulk Conversion"):
        progress_bar = st.progress(0)
        
        for index, uploaded_file in enumerate(uploaded_files):
            try:
                # ऑडियो प्रोसेसिंग
                audio = AudioSegment.from_file(uploaded_file, format="mp3")
                audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
                
                # मेमोरी में सेव करना
                wav_io = io.BytesIO()
                audio.export(wav_io, format="wav")
                wav_io.seek(0)
                
                # लिस्ट में नाम और डेटा सेव करना
                new_filename = uploaded_file.name.replace(".mp3", "_studio.wav")
                converted_files.append({"name": new_filename, "data": wav_io.getvalue()})
                
                # प्रोग्रेस अपडेट
                progress_bar.progress((index + 1) / len(uploaded_files))
                
            except Exception as e:
                st.error(f"Error converting {uploaded_file.name}: {e}")
        
        st.success("सभी फाइलें कनवर्ट हो गई हैं!")

        # 📦 ZIP फाइल तैयार करना
        if converted_files:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                for file in converted_files:
                    zip_file.writestr(file["name"], file["data"])
            
            st.divider()
            st.subheader("📥 अपना काम डाउनलोड करें")
            
            # पूरे पैक को एक साथ डाउनलोड करें
            st.download_button(
                label="Download All as ZIP",
                data=zip_buffer.getvalue(),
                file_name="converted_wav_files.zip",
                mime="application/zip",
                use_container_width=True
            )
            
            # अलग-अलग फाइल्स का प्रीव्यू और डाउनलोड
            with st.expander("Show individual files"):
                for file in converted_files:
                    st.write(f"✔️ {file['name']}")
                    st.download_button(f"Download {file['name']}", file['data'], file['name'])

st.divider()
st.caption("Standard for Music Distribution (DistroKid/Spotify Compatible) | Created for Ruhani Jot")