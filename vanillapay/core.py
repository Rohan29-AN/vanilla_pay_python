import json
import requests
import base64
from os import environ as environ


class VanillaPay:
    def __init__(
        self,
        client_id:str=env.get("CLIENT_ID"),
        client_secret:str=env.get("CLIENT_SECRET"),
        key_secret:str=env.get("KEY_SECRET"),
        vpi_version:str=env.get("VPI_VERSION"),
        status:str="PREPROD",
        token:str=None,
    ):
        """
            An library simplifies the process of integrating Vanilla Pay International payment functionalities

            Args:
                client_id (str): 
                client_secret (str):
                key_secret (str):
                vpi_version (str):
                status (str,optional) The status of your API
                (PREPROD: Developer Mode / PRODUCTION : Api deployé)
        """

        if not client_id:
            raise Exception("Missing CLIENT_ID in env")

        if not client_secret:
            raise Exception("Missing CLIENT_SECRET in env")
        
        if not key_secret:
            raise Exception("Missing KEY_SECRET in env")

        if not vpi_version:
            raise Exception("Missing VPI_VERSION in env")

        self.clientId=client_id
        self.clientSecret=client_secret
        self.vpiVersion=vpi_version
        self.key_secret=key_secret
        self.type=status
        self.token=token

        self.url=(
            "https://api.vanilla-pay.net"
            if self.type=="PRODUCTION"
            else "https://preprod.vanilla-pay.net"
        )
    
    def generate_token(self):
        """
            This function is used to generate the token used during transactins , which remains valid for 20 minutes
        """
        url=f"{self.url}/webpayment/token"
        headers={
            'Content-Type':'application/json',
            'Client-Id':'{self.clientId}',
            'Client-Secret':'{self.clientSecret}',
            'VPI-Version':'{self.vpiVersion}'
        }

        response=requests.get(url, headers=headers)

        if response.status_code == 200:
            print(response.json())
        
        else:
            print(f"Error: {response.status_code} - {response.reason}")

