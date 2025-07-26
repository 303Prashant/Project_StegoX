import streamlit as st
from PIL import Image
import io

def decode_message(img):
    img = img.convert("RGB")
    data = iter(img.getdata())
    message = ""
    while True:
        pixels = [value for value in next(data)[:3] +
                               next(data)[:3] +
                               next(data)[:3]]
        char_bits = [str(pixels[i] & 1) for i in range(8)]
        char = chr(int("".join(char_bits), 2))
        if char == chr(0):
            break
        message += char
    return message