import streamlit as st
from PIL import Image
import io
import base64

def encode_message(img, message):
    img = img.convert("RGB")
    encoded = img.copy()
    width, height = img.size
    message += chr(0)  # End marker

    data = iter(img.getdata())
    new_pixels = []

    for char in message:
        pixels = [value for value in next(data)[:3] +
                               next(data)[:3] +
                               next(data)[:3]]
        ascii_val = ord(char)
        for i in range(8):
            pixels[i] = pixels[i] & ~1 | ((ascii_val >> (7 - i)) & 1)
        new_pixels.extend([tuple(pixels[0:3]), tuple(pixels[3:6]), tuple(pixels[6:9])])

    # Add remaining pixels
    for pixel in data:
        new_pixels.append(pixel)

    encoded.putdata(new_pixels)
    return encoded

def file_to_base64(file_bytes):
    return base64.b64encode(file_bytes).decode('utf-8')

def base64_to_file(base64_string):
    return base64.b64decode(base64_string.encode('utf-8'))