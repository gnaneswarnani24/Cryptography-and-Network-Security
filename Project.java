import java.io.*;
import java.net.*;

public class Project {
    // Decrypt function for Caesar Cipher
    public static String decrypt(String str, int k) {
        StringBuilder decrypted = new StringBuilder();
        for (int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            if (Character.isLetter(c)) { // Handle only letters
                char base = Character.isUpperCase(c) ? 'A' : 'a';
                char ans = (char) (base + (c - base - k + 26) % 26);
                decrypted.append(ans);
            } else {
                decrypted.append(c); // Append non-alphabetic characters as-is
            }
        }
        return decrypted.toString();
    }

    public static void main(String[] args) {
        int port = 3080; // Port number
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Server is running on port " + port + " and waiting for a connection...");

            try (Socket socket = serverSocket.accept();
                DataInputStream input = new DataInputStream(socket.getInputStream())) {

                System.out.println("Client connected.");

                // Read the encrypted message from the client
                String receivedMessage = input.readUTF();
                System.out.println("CIPHER from client: " + receivedMessage);

                // Decrypt the message
                String decryptedMessage = decrypt(receivedMessage, 2);
                System.out.println("Decrypted Message: " + decryptedMessage);
            }
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
