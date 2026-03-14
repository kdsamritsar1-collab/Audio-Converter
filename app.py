# --- STEP 1: COMPATIBILITY PATCH FOR PYTHON 3.13+ ---
import sys
try:
    import audioop
except ImportError:
    try:
        import audioop_lpm as audioop
        sys.modules['audioop'] = audioop
    except ImportError:
        pass # Streamlit will handle errors if dependencies are missing

# --- STEP 2: IMPORTS ---
import streamlit as st
from pydub import AudioSegment
import io
import zipfile

# --- STEP 3: UI SETUP ---
st.set_page_config(page_title="Ruhani Audio Studio", page_icon="🎧", layout="centered")

st.title("🎧 Ruhani Audio Studio")
st.subheader("Professional MP3 to WAV Converter")
st.markdown("""
यह टूल आपकी फाइल्स को **Studio Standard (16-bit, 44.1 kHz, Stereo)** में बदलता है।  
*DistroKid, Spotify और Apple Music के लिए एकदम सही।*
""")

# --- STEP 4: CONVERSION LOGIC ---
uploaded_files = st.file_uploader("अपनी MP3 फाइलें यहाँ अपलोड करें", type=["mp3"], accept_multiple_files=True)

if uploaded_files:
    st.info(f"कुल {len(uploaded_files)} फाइलें प्रोसेस के लिए तैयार हैं।")
    
    if st.button("🚀 Start Bulk Conversion"):
        converted_items = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for index, file in enumerate(uploaded_files):
            try:
                status_text.text(f"प्रक्रिया जारी है: {file.name}")
                
                # ऑडियो लोड करें
                audio = AudioSegment.from_file(file, format="mp3")
                
                # प्रोफेशनल सेटिंग्स लागू करें
                # Frame Rate: 44100, Channels: 2 (Stereo), Sample Width: 2 (16-bit)
                audio = audio.set_frame_rate(44100).set_channels(2).set_sample_width(2)
                
                # बफर में सेव करें
                buf = io.BytesIO()
                audio.export(buf, format="wav")
                
                new_name = file.name.replace(".mp3", "_studio.wav")
                converted_items.append({"name": new_name, "data": buf.getvalue()})
                
                # प्रोग्रेस अपडेट करें
                progress_bar.progress((index + 1) / len(uploaded_files))
                
            except Exception as e:
                st.error(f"Error converting {file.name}: {str(e)}")
        
        status_text.text("✅ कन्वर्शन पूरा हुआ!")

        # --- STEP 5: DOWNLOAD SECTION ---
        if converted_items:
            st.divider()
            
            # ZIP फाइल तैयार करें
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as z:
                for item in converted_items:
                    z.writestr(item["name"], item["data"])
            
            # डाउनलोड बटन
            st.download_button(
                label="📦 Download All as ZIP",
                data=zip_buffer.getvalue(),
                file_name="ruhani_studio_wavs.zip",
                mime="application/zip",
                use_container_width=True
            )
            
            # इंडिविजुअल लिस्ट
            with st.expander("Show individual files"):
                for item in converted_items:
                    st.download_button(f"⬇️ {item['name']}", item['data'], item['name'])

st.divider()
st.caption("Developed for @ruhanijot | 16-bit / 44.1kHz Stereo Standard")