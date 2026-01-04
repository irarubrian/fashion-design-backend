from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import logging
import traceback
import os
from datetime import datetime

from extensions import db
from models import Order, Invoice

# --------------------
# LOGGING
# --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mpesa_bp = Blueprint("mpesa", __name__)

# --------------------
# M-PESA DISABLE SWITCH
# --------------------
MPESA_DISABLED = True   # 🔴 KEEP TRUE until Safaricom portal is back

# --------------------
# ENV CONFIG (SAFE)
# --------------------
MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")
MPESA_CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL")

# --------------------
# PAY ROUTE (DISABLED)
# --------------------
@mpesa_bp.route("/pay", methods=["POST"])
@cross_origin(supports_credentials=True)
def lipa_na_mpesa():
    """
    M-Pesa STK Push (TEMPORARILY DISABLED)
    """
    if MPESA_DISABLED:
        return jsonify({
            "success": False,
            "message": "M-Pesa service temporarily unavailable. Please try again later."
        }), 503

    # 🚨 This code will NOT run while MPESA_DISABLED = True
    try:
        data = request.get_json() or {}

        phone = data.get("phone")
        amount = data.get("amount")
        user_id = data.get("user_id")

        if not phone or not amount or not user_id:
            return jsonify({
                "success": False,
                "message": "phone, amount and user_id are required"
            }), 400

        # Order creation logic (safe placeholder)
        order = Order(
            user_id=user_id,
            payment_method="M-PESA",
            status="pending"
        )
        db.session.add(order)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Order created, awaiting M-Pesa activation",
            "order_id": order.id
        })

    except Exception:
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


# --------------------
# CALLBACK ROUTE (DISABLED)
# --------------------
@mpesa_bp.route("/callback", methods=["POST"])
@cross_origin(supports_credentials=True)
def mpesa_callback():
    """
    M-Pesa Callback (TEMPORARILY DISABLED)
    """
    if MPESA_DISABLED:
        return jsonify({
            "ResultCode": 0,
            "ResultDesc": "Service temporarily unavailable"
        })

    # 🚨 This code will NOT run while MPESA_DISABLED = True
    try:
        data = request.get_json() or {}

        callback = data.get("Body", {}).get("stkCallback", {})
        result_code = callback.get("ResultCode")
        checkout_request_id = callback.get("CheckoutRequestID")

        order = Order.query.filter_by(
            checkout_request_id=checkout_request_id
        ).first()

        if not order:
            return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

        if result_code == 0:
            order.status = "paid"

            invoice = Invoice(
                order_id=order.id,
                total_amount=order.amount if hasattr(order, "amount") else 0,
                issued_at=datetime.utcnow()
            )
            db.session.add(invoice)
        else:
            order.status = "failed"

        db.session.commit()

        return jsonify({
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        })

    except Exception:
        logger.error(traceback.format_exc())
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Rejected"
        }), 500
