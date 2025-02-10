from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

key = os.urandom(16)

def encrypt(plain_text):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_text = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    return base64.b64encode(iv + encrypted_text).decode()

def decrypt(encrypted_text):
    encrypted_text = base64.b64decode(encrypted_text)
    iv = encrypted_text[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = unpad(cipher.decrypt(encrypted_text[16:]), AES.block_size)
    return decrypted_text.decode()

text = "Hello, AES Encryption!"
encrypted = encrypt(text)
decrypted = decrypt(encrypted)

print(f"Original Text: {text}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
