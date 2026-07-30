import base64
from datetime import datetime
import requests


class MpesaPayment:

    def __init__(self):
        # Daraja App Credentials
        self.consumer_key = "MIv6hg1KB3SEPTqynNurOkeeKEIimNGfEXgNZPVocNGxNBFM"
        self.consumer_secret = "hThkL2P74XWz6GM1AqIR90CHuq8qp6Z557YJ5TCocGBLX7JgM7IV1aVGMUYrx1wf"

        # B2C Credentials
        self.initiator = "testapi"
        self.security_credential = "pF+8+QdfkVrCQ9K4xscn2tDNIw9qB+XHbBzkXV9NLPHHMjPmyJcslP2Nsl4YZJRCUAjKrs5RonkMCZb1kh0A7LH+QCkgk9oj0XXfYR0sj4AphE60R0jj3gg2FlIzOM1o7Gt/eayGI22UQvUQeMy1wB5eS7rlxB43iNHyqjf/yMjzG3lECwPfTIMrAaYWlsWmj521TmQfVHp0q4obvX6cejZM/vBL+aDtXltjyARnKflA07vquRkPDQF4d6T2DB6oe10NA9mRRRo4r2Y973axmXpJV6kAr9M4WT4rerONKTjWfz0Tz5hgCoZo1tpZi+U0Q/xNav4gwnsMnIJYZRkGvg=="

        # URLs
        self.token_url = (
            "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        )

        self.b2c_url = (
            "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
        )

        self.stk_url = (
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        )

        # Callback URLs
        self.b2c_callback_url = (
            "https://extrude-defeat-dirtiness.ngrok-free.dev/api/payments/b2c/callback"
        )

        self.stk_callback_url = (
            "https://extrude-defeat-dirtiness.ngrok-free.dev/api/payments/stk/callback"
        )

        # Sandbox Shortcode & Passkey
        self.shortcode = "174379"

        self.passkey = ("bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919")

    def get_token(self):
        response = requests.get(
            self.token_url,
            auth=requests.auth.HTTPBasicAuth(
                self.consumer_key,
                self.consumer_secret,
            ),
            timeout=30,
        )

        print("Token Status:", response.status_code)
        print("Token Response:", response.text)

        response.raise_for_status()

        token = response.json()["access_token"]

        return token

    def pay_deliverer(self, phone, amount):
        token = self.get_token()

        payload = {
            "Initiator": self.initiator,
            "SecurityCredential": self.security_credential,
            "CommandID": "BusinessPayment",
            "Amount": amount,
            "PartyA": "600982",
            "PartyB": "600000",
            "SenderIdentifierType": "4",
            "ReceiverIdentifierType": "4",
            "AccountReference": "ORDERS",
            "Remarks": "Order Payment",
            "QueueTimeOutURL": self.b2c_callback_url,
            "ResultURL": self.b2c_callback_url,
        }

        response = requests.post(
            self.b2c_url,
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

        print(response.status_code)
        print(response.text)

        return response.json()

    def customer_payment(self, phone, amount, order_id):
        print(f" phone:{phone}  amount: {amount} orderid:{order_id}" )
        print("Customer Payment Function")

        token = self.get_token()

        # Convert phone number to 254XXXXXXXXX format
        phone = phone.strip()

        if phone.startswith("+"):
            phone = phone[1:]

        if phone.startswith("0"):
            phone = "254" + phone[1:]

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        password = base64.b64encode(
            f"{self.shortcode}{self.passkey}{timestamp}".encode("utf-8")
        ).decode("utf-8")

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",
            "PartyA": phone,
            "PartyB": self.shortcode,
            "PhoneNumber": phone,
            "CallBackURL": self.stk_callback_url,
            "AccountReference": str(order_id),
            "TransactionDesc": "Order Payment",
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        print("\n========== STK REQUEST ==========")
        print("URL:", self.stk_url)
        print("Headers:", headers)
        print("Payload:", payload)

        response = requests.post(
            self.stk_url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        print("\n========== STK RESPONSE ==========")
        print("Status:", response.status_code)
        print("Response:", response.text)

        return response.json()
