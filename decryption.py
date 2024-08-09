from cryptography.fernet import Fernet

def prompt(title):
    return input(title).strip()
    
# Function to decrypt the message
def decrypt_message(key, encrypted_message):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message)
    return decrypted_message.decode()

# Decrypts a file and prints the confirmation
def decrypt_file(key, encrypted_data, output_path):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(output_path, 'wb') as file:
        file.write(decrypted_data)
    print(f"File decrypted and saved to {output_path}")

# Decrypting an email body
if __name__ == "__main__":
    key = prompt('Enter your received key: ')  # Prompt for the key you received
    encrypted_message = prompt('Enter your encrypted message: ')  # Prompt for the encrypted message
    
    # Loop to handle multiple encrypted files
    while True:
        encrypted_file_path = prompt("Enter path to encrypted file (leave blank if none): ")  # Prompt for file path
        
        if encrypted_file_path:  # Checks if an encrypted file path was provided
            output_path = prompt("Enter path to save decrypted file: ")  # Prompts for the output file path
            with open(encrypted_file_path, 'rb') as file:
                encrypted_data = file.read()
            
            decrypt_file(key, encrypted_data, output_path)
        else:
            break  # Exit the loop if no file path is provided
        
        # Prompts if the user has another file to decrypt
        another_file = prompt("Do you have another encrypted file to decrypt with the same key? (yes/no): ").lower()
        if another_file != 'yes':
            break  # Exit the loop if the user does not have another file

    #Decrypt and display the message
    decrypted_message = decrypt_message(key, encrypted_message)
    print("Decrypted Message:", decrypted_message)