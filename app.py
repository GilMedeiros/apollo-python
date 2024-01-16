from flask import Flask, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler

# Configuração de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
file_handler = RotatingFileHandler('logs/app_logs.log', maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
logger.addHandler(file_handler)

logger.info('Aplicativo iniciado')

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o Flask
app = Flask(__name__)

# Inicializar o Firebase
from models.firestone_services import init_firestore
init_firestore()

# Importar as outras funções
from models.facebook_services import init_facebook_session_and_get_ad_accounts, get_campaigns, get_ad_sets, get_ads
from models.firestone_services import store_data
from facebook_business.exceptions import FacebookRequestError
from models.conexao_firebase import retrieve_data

# Carregar as credenciais do Facebook
app_id = os.getenv('FACEBOOK_APP_ID')
app_secret = os.getenv('FACEBOOK_APP_SECRET')
access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
ad_accounts = init_facebook_session_and_get_ad_accounts(app_id, app_secret, access_token)
current_ad_account = ad_accounts[0]['id']

# Monitor de chamadas da API
class ApiCallMonitor:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def add_call(self):
        now = datetime.now()
        self.calls.append(now)
        self.calls = [call for call in self.calls if now - call < self.period]

    def can_make_call(self):
        return len(self.calls) < self.max_calls

monitor = ApiCallMonitor(max_calls=400, period=timedelta(hours=1))

@app.route('/')
def index():
    return render_template('page-one.html')

@app.route('/get_ad_accounts')
def get_ad_accounts():
    ad_accounts = init_facebook_session_and_get_ad_accounts(app_id, app_secret, access_token)
    ad_accounts_list = [{'id': acc['id'], 'name': acc['name']} for acc in ad_accounts]
    return jsonify(ad_accounts_list)

# Função separada para buscar e armazenar dados de campanha
def fetch_and_store_data(account_id):
    if not monitor.can_make_call():
        return {'status': 'error', 'message': 'API call limit reached'}, 429

    try:
        monitor.add_call()
        campaign_data = get_campaigns(account_id)
        if campaign_data is None:
            return {'status': 'error', 'message': 'Falha ao obter dados das campanhas'}, 500
        ad_sets_data = get_ad_sets(account_id)
        if ad_sets_data is None:
            return {'status': 'error', 'message': 'Falha ao obter dados dos conjuntos de anúncios'}, 500

        ads_data = []
        for ad_set in ad_sets_data:
            if 'campaign_id' in ad_set:
                ad_set_ads = get_ads(ad_set['id'])
                if ad_set_ads is None:
                    return {'status': 'error', 'message': 'Falha ao obter dados dos anúncios'}, 500
                ads_data.extend(ad_set_ads)

        store_data(account_id, campaign_data, ad_sets_data, ads_data)
        return {'status': 'success', 'message': 'Campaigns, Ad Sets, and Ads data stored successfully'}, 200

    except FacebookRequestError as e:
        logger.error(f"Erro na requisição da API: {e}")
        error_code = e.api_error_code()
        error_message = e.api_error_message()
        error_subcode = e.api_error_subcode()
        logger.error(f"Código do erro: {error_code}, Mensagem: {error_message}, Subcódigo: {error_subcode}")
        time.sleep(60)
        return {'status': 'error', 'message': 'API request error occurred'}, 429

@app.route('/fetch_and_store_campaigns', methods=['GET'])
def fetch_and_store_campaigns_route():
    global current_ad_account
    result, status_code = fetch_and_store_data(current_ad_account)
    return jsonify(result), status_code

@app.route('/get_data')
def get_data():
    global current_ad_account
    collection_name = current_ad_account
    campaign_data = retrieve_data(collection_name)
    campaigns_funnel = []
    for campaign in campaign_data:
        campaign_funnel = {
            # ... seus dados de campanha ...
        }
        campaigns_funnel.append(campaign_funnel)
    return jsonify(campaigns_funnel)

def combined_task():
    with app.app_context():
        global current_ad_account
        try:
            ad_accounts = init_facebook_session_and_get_ad_accounts(app_id, app_secret, access_token)
            if current_ad_account not in [acc['id'] for acc in ad_accounts]:
                logger.warning(f"A conta atual {current_ad_account} não foi encontrada. Selecionando uma nova conta.")
                current_ad_account = ad_accounts[0]['id']
            else:
                current_ad_account_index = [acc['id'] for acc in ad_accounts].index(current_ad_account)
                current_ad_account = ad_accounts[(current_ad_account_index + 1) % len(ad_accounts)]['id']
            fetch_and_store_data(current_ad_account)
        except Exception as e:
            logger.error(f'Erro na tarefa combined_task: {e}')

# Configuração do APScheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=combined_task, trigger='interval', hours=1)
scheduler.start()

def shutdown_scheduler(exception=None):
    pass  

if __name__ == '__main__':
    import atexit
    atexit.register(lambda: scheduler.shutdown(wait=False))
    app.run(debug=True)
