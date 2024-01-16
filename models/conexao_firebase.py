import firebase_admin
from firebase_admin import credentials, firestore
import json

def init_firestore():
    # Substitua 'path_to_your_service_account_file.json' pelo caminho do seu arquivo de credenciais
    cred = credentials.Certificate('db/apollo-7d70d-7f7936efda49.json')
    firebase_admin.initialize_app(cred)

def retrieve_data(collection_name):
    db = firestore.client()
    documents = db.collection(collection_name).stream()
    return [doc.to_dict() for doc in documents]

def test_retrieve_data():
    init_firestore()
    collection_name = 'act_330283615337074'  # Substitua pelo nome da sua coleção
    data = retrieve_data(collection_name)
    print(f"Data from {collection_name}:")
    print(json.dumps(data, indent=4))
      # Formata os dados como JSON com indentação

if __name__ == "__main__":
    test_retrieve_data()
