import firebase_admin
from firebase_admin import credentials, firestore
import time
from firebase_admin import firestore
from google.cloud.exceptions import GoogleCloudError

def init_firestore():
    # Inicialize o Firebase aqui. Garanta que isso seja feito apenas uma vez.
    cred = credentials.Certificate('db/apollo-7d70d-7f7936efda49.json')
    firebase_admin.initialize_app(cred)

def store_data(account_id, campaign_data, ad_sets_data, ads_data):
    try:
        db = firestore.client()
        account_ref = db.collection(account_id)
        
        for campaign in campaign_data:
            campaign_ref = account_ref.document(campaign['id'])
            campaign_ref.set(campaign)
            
            ad_sets_ref = campaign_ref.collection('ad_sets')
            for ad_set in ad_sets_data:
                # Verifique se ad_set tem 'campaign_id' e se corresponde ao 'id' da campanha
                if 'campaign_id' in ad_set:
                    if ad_set.get('campaign_id') == campaign['id']:
                        ad_set_ref = ad_sets_ref.document(ad_set['id'])
                        ad_set_ref.set(ad_set)
                        
                        ads_ref = ad_set_ref.collection('ads')
                        for ad in ads_data:
                            # Verifique se ad tem 'adset_id' e se corresponde ao 'id' do conjunto de anúncios
                            if ad.get('adset_id') == ad_set['id']:
                                ad_ref = ads_ref.document(ad['id'])
                                ad_ref.set(ad)
    except Exception as e:
        print(f"Erro inesperado: {e}")


def store_change_logs(collection_name, change_logs):
    db = firestore.client()
    for log in change_logs:
        # Você pode usar um identificador único, como um timestamp ou um ID gerado.
        doc_id = f"log_{int(time.time())}"
        db.collection(collection_name).document(doc_id).set(log)


