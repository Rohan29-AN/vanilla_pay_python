from dotenv import load_dotenv
import json
import requests
import base64
import os
from . import tools

class VanillaPay:
    def __init__(
        self,
        status:str="PREPROD"
    ):
        """
            An library simplifies the process of integrating Vanilla Pay International payment functionalities

            Args:
                status (str, optional): The status of the API.
                    Possible values are 'PREPROD' for Developer Mode and 'PRODUCTION' for deployed API.
                    Defaults to 'PREPROD'.
        """
        load_dotenv()
        
        self.clientId = os.getenv("CLIENT_ID")
        self.clientSecret = os.getenv("CLIENT_SECRET")
        self.keySecret = os.getenv("KEY_SECRET")
        self.vpiVersion = os.getenv("VPI_VERSION")
       

        if not self.clientId:
            raise Exception("Missing CLIENT_ID in env")

        if not self.clientSecret:
            raise Exception("Missing CLIENT_SECRET in env")
        
        if not self.keySecret:
            raise Exception("Missing KEY_SECRET in env")

        if not self.vpiVersion:
            raise Exception("Missing VPI_VERSION in env")

        self.type=status

        self.url=(
            "https://api.vanilla-pay.net"
            if self.type=="PROD"
            else "https://preprod.vanilla-pay.net"
        )
    
    def generate_token(self):
        """
            This function is used to generate the token used during transactins , which remains valid for 20 minutes
        """
        url=f"{self.url}/webpayment/token"

        headers={
            'Content-Type':'application/json',
            'Client-Id':self.clientId,
            'Client-Secret':self.clientSecret,
            'VPI-Version':self.vpiVersion
        }

        response=requests.get(url, headers=headers)

        if response.status_code == 200:
            data=response.json()
            code_retour=data.get('CodeRetour') 
            return data.get('Data').get('Token')


        else:
             detail_retour = response.json().get('DetailRetour')
             if detail_retour is not None and detail_retour != '': 
                raise Exception(f"Error initializing payment: {response.status_code} - {response.reason} - {detail_retour}")
             else:
                raise Exception(f"Error initializing payment: {response.status_code} - {response.reason}")


    def initialize_payment(self,token,montant,devise,reference,panier,notifUrl,redirectUrl):
        """
        Initiates a payment process by generating a payment link for the customer to access and complete the payment.

        Args:
            userToken (str): The generated token used for authentication and authorization
            montant (float): The amount of the transaction.
            devise (str): The currency of the payment.
            reference (str): The external reference associated with the transaction.
            panier (str): The identifier for the transaction.
            notifUrl (str): The URL to be called when the payment is finished.
            redirectUrl (str): The redirect URL after payment completion.
        """
        url=f"{self.url}/webpayment/token"

        headers={
            'Content-Type':'application/json',
            'Client-Id':self.clientId,
            'Client-Secret':self.clientSecret,
            'VPI-Version':self.vpiVersion,
            'Authorization': token
        }

        body = {
            'montant': montant,
            'devise': devise,
            'reference': reference,
            'panier': panier,
            'notifUrl': notifUrl,
            'redirectUrl': redirectUrl
        }   

        json_body=json.dumps(body)

        url=f"{self.url}/webpayment/initiate"
        response = requests.post(url, headers=headers, data=json_body)
        if response.status_code == 200:
            data=response.json()
            code_retour=data.get('CodeRetour')
            return data.get('Data').get('url')
            
        else:
             detail_retour = response.json().get('DetailRetour')

             if detail_retour is not None and detail_retour != '':

                raise Exception(f"Error initializing payment: {response.status_code} - {response.reason} - {detail_retour}")
             else:
                raise Exception(f"Error initializing payment: {response.status_code} - {response.reason}")

    def checkTransactionsStatus(self,token,paymentLink):
         """
             Retrieves the status of a transaction using the provided payment link.
            Args:
            token (str): The generated token used for authentication and authorization
            paymentLink (str): The payment link associated with the transaction.
        """

         id_value = tools.extract_id_from_url(paymentLink)
         url=f"{self.url}/webpayment/status/{id_value}"

         print(f"ID VALUE: {id_value}")
         print(f"URL : {url}")
         headers={
            'VPI-Version':self.vpiVersion,
            'Authorization': token
        }

         print(headers)

         response=requests.get(url, headers=headers)

         if response.status_code == 200:
            data=response.json()
            code_retour=data.get('CodeRetour') 
            print(data)
         else:
             print(response.json())
             detail_retour = response.json().get('DetailRetour')
             if detail_retour is not None and detail_retour != '': 
                raise Exception(f"Failed to check transaction status: {response.status_code} - {response.reason} - {detail_retour}")
             else:
                raise Exception(f"Failed to check transaction status: {response.status_code} - {response.reason}")

    def validate_data_authenticity(self,vpi_signature, body):
        """
            Validates the authenticity of the provided data by verifying the signature
            against the hashed body using the client secret.

            Args:
                vpi_signature (str): The signature extracted from the headers.
                body (str): The data to be hashed and compared against the signature.
                client_secret (str): The secret key used for hashing and signature verification.
            
            Returns:
                bool: True if the data is authentic, otherwise False.
        """
        # Hash the provided body using the KeySecret
        hashed_data = tools.hash_data(self.keySecret, body)
        # Compare the hashed body with the provided signature
        return hashed_data == vpi_signature