from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.exceptions import FacebookRequestError
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.ad import Ad
import os

app_id = os.getenv('FACEBOOK_APP_ID')
app_secret = os.getenv('FACEBOOK_APP_SECRET')
access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')

def init_facebook_session_and_get_ad_accounts(app_id, app_secret, access_token):
    # Inicializa a sessão da API do Facebook
    FacebookAdsApi.init(app_id, app_secret, access_token)

    # Cria um objeto User para o usuário atual
    me = User(fbid='me')

    # Obtém as contas de anúncios associadas ao usuário
    ad_accounts = me.get_ad_accounts(fields=['id', 'name'])

    return list(ad_accounts)

def is_campaign_active(campaign):
    return campaign.get('status') == 'ACTIVE'

def get_campaigns(account_id):
    try:
        ad_account = AdAccount(account_id)
        fields = [
            Campaign.Field.account_id,
            Campaign.Field.adlabels,
            Campaign.Field.bid_strategy,
            Campaign.Field.boosted_object_id,
            Campaign.Field.brand_lift_studies,
            Campaign.Field.budget_rebalance_flag,
            Campaign.Field.budget_remaining,
            Campaign.Field.buying_type,
            Campaign.Field.campaign_group_active_time,
            Campaign.Field.can_create_brand_lift_study,
            Campaign.Field.can_use_spend_cap,
            Campaign.Field.configured_status,
            Campaign.Field.created_time,
            Campaign.Field.daily_budget,
            Campaign.Field.effective_status,
            Campaign.Field.has_secondary_skadnetwork_reporting,
            Campaign.Field.id,
            Campaign.Field.is_budget_schedule_enabled,
            Campaign.Field.is_skadnetwork_attribution,
            Campaign.Field.issues_info,
            Campaign.Field.last_budget_toggling_time,
            Campaign.Field.lifetime_budget,
            Campaign.Field.name,
            Campaign.Field.objective,
            Campaign.Field.pacing_type,
            Campaign.Field.primary_attribution,
            Campaign.Field.promoted_object,
            Campaign.Field.recommendations,
            Campaign.Field.smart_promotion_type,
            Campaign.Field.source_campaign,
            Campaign.Field.source_campaign_id,
            Campaign.Field.special_ad_categories,
            Campaign.Field.special_ad_category,
            Campaign.Field.special_ad_category_country,
            Campaign.Field.spend_cap,
            Campaign.Field.start_time,
            Campaign.Field.status,
            Campaign.Field.stop_time,
            Campaign.Field.topline_id,
            Campaign.Field.updated_time,
            Campaign.Field.adbatch,
            Campaign.Field.execution_options,
            Campaign.Field.iterative_split_test_configs
        ]
        campaigns = ad_account.get_campaigns(fields=fields)
        # Filtra apenas as campanhas ativas antes de retornar
        return [campaign.export_all_data() for campaign in campaigns if is_campaign_active(campaign.export_all_data())]
    except FacebookRequestError as e:
        print(f"Erro na requisição da API do Facebook: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
    

def get_ad_sets(account_id):
    try:
        ad_account = AdAccount(account_id)
        fields = [
            AdSet.Field.id,
            AdSet.Field.account_id,
            AdSet.Field.campaign_id,
            AdSet.Field.name,
            AdSet.Field.status,
            AdSet.Field.configured_status,
            AdSet.Field.effective_status,
            AdSet.Field.daily_budget,
            AdSet.Field.billing_event,
            AdSet.Field.optimization_goal,
            AdSet.Field.end_time,
            AdSet.Field.created_time,
            AdSet.Field.updated_time,
            AdSet.Field.bid_strategy,
            AdSet.Field.billing_event,
            AdSet.Field.destination_type,
            AdSet.Field.effective_status,
            AdSet.Field.optimization_goal,
            AdSet.Field.optimization_sub_event,
            AdSet.Field.pacing_type,
            AdSet.Field.promoted_object,
            AdSet.Field.targeting,
            ]
        adsets = ad_account.get_ad_sets(fields=fields)
        # Filtra apenas os conjuntos de anúncios ativos antes de retornar
        return [adset.export_all_data() for adset in adsets if adset[AdSet.Field.effective_status] == 'ACTIVE']
    except FacebookRequestError as e:
        print(f"Erro na requisição da API do Facebook: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None



def get_ads(ad_set_id):
    try:
        ad_set = AdSet(ad_set_id)
        fields = [
            Ad.Field.account_id,
            #Ad.Field.ad_active_time,
            #Ad.Field.ad_review_feedback,
            #Ad.Field.ad_schedule_end_time,
            #Ad.Field.ad_schedule_start_time,
            #Ad.Field.adlabels,
            #Ad.Field.adset,
            Ad.Field.adset_id,
            #Ad.Field.bid_amount,
            #Ad.Field.bid_info,
            #Ad.Field.bid_type,
            #Ad.Field.campaign,
            #Ad.Field.campaign_id,
            #Ad.Field.configured_status,
            #Ad.Field.conversion_domain,
            #Ad.Field.conversion_specs,
            #Ad.Field.created_time,
            #Ad.Field.creative,
            #Ad.Field.demolink_hash,
            #Ad.Field.display_sequence,
            Ad.Field.effective_status,
            #Ad.Field.engagement_audience,
            #Ad.Field.failed_delivery_checks,
            Ad.Field.id,
            #Ad.Field.issues_info,
            #Ad.Field.last_updated_by_app_id,
            #Ad.Field.name,
            #Ad.Field.preview_shareable_link,
            #Ad.Field.priority,
            #Ad.Field.recommendations,
            #Ad.Field.source_ad,
            #Ad.Field.source_ad_id,
            #Ad.Field.status,
            #Ad.Field.targeting,
            #Ad.Field.tracking_and_conversion_with_defaults,
            #Ad.Field.tracking_specs,
            #Ad.Field.updated_time,
            #Ad.Field.adset_spec,
            #Ad.Field.audience_id,
            #Ad.Field.date_format,
            #Ad.Field.draft_adgroup_id,
            #Ad.Field.execution_options,
            #Ad.Field.include_demolink_hashes,
            #Ad.Field.filename
        ]
        ads = ad_set.get_ads(fields=fields)
        # Filtra apenas os anúncios ativos antes de retornar
        return [ad.export_all_data() for ad in ads if ad[Ad.Field.effective_status] == 'ACTIVE']
    except FacebookRequestError as e:
        print(f"Erro na requisição da API do Facebook: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None


def detect_changes(new_data, old_data):
    changes = []
    for key in new_data:
        old_value = old_data.get(key)
        new_value = new_data[key]
        if old_value != new_value:
            change = {
                'field': key,
                'old_value': old_value,
                'new_value': new_value
            }
            changes.append(change)
    return changes



