import cloudinary
import cloudinary.uploader
import sendgrid
from sendgrid.helpers.mail import Mail

cloudinary.config(
    cloud_name='your-cloud-name',
    api_key='your-api-key',
    api_secret='your-api-secret'
)

SENDGRID_API_KEY = 'your-sendgrid-key'

def upload_image(file):
    result = cloudinary.uploader.upload(file)
    return result['secure_url']

def send_email(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    mail = Mail(from_email='no-reply@yourshop.com', to_emails=to_email,
                subject=subject, html_content=content)
    return sg.send(mail)