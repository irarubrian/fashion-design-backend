from flask import Blueprint, request, jsonify
import requests
import base64
from datetime import datetime

mpesa_bp = Blueprint('mpesa', __name__)

# M-Pesa credentials (replace with your own)
consumer_key = 'ln4Vml8JYNsnHb79xP05pTz57ZvX21qf4G6ym9JR11HkpvEt'
consumer_secret = 'i6jfGgtgGeaOmCmF7DfdTTMZEge5pGkYaw5LRpxcAt0El0H3N5OHSAoVBYeyafq2'
business_short_code = '174379'
passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
callback_url = 'https://ec35-102-0-8-22.ngrok-free.app/callback'
def generate_access_token():
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    return response.json().get('access_token')

@mpesa_bp.route('/api/pay', methods=['POST'])
def lipa_na_mpesa_online():
    data = request.get_json()
    phone_number = data.get('phone')
    amount = data.get('amount')

    access_token = generate_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": "FashionShop",
        "TransactionDesc": "Payment for clothes"
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )
    return jsonify(response.json())

@mpesa_bp.route('/api/mpesa/callback', methods=['POST'])
def mpesa_callback():
    data = request.get_json()
    print("M-PESA Callback received:", data)

    try:
        result_code = data['Body']['stkCallback']['ResultCode']
        if result_code == 0:
            print("✅ Payment Successful")
            # You can update the order status here
        else:
            print("❌ Payment Failed or Cancelled")
    except KeyError:
        print("Invalid M-PESA callback format")

    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})
