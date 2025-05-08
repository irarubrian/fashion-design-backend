from flask import Blueprint, request, jsonify, session, current_app
import requests
import base64
from datetime import datetime
import logging
import traceback
from extensions import db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mpesa_bp = Blueprint('mpesa', __name__)

# M-Pesa credentials (replace with your own)
consumer_key = 'ln4Vml8JYNsnHb79xP05pTz57ZvX21qf4G6ym9JR11HkpvEt'
consumer_secret = 'i6jfGgtgGeaOmCmF7DfdTTMZEge5pGkYaw5LRpxcAt0El0H3N5OHSAoVBYeyafq2'
business_short_code = '174379'
passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
callback_url = 'https://ec35-102-0-8-22.ngrok-free.app/api/mpesa/callback'

def generate_access_token():
    try:
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
        json_response = response.json()
        logger.info(f"M-PESA token response: {json_response}")
        return json_response.get('access_token')
    except Exception as e:
        logger.error(f"Error generating M-PESA access token: {str(e)}")
        logger.error(traceback.format_exc())
        return None

@mpesa_bp.route('/pay', methods=['POST', 'OPTIONS'])
def lipa_na_mpesa_online():
    if request.method == 'OPTIONS':
        return jsonify({'success': True})
        
    try:
        # Import models here to avoid circular imports
        from models.models import User, Order, Invoice
        
        data = request.get_json()
        logger.info(f"M-PESA payment request data: {data}")
        
        phone_number = data.get('phone')
        amount = data.get('amount')
        user_id = session.get('user_id')
        
        logger.info(f"M-PESA payment request: Phone: {phone_number}, Amount: {amount}, User ID: {user_id}")
        
        # For testing purposes, allow payments without authentication
        if not user_id:
            user_id = 1  # Use a default user ID for testing
            logger.warning("No user ID in session, using default user ID for testing")
        
        if not phone_number or not amount:
            logger.error("Missing phone number or amount")
            return jsonify({'success': False, 'message': 'Phone number and amount are required'}), 400
        
        # Format phone number (ensure it starts with 254)
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif not phone_number.startswith('254'):
            phone_number = '254' + phone_number
        
        logger.info(f"Formatted phone number: {phone_number}")
        
        access_token = generate_access_token()
        if not access_token:
            logger.error("Failed to generate M-PESA access token")
            return jsonify({'success': False, 'message': 'Failed to generate M-PESA access token'}), 500
            
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
            "Amount": int(float(amount)),
            "PartyA": phone_number,
            "PartyB": business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": f"FashionShop-{user_id}",
            "TransactionDesc": "Payment for clothes"
        }

        logger.info(f"M-PESA API request payload: {payload}")

        try:
            response = requests.post(
                "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers
            )
            
            logger.info(f"M-PESA API response status: {response.status_code}")
            logger.info(f"M-PESA API response: {response.text}")
            
            # Create a pending order
            order = Order(
                user_id=user_id,
                payment_method='M-PESA',
                status='pending'
            )
            db.session.add(order)
            db.session.commit()
            
            # Return the M-Pesa response along with the order ID
            try:
                mpesa_response = response.json()
                return jsonify({
                    'success': True,
                    'order_id': order.id,
                    'mpesa_response': mpesa_response
                })
            except Exception as e:
                logger.error(f"Error parsing M-PESA API response: {str(e)}")
                return jsonify({
                    'success': True,
                    'order_id': order.id,
                    'message': 'Payment request sent, but could not parse response'
                })
                
        except Exception as e:
            logger.error(f"Error making M-PESA API request: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({'success': False, 'message': f'Error making M-PESA API request: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Unexpected error in M-PESA payment: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

@mpesa_bp.route('/callback', methods=['POST'])
def mpesa_callback():
    try:
        # Import models here to avoid circular imports
        from models.models import Order, Invoice
        
        data = request.get_json()
        logger.info(f"M-PESA callback received: {data}")
        
        callback_data = data.get('Body', {}).get('stkCallback', {})
        result_code = callback_data.get('ResultCode')
        merchant_request_id = callback_data.get('MerchantRequestID')
        checkout_request_id = callback_data.get('CheckoutRequestID')
        
        # Find the order associated with this transaction
        # In a real app, you'd store the checkout_request_id with the order
        # For this example, we'll just update the most recent pending order
        order = Order.query.filter_by(status='pending').order_by(Order.created_at.desc()).first()
        
        if order:
            if result_code == 0:
                # Payment successful
                order.status = 'paid'
                db.session.commit()
                logger.info(f"M-PESA payment successful for order ID: {order.id}")
                
                # You could also create an invoice here
                
                return jsonify({
                    "ResultCode": 0,
                    "ResultDesc": "Accepted"
                })
            else:
                # Payment failed
                order.status = 'failed'
                db.session.commit()
                logger.info(f"M-PESA payment failed for order ID: {order.id}")
        
        return jsonify({
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        })
    except Exception as e:
        logger.error(f"Error processing M-PESA callback: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Rejected"
        }), 500
