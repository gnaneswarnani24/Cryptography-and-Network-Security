import java.io.*;
import java.net.*;

public class server {

    public static String createPlayfairMatrix(String key) {
        StringBuilder matrix = new StringBuilder();
        boolean[] used = new boolean[26];
        key = key.toUpperCase().replaceAll("[^A-Z]", "").replace("J", "I"); // Clean key and treat 'J' as 'I'
        
        // Add key letters to matrix
        for (char c : key.toCharArray()) {
            if (!used[c - 'A']) {
                matrix.append(c);
                used[c - 'A'] = true;
            }
        }
        
        // Add remaining letters of the alphabet
        for (char c = 'A'; c <= 'Z'; c++) {
            if (!used[c - 'A']) {
                matrix.append(c);
                used[c - 'A'] = true;
            }
        }
        
        return matrix.toString();
    }

    public static String[] digraphs(String text) {
        text = text.toUpperCase().replaceAll("[^A-Z]", "").replace("J", "I");
        if (text.length() % 2 != 0) text += "X"; // If odd length, add filler character 'X'

        String[] digraphs = new String[text.length() / 2];
        for (int i = 0; i < text.length(); i += 2) {
            digraphs[i / 2] = text.substring(i, i + 2);
        }
        return digraphs;
    }

    public static String decrypt(String cipherText, String key) {
        String matrix = createPlayfairMatrix(key);
        String[] digraphs = digraphs(cipherText);
        StringBuilder decryptedText = new StringBuilder();
        
        for (String digraph : digraphs) {
            int pos1 = matrix.indexOf(String.valueOf(digraph.charAt(0)));
            int pos2 = matrix.indexOf(String.valueOf(digraph.charAt(1)));
            
            int row1 = pos1 / 5, col1 = pos1 % 5;
            int row2 = pos2 / 5, col2 = pos2 % 5;

            // If they are in the same row
            if (row1 == row2) {
                decryptedText.append(matrix.charAt(row1 * 5 + (col1 - 1 + 5) % 5));
                decryptedText.append(matrix.charAt(row2 * 5 + (col2 - 1 + 5) % 5));
            }
            // If they are in the same column
            else if (col1 == col2) {
                decryptedText.append(matrix.charAt(((row1 - 1 + 5) % 5) * 5 + col1));
                decryptedText.append(matrix.charAt(((row2 - 1 + 5) % 5) * 5 + col2));
            }
            // If they form a rectangle
            else {
                decryptedText.append(matrix.charAt(row1 * 5 + col2));
                decryptedText.append(matrix.charAt(row2 * 5 + col1));
            }
        }
        
        return decryptedText.toString();
    }

    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(5000)) {
            System.out.println("Server is listening on port 5000");
            Socket socket = serverSocket.accept();
            System.out.println("Client connected.");
            DataInputStream input = new DataInputStream(socket.getInputStream());
            DataOutputStream output = new DataOutputStream(socket.getOutputStream());
            String receivedCipher = input.readUTF();
            System.out.println("Received Cipher Text: " + receivedCipher);
            String key = "KEY"; // You can modify the key as needed
            String decryptedMessage = decrypt(receivedCipher, key);
            System.out.println("Decrypted Message: " + decryptedMessage);
            output.writeUTF("Message Received and Decrypted");
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}