import os
import io

def get_file_size_bytes(file):
    if isinstance(file, (str, os.PathLike)):
        return os.path.getsize(file)
    elif isinstance(file, io.BytesIO):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        return size
    else:
        raise TypeError("Input must be a file path or BytesIO object")

def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()
