import socket
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import logging
 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
class AESCipher:
    def __init__(self, key):
        self.key = key
 
    def encrypt(self, message):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + ciphertext).decode()
 
    def decrypt(self, encrypted_message):
        raw_data = base64.b64decode(encrypted_message)
        iv, ciphertext = raw_data[:16], raw_data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
 
def generate_key():
    return os.urandom(16)  
 
def server():
    key = generate_key()
    aes_cipher = AESCipher(key)
    logging.info(f"Server AES Key (Share with Client): {base64.b64encode(key).decode()}")
 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    logging.info("Server listening on port 12345...")
 
    try:
        conn, addr = server_socket.accept()
        logging.info(f"Connection from {addr}")
        conn.send(base64.b64encode(key))  # Send encryption key to client
 
        while True:
            encrypted_data = conn.recv(1024).decode()
            if not encrypted_data:
                break
            decrypted_data = aes_cipher.decrypt(encrypted_data)
            logging.info(f"Client: {decrypted_data}")
 
            response = input("Server: ")
            conn.send(aes_cipher.encrypt(response).encode())
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        conn.close()
        server_socket.close()
        logging.info("Server shutdown.")
 
if __name__ == "__main__":
    server()
