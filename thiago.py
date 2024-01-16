from facebook_business.api import FacebookAdsApi
from facebook_business.exceptions import FacebookRequestError

# Configuração inicial da API do Facebook
app_id = '677752197796360'
app_secret = 'b4ddf1dd78d1fd88ee6d251f47dfd11e'
access_token = 'EAAJoaXrZB0ggBO2xgy27MiVazt0XHj4h3NCboAdoCpC8CnGdVZACXSwUxDo0IfPUEU02ZCphBU5I2JMF4qXBZByt6A8iZAD0mhVc9LWdrZAQZAPkos8ZBvr97LUZAP5SOFPExQZAO4SYwDItRYlVOmYiNqIL9TdZC0KgZAeOoYekNnQRTAaxXLH8AZA1hFN4KBxVJB0UR'
ad_account_id = 'act_330283615337074'
FacebookAdsApi.init(app_id, app_secret, access_token)

# Fazendo uma chamada para a API
try:
    # Substitua 'me' por uma chamada específica que você deseja fazer
    response = FacebookAdsApi.get_default_api().call(
        'GET', 
        ('me',)
    )

    # Acessando os cabeçalhos de resposta
    headers = response.headers()
    app_usage = headers.get('X-App-Usage', None)
    page_usage = headers.get('X-Page-Usage', None)
    business_usage = headers.get('X-Business-Use-Case-Usage', None)

    # Exibindo as informações de uso
    if app_usage:
        print("Uso do App:", app_usage)
    if page_usage:
        print("Uso da Página:", page_usage)
    if business_usage:
        print("Uso do Caso de Uso de Negócios:", business_usage)

except FacebookRequestError as e:
    # Lidando com erros na chamada da API
    print("Erro na requisição:", e)

    # Acessando e imprimindo informações de cabeçalhos de limite de taxa
    headers = e.headers()
    app_usage = headers.get('X-App-Usage', None)
    page_usage = headers.get('X-Page-Usage', None)
    business_usage = headers.get('X-Business-Use-Case-Usage', None)

    if app_usage:
        print("Uso do App:", app_usage)
    if page_usage:
        print("Uso da Página:", page_usage)
    if business_usage:
        print("Uso do Caso de Uso de Negócios:", business_usage)
