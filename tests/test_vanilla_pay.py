import unittest
from unittest.mock import patch,MagicMock
from vanillapay import VanillaPay

class TestVanillaPay(unittest.TestCase):
    @patch('requests.get')
    def test_generate_token_success(self,mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value.status_code=200
        mock_response.json.return_value = {
            'CodeRetour': 'Success',
            'Data': {'Token': 'mock_token'}
        }

        mock_get.return_value = mock_response
        vanilla_pay=VanillaPay()

        token=vanilla_pay.generate_token()

        self.assertEqual(token,'mock_token')

    @patch('requests.get')
    def test_generate_token_failure(self,mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'DetailRetour':'Identifiants invalides'
        }

        mock_get.return_value=mock_response

        vanilla_pay=VanillaPay()
        with self.assertRaises(Exception) as context:
            vanilla_pay.generate_token()

        self.assertTrue('Error initializing payment' in str(context.exception))


    @patch('requests.post')
    def test_initialize_payment_success(self,mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'CodeRetour':200,
            'Data':{
                'url':'payment_link'
            }
        }

        mock_post.return_value = mock_response
        vanilla_pay=VanillaPay()
        token='mock_token'
        montant=100
        devise='EUR'
        reference='REF-001'
        panier='Cart01'
        notif_url='https//lien_milay.com/notify'
        redirect_url='https//lien_milay.com/redirect'


        payment_url=vanilla_pay.initialize_payment(
            token=token,
            montant=montant,
            devise=devise,
            reference=reference,
            panier=panier,
            notifUrl=notif_url,
            redirectUrl=redirect_url
        )

        self.assertEqual(payment_url,'payment_link')

    @patch('requests.post')
    def test_initialize_payment_failure(self,mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'DetailRetour':'Invalid request'
        }

        mock_post.return_value = mock_response
        vanilla_pay=VanillaPay()
        token='mock_token'
        montant=100
        devise='EUR'
        reference='REF-001'
        panier='Cart01'
        notif_url='https//lien_milay.com/notify'
        redirect_url='https//lien_milay.com/redirect'



        with self.assertRaises(Exception) as context:
            vanilla_pay.initialize_payment(
                token,montant,devise,reference,panier,notif_url,redirect_url
            )

        
        self.assertTrue('Error initializing payment' in str(context.exception))

    @patch('requests.get')
    def test_check_transactions_status_success(self,mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value.status_code=200
        mock_response.json.return_value = {
            'CodeRetour': 200,
            'DescRetour':'Transaction status',
            'DetailRetour':'',
            'Data': {
                'reference_VPI':'VPI24031510253820',
                'reference':'REF-0001',
                'remarque':'',
                'etat': 'SUCCESS',
                }
        }

        mock_get.return_value = mock_response
        vanilla_pay=VanillaPay()
        token='mock_token'

        payment_link = 'https://preprod.vanilla-pay.net/webpayment?id=eyJhbGciOiJIUzI1NiJ9.VlBJMjQwMzE1MTAyNTM4MjA.UWPypqD-LJwoFVUQp4vnq04NTOS4TG0ZSFVgFDx23-I'
        transaction_status = vanilla_pay.checkTransactionsStatus(token, payment_link)

        expected_status={
            'CodeRetour': 200,
            'DescRetour':'Transaction status',
            'DetailRetour':'',
            'Data': {
                'reference_VPI':'VPI24031510253820',
                'reference':'REF-0001',
                'remarque':'',
                'etat': 'SUCCESS',
                }
        }


        self.assertEqual(transaction_status,expected_status)


    @patch('requests.get')
    def test_check_transactions_status_failure(self,mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value.status_code=500
        mock_response.json.return_value = {
            'DetailRetour':'Token non valide'
        }

        mock_get.return_value = mock_response
        vanilla_pay=VanillaPay()
        token='mock_token'

        payment_link = 'https://preprod.vanilla-pay.net/webpayment?id=eyJhbGciOiJIUzI1NiJ9.VlBJMjQwMzE1MTAyNTM4MjA.UWPypqD-LJwoFVUQp4vnq04NTOS4TG0ZSFVgFDx23-I'
       
        with self.assertRaises(Exception) as context:
            vanilla_pay.checkTransactionsStatus(token, payment_link)
            
        self.assertTrue('Failed to check transaction status' in str(context.exception))



if __name__ == '__main__':
    unittest.main()


        
