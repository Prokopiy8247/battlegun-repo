import requests
import json
import hashlib
import hmac
from decouple import config
from django.conf import settings

class NOWPaymentsService:
    API_URL = "https://api.nowpayments.io/v1"
    API_KEY = config('NOWPAYMENTS_API_KEY', default='')
    IPN_SECRET = config('NOWPAYMENTS_IPN_SECRET', default='')

    @classmethod
    def create_invoice(cls, order):
        """
        Creates an invoice for the given order.
        Returns the invoice data including invoice_url.
        """
        url = f"{cls.API_URL}/invoice"
        headers = {
            "x-api-key": cls.API_KEY,
            "Content-Type": "application/json"
        }
        
        # Build callback URL (IPN)
        # Assumes the site is accessible publicly. For local dev with ngrok, set ALLOWED_HOSTS/SITE_URL properly.
        # We'll use a placeholder or config for the domain.
        # For now, relative to the request logic in views, but here we need absolute URL.
        # We'll pass it or construct it. Let's assume we pass full URLs in payload or config.
        # tech.md suggests environment variables or constructing it.
        # Let's use a hardcoded base or config.
        base_url = config('SITE_URL', default='http://localhost:8000') 
        
        payload = {
            "price_amount": float(order.total),
            "price_currency": "eur", # tech.md implies EUR (from templates)
            "order_id": str(order.id),
            "order_description": f"Order {order.order_number}",
            "ipn_callback_url": f"{base_url}/payment/webhook/",
            "success_url": f"{base_url}/payment/success/{order.order_number}/",
            "cancel_url": f"{base_url}/payment/failed/{order.order_number}/",
             # "is_fixed_rate": True, # Optional
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    @classmethod
    def create_payment(cls, order, pay_currency="btc"):
        """
        Creates a direct payment.
        """
        url = f"{cls.API_URL}/payment"
        headers = {
            "x-api-key": cls.API_KEY,
            "Content-Type": "application/json"
        }
        
        base_url = config('SITE_URL', default='http://localhost:8000') 

        payload = {
            "price_amount": float(order.total),
            "price_currency": "eur",
            "pay_currency": pay_currency,
            "ipn_callback_url": f"{base_url}/payment/webhook/",
            "order_id": str(order.id),
            "order_description": f"Order {order.order_number}",
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    @classmethod
    def check_signature(cls, request_data, received_sig):
        """
        Verifies the IPN signature.
        """
        if not cls.IPN_SECRET:
            return False

        # Sort the dictionary by keys
        sorted_data = dict(sorted(request_data.items()))
        
        # Convert to JSON string - exact format matters! 
        # NOWPayments uses specific sorting and JSON dumps.
        # Python's json.dumps might add spaces.
        # According to docs: JSON.stringify(params, Object.keys(params).sort())
        # In Python: json.dumps(message, separators=(',', ':'), sort_keys=True)
        
        msg = json.dumps(sorted_data, separators=(',', ':'), sort_keys=True)
        
        digest = hmac.new(
            cls.IPN_SECRET.encode('utf-8'),
            msg.encode('utf-8'),
            hashlib.sha512
        )
        signature = digest.hexdigest()
        
        return signature == received_sig
