from PIL import Image
import numpy as np
import random
import base64

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join([chr(int(c, 2)) for c in chars])

def get_random_positions(width, height, num_bits, seed):
    total_pixels = width * height
    random.seed(seed)
    if num_bits > total_pixels:
        raise ValueError("Data too large to fit in the image.")
    positions = random.sample(range(total_pixels), num_bits)
    return positions

def encode_random_lsb(image: Image.Image, message: str, seed: str) -> Image.Image:
    bits = text_to_bits(message)
    width, height = image.size
    pixels = np.array(image).reshape(-1, 3)
    
    positions = get_random_positions(width, height, len(bits), seed)

    for i, bit in enumerate(bits):
        pixel_idx = positions[i]
        r, g, b = pixels[pixel_idx]
        b = (b & ~1) | int(bit)
        pixels[pixel_idx] = [r, g, b]

    new_pixels = pixels.reshape((height, width, 3))
    return Image.fromarray(new_pixels.astype(np.uint8))

def decode_random_lsb(image: Image.Image, num_chars: int, seed: str) -> str:
    width, height = image.size
    num_bits = num_chars * 8
    pixels = np.array(image).reshape(-1, 3)
    
    positions = get_random_positions(width, height, num_bits, seed)

    bits = ""
    for i in range(num_bits):
        pixel_idx = positions[i]
        b = pixels[pixel_idx][2]
        bits += str(b & 1)

    return bits_to_text(bits)

def file_to_base64(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode()

def base64_to_file(b64_data: str) -> bytes:
    return base64.b64decode(b64_data)