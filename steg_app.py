import streamlit as st
from PIL import Image
import io
import base64

from utills.encode import encode_message, file_to_base64, base64_to_file
from utills.decode import decode_message
from utills.encrpyt import encrypt_message, decrypt_message
from utills.random_steg import encode_random_lsb, decode_random_lsb

import io
from utills.audio_steg import embed_file_in_audio, extract_file_from_audio, get_max_audio_capacity
from utills.video_steg import get_file_size_bytes

st.set_page_config(page_title="StegoX", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1f77b4;'> Welcome to StegoX</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Your Ultimate Secret File Hiding Toolkit</h4>", unsafe_allow_html=True)
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader(" What is StegoX?")
    st.markdown("""
    **StegoX** lets you:
    -  Hide messages in images
    -  Hide any file in images or audio
    -  Hide files inside audio (.wav)
    -  Decode secrets with password
    -  Protect your data creatively!
    """)
    
with col2:
    image = Image.open("utills/Gemini_Generated_Image_myug8bmyug8bmyug.png")
    image = image.resize((650, 280)) 
    st.image(image, use_container_width=True)
        
tabA, tabB = st.tabs(["Image Steganography", "Audio Steganography"])

with tabA:
    st.title(" Image Steganography Tool")
    st.caption("Securely encode or decode hidden messages inside images.")

    tab1, tab2 = st.tabs([" Encode", " Decode"])

    with tab1:
        st.subheader(" Upload Cover Image")
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "bmp"])
        option = st.radio("What do you want to hide?", ["Text Message", "File", " Image"])
    
        if option == "Text Message":
            st.subheader(" Encode Text Message")
            secret_message = st.text_area("Enter the secret message to hide")

        elif option == "File":
            st.subheader(" Encode a File")
            uploaded_secret_file = st.file_uploader("Upload any file (txt, pdf, png, etc.)", type=None, key="secret_file")

        elif option == " Image":
            st.subheader(" Encode an Image inside Image")
            uploaded_secret_img = st.file_uploader("Upload secret image (PNG/JPG)", type=["png", "jpg", "jpeg"], key="secret_img")
    
        if uploaded_file:
            image = Image.open(uploaded_file)
            png_image = image.convert("RGB")
        
            # ------------------ Case 1: Text Message ------------------
            if secret_message and not uploaded_secret_file:
                password = st.text_input("Set a password (optional)", type="password", key="pass_text")

                if password:
                    try:
                        secret_message = encrypt_message(secret_message, password)
                    except:
                        st.error("Encryption failed. Try a stronger password.")
                        st.stop()

                try:
                    encoded_image = encode_random_lsb(png_image, secret_message, seed=password or "default")
                    st.success(" Message encoded successfully into image.")
                    st.image(encoded_image, caption="Encoded Image", use_container_width=True)
                    buf = io.BytesIO()
                    encoded_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    st.download_button(" Download Encoded Image", data=byte_im, file_name="encoded_image.png", mime="image/png")
                
                except:
                    st.error("Encoding faied")    

            #  ------------------ Case 2: File Encoding ------------------
            elif uploaded_secret_file and not secret_message:
                file_bytes = uploaded_secret_file.read()
                file_b64 = file_to_base64(file_bytes)
            
                file_info = f"{uploaded_secret_file.name}::"
                full_payload = file_info + file_b64

                st.info(f"Selected file: {uploaded_secret_file.name} | Size: {len(file_bytes)} bytes")
                password = st.text_input("Set password (optional)", type="password", key="pass_file")

                if password:
                    try:
                        full_payload = encrypt_message(full_payload, password)
                    except:
                        st.error("Encryption failed. Try again.")
                        st.stop()

                encoded_image = encode_message(png_image, full_payload)
                st.success(" File successfully encoded inside the image!")
                st.image(encoded_image, caption="Encoded Image", use_container_width=True)

                buf = io.BytesIO()
                encoded_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(" Download Encoded Image", data=byte_im, file_name="encoded_with_file.png", mime="image/png")

        # ----------------------- case 3 image encode -----------------------------------------------
            elif  uploaded_secret_img and not secret_message and not uploaded_secret_file:
                password = st.text_input("Set password (optional)", type="password", key="pass_img")

           
                secret_image = Image.open(uploaded_secret_img)
                img_byte_arr = io.BytesIO()
                secret_image.save(img_byte_arr, format="PNG")
                img_bytes = img_byte_arr.getvalue()

                file_b64 = file_to_base64(img_bytes)
                full_payload = f"{uploaded_secret_img.name}::" + file_b64

                if password:
                    try:
                       full_payload = encrypt_message(full_payload, password)
                    except:
                        st.error("Encryption failed.")
                        st.stop()

                encoded_image = encode_message(png_image, full_payload)
                st.success("Image successfully hidden inside another image!")
                st.image(encoded_image, caption="Encoded Image", use_container_width=True)

                buf = io.BytesIO()
                encoded_image.save(buf, format="PNG")
                st.download_button("Download Encoded Image", data=buf.getvalue(), file_name="image_with_image.png", mime="image/png")
            
        # ------------------ Error: Both or None ------------------
            else:
                st.warning(" Please provide either a message OR a file (not both).")

    with tab2:
        st.subheader(" Upload Encoded Image (PNG only)")
        stego_image_file = st.file_uploader("Upload encoded PNG image only", type=["png"])

        if stego_image_file:
            image = Image.open(stego_image_file)
            st.image(image, caption="Uploaded Encoded Image", use_container_width=True)

            st.subheader(" Enter Password (if asked)")
            password = st.text_input("Enter password", type="password", key="decode_pass")
            length = st.number_input("Approx. message length (for random decoding)", min_value=1, max_value=1000, value=100)
        
            try:
                decoded_data = decode_message(image)

           
                if password:
                    try:
                        decoded_data = decrypt_message(decoded_data, password)
                    except:
                        st.error(" Wrong password or data not encrypted.")
                        st.stop()

                if "::" in decoded_data:
                    file_name, file_b64 = decoded_data.split("::", 1)
                    try:
                        file_bytes = base64.b64decode(file_b64)
                        try:
                            img = Image.open(io.BytesIO(file_bytes))
                            st.success(f"Hidden image extracted: {file_name}")
                            st.image(img, caption="Decoded Hidden Image", use_container_width=True)
                            st.download_button("Download Hidden Image", data=file_bytes,
                                           file_name=file_name, mime="image/png")
                        except:
                            st.success(f"Hidden file extracted: {file_name}")
                            st.download_button("Download Hidden File", data=file_bytes,
                                           file_name=file_name, mime="application/octet-stream")

                    except:
                        st.error("Failed to decode base64 data.")
                else:
                    try:
                         decoded_text = decode_random_lsb(image, num_chars=length, seed=password or "default")
                         st.success("Hidden message extracted:")
                         st.code(decoded_text)
                    
                    except:
                        st.error("text decoding faied")    
  
            except Exception as e:
                st.error("Failed to decode. Make sure image is valid and was encoded properly.") 
            
with tabB:
    st.title(" Audio Steganography Tool")

    tab1, tab2 = st.tabs([" Encode into Audio", " Decode from Audio"])

    with tab1:
        st.header("Embed Image/File/Video into Audio")

        audio_file = st.file_uploader("Upload WAV audio file", type=["wav"])
        file_to_hide = st.file_uploader("Upload file to hide (image, doc, video etc.)")

        if audio_file and file_to_hide:
            audio_path = io.BytesIO(audio_file.read())
            file_path = io.BytesIO(file_to_hide.read())

            max_capacity = get_max_audio_capacity(audio_path)
            file_size = get_file_size_bytes(file_path)

            st.write(f"**Audio Capacity:** {max_capacity / 1024:.2f} KB")
            st.write(f"**Your File Size:** {file_size / 1024:.2f} KB")

            if st.button(" Encode and Download"):
                try:
                    file_name = file_to_hide.name
                    stego_audio = embed_file_in_audio(audio_path, file_path, file_name)
                    st.download_button("Download Stego Audio", stego_audio, file_name="stego_audio.wav")
                except ValueError as e:
                    st.error(str(e))

    with tab2:
        st.header("Extract Hidden File from Audio")
        stego_audio = st.file_uploader("Upload stego-audio WAV file", type=["wav"])

        if stego_audio:
            audio_path = io.BytesIO(stego_audio.read())

            if st.button(" Decode and Download File"):
                try:
                    file_name, file_obj = extract_file_from_audio(audio_path)
                    st.download_button("Download Hidden File", file_obj, file_name=file_name)
                except Exception as e:
                    st.error(f"Failed to decode: {str(e)}")