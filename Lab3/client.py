import socket
import base64
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
 
def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12345))
        key = base64.b64decode(client_socket.recv(1024))  # Receive key from server
        aes_cipher = AESCipher(key)
        logging.info("Connected to server")
 
        while True:
            message = input("Client: ")
            client_socket.send(aes_cipher.encrypt(message).encode())
            encrypted_response = client_socket.recv(1024).decode()
            logging.info(f"Server: {aes_cipher.decrypt(encrypted_response)}")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        client_socket.close()
        logging.info("Client shutdown.")
 
if __name__ == "__main__":
    client()
 