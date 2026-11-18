import hmac
import hashlib
import uuid
import razorpay
from flask import current_app

class RazorpayService:
    @staticmethod
    def get_client():
        key_id = current_app.config.get('RAZORPAY_KEY_ID')
        key_secret = current_app.config.get('RAZORPAY_KEY_SECRET')
        if not key_id or not key_secret:
            return None
        return razorpay.Client(auth=(key_id, key_secret))

    @classmethod
    def create_order(cls, amount, receipt_id, currency='INR', notes=None):
        """
        Amount in INR (float/decimal). Razorpay expects amount in paise (1 INR = 100 paise).
        """
        amount_paise = int(round(float(amount) * 100))
        client = cls.get_client()

        if client:
            try:
                data = {
                    'amount': amount_paise,
                    'currency': currency,
                    'receipt': str(receipt_id),
                    'notes': notes or {'platform': "Karthik's Cart"}
                }
                order = client.order.create(data=data)
                return {
                    'id': order['id'],
                    'amount': amount,
                    'amount_paise': amount_paise,
                    'currency': currency,
                    'receipt': str(receipt_id),
                    'status': order.get('status', 'created'),
                    'is_live': True
                }
            except Exception as error:
                if current_app.config.get('IS_PRODUCTION'):
                    raise RuntimeError('Razorpay order creation failed.') from error
                current_app.logger.warning(
                    'Razorpay order creation failed; using local simulated checkout: %s',
                    error,
                )
        elif current_app.config.get('IS_PRODUCTION'):
            raise RuntimeError('Razorpay credentials are required for production payments.')

        # Robust test mode simulation (allows full end-to-end checkout testing without live keys)
        simulated_order_id = f"order_test_{uuid.uuid4().hex[:14]}"
        return {
            'id': simulated_order_id,
            'amount': float(amount),
            'amount_paise': amount_paise,
            'currency': currency,
            'receipt': str(receipt_id),
            'status': 'created',
            'is_live': False
        }

    @classmethod
    def verify_payment_signature(cls, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        """
        Verifies Razorpay HMAC SHA256 payment signature.
        """
        key_secret = current_app.config.get('RAZORPAY_KEY_SECRET', '')
        
        # Simulated checkout is available only in development and still verifies its HMAC.
        if razorpay_order_id.startswith('order_test_'):
            if current_app.config.get('IS_PRODUCTION'):
                return False
            expected_signature = hmac.new(
                key_secret.encode('utf-8'),
                f"{razorpay_order_id}|{razorpay_payment_id}".encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            return hmac.compare_digest(expected_signature, razorpay_signature)

        if not key_secret:
            return False

        client = cls.get_client()
        if client:
            try:
                client.utility.verify_payment_signature({
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature
                })
                return True
            except razorpay.errors.SignatureVerificationError:
                return False

        # Standard HMAC SHA256 verification
        generated_signature = hmac.new(
            key_secret.encode('utf-8'),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(generated_signature, razorpay_signature)
