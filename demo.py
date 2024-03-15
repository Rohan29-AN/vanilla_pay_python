from vanillapay import VanillaPay
import threading
from dotenv import load_dotenv
import os
import sys
from vanillapay.tools import hash_data

load_dotenv()

if os.getenv("CLIENT_ID") and os.getenv("CLIENT_SECRET") and os.getenv("KEY_SECRET"):
    api=VanillaPay()
    print("Welcome to Vanilla Pay")
else:
    print(
        "VanillaPay error: Verify if you have .env file"
    )
    sys.exit()

#Generate Token

try:
    generatedToken=api.generate_token()
    print(f"Your token:  {generatedToken}")

    paymentLink=api.initialize_payment(token=generatedToken,montant=10,devise='EUR',reference='REF-0001',panier='PANIER-01',notifUrl='https://google.com',redirectUrl='https://google.com')
    print(f"Your payment link: {paymentLink}")

    paymentStatus=api.checkTransactionsStatus(token=generatedToken,paymentLink="https://preprod.vanilla-pay.net/webpayment?id=eyJhbGciOiJIUzI1NiJ9.VlBJMjQwMzE1MTAyNTM4MjA.UWPypqD-LJwoFVUQp4vnq04NTOS4TG0ZSFVgFDx23-I")
    print(f"Payment Status: {paymentStatus}")

    hashed_data=hash_data('shutt','vanilla pay international')
    print(f"Hashed data: {hashed_data}")
except Exception as e:
    print(f"{e}")



