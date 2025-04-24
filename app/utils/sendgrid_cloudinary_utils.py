import os
import cloudinary
import cloudinary.uploader
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv

# Load environment variables from .env file (ensure you've installed `python-dotenv`)
load_dotenv()

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# SendGrid Configuration
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# Function to upload image to Cloudinary
def upload_image(image_file):
    """
    Uploads an image to Cloudinary and returns the image URL.

    :param image_file: The image file (e.g., from a form or API request)
    :return: The secure URL of the uploaded image
    """
    try:
        response = cloudinary.uploader.upload(image_file)
        return response['secure_url']
    except Exception as e:
        print(f"Error uploading image to Cloudinary: {e}")
        return None

# Function to send an email via SendGrid
def send_email(to_email, subject, content):
    """
    Sends an email using SendGrid.

    :param to_email: The recipient email address
    :param subject: The email subject
    :param content: The email body content
    :return: SendGrid API response status code
    """
    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email("from-email@example.com")  # Replace with a real sender email
        to_email = To(to_email)
        content = Content("text/plain", content)
        mail = Mail(from_email, to_email, subject, content)
        response = sg.send(mail)
        return response.status_code
    except Exception as e:
        print(f"Error sending email via SendGrid: {e}")
        return None

# Example Usage
if __name__ == "__main__":
    # Example: Upload an image to Cloudinary
    image_path = "path/to/your/image.jpg"  # Replace with an actual image path
    cloudinary_url = upload_image(image_path)
    if cloudinary_url:
        print(f"Image uploaded to Cloudinary: {cloudinary_url}")

    # Example: Send an email via SendGrid
    email_status = send_email("recipient@example.com", "Test Subject", "This is a test email content.")
    if email_status:
        print(f"Email sent successfully, status code: {email_status}")
