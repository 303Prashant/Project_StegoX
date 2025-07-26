import wave
import io

def get_max_audio_capacity(audio_bytes):
    audio_bytes.seek(0)
    with wave.open(audio_bytes, 'rb') as audio:
        total_bytes = len(audio.readframes(audio.getnframes()))
    return total_bytes - 8  # reserve 8 bytes for file size

def embed_file_in_audio(audio_bytes, file_bytes, file_name):
    audio_bytes.seek(0)
    file_bytes.seek(0)

    with wave.open(audio_bytes, 'rb') as audio:
        audio_params = audio.getparams()
        audio_frames = bytearray(audio.readframes(audio.getnframes()))

    file_data = file_bytes.read()
    file_size = len(file_data)
    file_name_bytes = file_name.encode()
    name_length = len(file_name_bytes)

    # total = 8 bytes size + 2 bytes name length + name + data
    total_required = 8 + 2 + name_length + file_size
    max_capacity = len(audio_frames)

    if total_required > max_capacity:
        raise ValueError(f"File too large! Max = {(max_capacity - 10) / 1024:.2f} KB")

    audio_frames[0:8] = file_size.to_bytes(8, 'big')
    audio_frames[8:10] = name_length.to_bytes(2, 'big')
    audio_frames[10:10 + name_length] = file_name_bytes
    audio_frames[10 + name_length:10 + name_length + file_size] = file_data

    stego_audio = io.BytesIO()
    with wave.open(stego_audio, 'wb') as audio_out:
        audio_out.setparams(audio_params)
        audio_out.writeframes(audio_frames)

    stego_audio.seek(0)
    return stego_audio

def extract_file_from_audio(audio_bytes):
    audio_bytes.seek(0)
    with wave.open(audio_bytes, 'rb') as audio:
        audio_frames = bytearray(audio.readframes(audio.getnframes()))

    file_size = int.from_bytes(audio_frames[0:8], 'big')
    name_length = int.from_bytes(audio_frames[8:10], 'big')
    file_name = audio_frames[10:10 + name_length].decode()
    file_data = bytes(audio_frames[10 + name_length : 10 + name_length + file_size])

    return file_name, io.BytesIO(file_data)
