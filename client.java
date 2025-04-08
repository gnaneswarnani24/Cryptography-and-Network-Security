import java.io.*;
import java.net.*;
public class client {
    public static String encrypt(String str, int key) {
        StringBuilder encrypted = new StringBuilder();
        for (int i = 0; i < str.length(); i++) {
            char currentChar = str.charAt(i);
            char plainChar = Character.toUpperCase(currentChar);
            char encryptedChar = (char) ('A' + (plainChar - 'A' + key) % 26);
            encrypted.append(encryptedChar);
        }
        return encrypted.toString();
    }
    public static void main(String[] args) {
        try (Socket socket = new Socket("localhost", 5000)) {
            System.out.println("Connected to the server.");

            DataInputStream input = new DataInputStream(socket.getInputStream());
            DataOutputStream output = new DataOutputStream(socket.getOutputStream());

            String plaintext = "wearediscoveredsaveyourself";
            System.out.println("Plaintext: " + plaintext);

            int key = 3; 
            String encryptedMessage = encrypt(plaintext, key);
            System.out.println("Encrypted Message: " + encryptedMessage);

            output.writeUTF(encryptedMessage);
            String response = input.readUTF();
            System.out.println("Server Response: " + response);

            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}