import streamlit as st
from pydub import AudioSegment
import io
import zipfile

# UI Setup
st.set_page_config(page_title="Ruhani Audio Studio", page_icon="🎧")

st.title("🎧 Ruhani Audio Studio")
st.write("Convert MP3 to **16-bit, 44.1 kHz, Stereo WAV**")

uploaded_files = st.file_uploader("MP3 फाइलें चुनें", type=["mp3"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 Start Conversion"):
        converted_items = []
        progress_bar = st.progress(0)
        
        for index, file in enumerate(uploaded_files):
            try:
                # ऑडियो लोड और प्रोसेस करें
                audio = AudioSegment.from_file(file, format="mp3")
                # Professional Settings: 44.1kHz, Stereo, 16-bit
                audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
                
                buf = io.BytesIO()
                audio.export(buf, format="wav")
                
                new_name = file.name.replace(".mp3", "_studio.wav")
                converted_items.append({"name": new_name, "data": buf.getvalue()})
                
                progress_bar.progress((index + 1) / len(uploaded_files))
            except Exception as e:
                st.error(f"Error in {file.name}: {e}")
        
        if converted_items:
            st.success("Conversion Complete!")
            st.divider()

            # --- स्मार्ट डाउनलोड लॉजिक ---
            if len(converted_items) == 1:
                # सिर्फ एक फाइल होने पर सीधा .wav डाउनलोड करें
                single_file = converted_items[0]
                st.info(f"फाइल तैयार है: {single_file['name']}")
                st.download_button(
                    label="📥 Download WAV File",
                    data=single_file["data"],
                    file_name=single_file["name"],
                    mime="audio/wav",
                    use_container_width=True
                )
            else:
                # एक से ज्यादा फाइल्स होने पर ZIP बनाएँ
                st.info(f"कुल {len(converted_items)} फाइल्स तैयार हैं।")
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as z:
                    for item in converted_items:
                        z.writestr(item["name"], item["data"])
                
                st.download_button(
                    label="📦 Download All as ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="converted_wavs.zip",
                    mime="application/zip",
                    use_container_width=True
                )

st.divider()
st.caption("Standard for Music Distribution | Created for Ruhani Jot")