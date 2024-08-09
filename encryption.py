import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet
from email.mime.application import MIMEApplication
import os

# Requests and returns the input
def prompt(title):
    return input(title).strip()
    
# Generates and returns an encryption key
def generate_key():
    return Fernet.generate_key()

# Encrypts the message with the generated encryption key
def encrypt_message(key, message):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

#Encrypts the attached files
def encrypt_file(key, file_path):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    return encrypted_data

# Sends the encrypted mail
def send_encrypted_email(sender_email, sender_password, receiver_email, subject, encrypted_body, key, attachment_paths):
    # Create sthe email headers and multipart messages
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attaching the encrypted body
    body_part = MIMEText(encrypted_body.decode(), 'plain')
    msg.attach(body_part)
    
    # Attaches the files and encrypts them
    for file_path in attachment_paths:
        if os.path.exists(file_path):
            encrypted_data = encrypt_file(key, file_path)
            attachment_part = MIMEApplication(encrypted_data, Name=os.path.basename(file_path)+'.enc')
            attachment_part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}.enc"'
            msg.attach(attachment_part)

    # Attaching the encryption key as a file (optional and is preferred)
    key_attachment = MIMEApplication(key, Name='encryption_key.key')
    msg.attach(key_attachment)

    # Sends the email via SMTP server
    try:
        #Input your server details
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server: # Currently gmail is being used as the server
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Encrypted email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main code
if __name__ == "__main__":
    #Prompts for the email id and password to send from
    sender_email = prompt("Email Id: ")
    sender_password = prompt("Password: ") #App password is required if using gmail as the server
    receiver_email = prompt("To: ") #To address
    subject = prompt("Subject: ") #Subject
    
    # Prompts for the Message to be encrypted
    message = prompt("Body: ")

    #Prompts for the attachment paths
    attachment_paths_input = prompt("Attachment Paths (comma-separated): ")
    attachment_paths = [path.strip() for path in attachment_paths_input.split(',')] if attachment_paths_input else []

    # Generating the encryption key
    key = generate_key()
    
    # Encrypting the message
    encrypted_body = encrypt_message(key, message)
    
    # Sending the encrypted email
    send_encrypted_email(sender_email, sender_password, receiver_email, subject, encrypted_body, key, attachment_paths)
