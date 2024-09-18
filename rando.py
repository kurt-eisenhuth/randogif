import smtplib
from email.mime.text import MIMEText
import requests
import getpass

# Carrier email gateways (you can add more as needed)
carrier_gateways = {
    'att': '@txt.att.net',
    'verizon': '@vtext.com',
    'tmobile': '@tmomail.net',
    # Add more carriers as needed
}

# Giphy API credentials (replace with your Giphy API key)
GIPHY_API_KEY = ''

# Function to get a random GIF URL from Giphy
def get_random_gif():
    url = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        gif_url = data['data']['images']['original']['url']
        return gif_url
    else:
        return None

# Function to send an email as an SMS
def send_sms_via_email(phone_number, carrier, gif_url, your_email, your_email_password):
    # Create the email body
    message_body = f"Here's a random GIF for you: {gif_url}"
    
    # Construct the carrier-specific email address
    to_email = f'{phone_number}{carrier_gateways[carrier]}'
    
    # Create a MIMEText object to represent the email
    msg = MIMEText(message_body)
    msg['From'] = your_email
    msg['To'] = to_email
    msg['Subject'] = 'Random GIF'
    
    # Send the email using SMTP
    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:  # Office 365 SMTP server
            server.starttls()  # Upgrade the connection to secure
            server.login(your_email, your_email_password)  # Log in to your email account
            server.sendmail(your_email, to_email, msg.as_string())  # Send the email
        print(f"Message sent to {phone_number} via {carrier}.")
    except smtplib.SMTPException as e:
        print(f"Failed to send message: {e}")


# Main logic
if __name__ == "__main__":
    # Prompt user for input
    your_email = input("Enter your email address: ")
    your_email_password = getpass.getpass("Enter your email password: ")
    phone_number = input("Enter the recipient's phone number: ")
    carrier = input("Enter the recipient's carrier (e.g., 'verizon'): ").lower()
    
    # Validate carrier
    if carrier not in carrier_gateways:
        print("Unsupported carrier. Please add the carrier to the carrier_gateways dictionary.")
    else:
        # Get a random GIF from Giphy
        gif_url = get_random_gif()
        
        if gif_url:
            send_sms_via_email(phone_number, carrier, gif_url, your_email, your_email_password)
        else:
            print("Failed to retrieve a random GIF.")