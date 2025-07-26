from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key_from_password(password):
    password_bytes = password.encode()
    key = hashlib.sha256(password_bytes).digest()  # 32 bytes key
    return base64.urlsafe_b64encode(key)  # Fernet-compatible

def encrypt_message(message, password):
    key = generate_key_from_password(password)
    f = Fernet(key)
    encrypted = f.encrypt(message.encode())
    return encrypted.decode()  # string

def decrypt_message(encrypted_message, password):
    key = generate_key_from_password(password)
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_message.encode())
    return decrypted.decode()
