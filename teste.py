import unittest
from facebook_business.api import FacebookAdsApi
from unittest.mock import patch
from models import facebook_services, firestone_services
from app import app

class TestFacebookAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app_id = '677752197796360'
        app_secret = 'b4ddf1dd78d1fd88ee6d251f47dfd11e'
        access_token = 'EAAJoaXrZB0ggBO2xgy27MiVazt0XHj4h3NCboAdoCpC8CnGdVZACXSwUxDo0IfPUEU02ZCphBU5I2JMF4qXBZByt6A8iZAD0mhVc9LWdrZAQZAPkos8ZBvr97LUZAP5SOFPExQZAO4SYwDItRYlVOmYiNqIL9TdZC0KgZAeOoYekNnQRTAaxXLH8AZA1hFN4KBxVJB0UR'
        FacebookAdsApi.init(app_id, app_secret, access_token)



    def test_get_campaigns(self):
        campaigns = facebook_services.get_campaigns('act_104028533759661')
        self.assertIsNotNone(campaigns)
        # Verifique se o retorno é uma lista e possui os campos esperados
        self.assertTrue(isinstance(campaigns, list))
        if campaigns:  # Verifica se a lista não está vazia
            self.assertIn('id', campaigns[0])
            self.assertIn('name', campaigns[0])


    def test_get_ad_sets(self):
        ad_sets = facebook_services.get_ad_sets('act_104028533759661')
        self.assertIsNotNone(ad_sets)

    def test_get_ads(self):
        ads = facebook_services.get_ads('act_104028533759661')
        self.assertIsNotNone(ads)

class TestFirestoneServices(unittest.TestCase):

    @patch('firebase_admin.firestore.client')
    def test_store_data(self, mock_firestore_client):
        mock_db = mock_firestore_client.return_value
        mock_collection = mock_db.collection.return_value
        mock_document = mock_collection.document.return_value

        account_id = 'test_account_id'
        campaign_data = [{'id': '123', 'name': 'Test Campaign'}]
        ad_sets_data = [{'id': '456', 'name': 'Test AdSet'}]
        ads_data = [{'id': '789', 'name': 'Test Ad'}]

        firestone_services.store_data(account_id, campaign_data, ad_sets_data, ads_data)
        mock_db.collection.assert_called_with(account_id)
        mock_document.set.assert_called()

class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
