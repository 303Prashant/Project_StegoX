
# from Crypto.Cipher import AES
# import base64
# import hashlib
# from Crypto.Util.Padding import pad, unpad

# def encrypt_message(message: str, password: str) -> str:
#     key = hashlib.sha256(password.encode()).digest()
#     cipher = AES.new(key, AES.MODE_CBC)
#     ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
#     iv = base64.b64encode(cipher.iv).decode()
#     ct = base64.b64encode(ct_bytes).decode()
#     return iv + ":" + ct

# def decrypt_message(cipher_text: str, password: str) -> str:
#     try:
#         key = hashlib.sha256(password.encode()).digest()
#         iv, ct = cipher_text.split(":")
#         iv = base64.b64decode(iv)
#         ct = base64.b64decode(ct)
#         cipher = AES.new(key, AES.MODE_CBC, iv)
#         pt = unpad(cipher.decrypt(ct), AES.block_size)
#         return pt.decode()
#     except Exception:
#         raise ValueError("Decryption failed.")
