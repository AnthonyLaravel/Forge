from django.shortcuts import render

from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

import requests
from django.utils import timezone
from datetime import timedelta

# Create your views here.
@login_required
def ebay_authorize(request):
    # Redirect the user to eBay's authorization page
    # ebay_auth_url = f"https://auth.ebay.com/oauth2/authorize?client_id={settings.EBAY_CLIENT_ID}&redirect_uri={settings.EBAY_REDIRECT_URI}&response_type=code&scope={settings.EBAY_SCOPE}"
    ebay_auth_url = "https://auth.sandbox.ebay.com/oauth2/authorize?client_id=AnthonyG-SpeedLis-SBX-ba2849bbb-0589fd43&response_type=code&redirect_uri=Anthony_Grady-AnthonyG-SpeedL-azxzeifax&scope=https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/buy.order.readonly https://api.ebay.com/oauth/api_scope/buy.guest.order https://api.ebay.com/oauth/api_scope/sell.marketing.readonly https://api.ebay.com/oauth/api_scope/sell.marketing https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account.readonly https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly https://api.ebay.com/oauth/api_scope/sell.marketplace.insights.readonly https://api.ebay.com/oauth/api_scope/commerce.catalog.readonly https://api.ebay.com/oauth/api_scope/buy.shopping.cart https://api.ebay.com/oauth/api_scope/buy.offer.auction https://api.ebay.com/oauth/api_scope/commerce.identity.readonly https://api.ebay.com/oauth/api_scope/commerce.identity.email.readonly https://api.ebay.com/oauth/api_scope/commerce.identity.phone.readonly https://api.ebay.com/oauth/api_scope/commerce.identity.address.readonly https://api.ebay.com/oauth/api_scope/commerce.identity.name.readonly https://api.ebay.com/oauth/api_scope/commerce.identity.status.readonly https://api.ebay.com/oauth/api_scope/sell.finances https://api.ebay.com/oauth/api_scope/sell.payment.dispute https://api.ebay.com/oauth/api_scope/sell.item.draft https://api.ebay.com/oauth/api_scope/sell.item https://api.ebay.com/oauth/api_scope/sell.reputation https://api.ebay.com/oauth/api_scope/sell.reputation.readonly https://api.ebay.com/oauth/api_scope/commerce.notification.subscription https://api.ebay.com/oauth/api_scope/commerce.notification.subscription.readonly https://api.ebay.com/oauth/api_scope/sell.stores https://api.ebay.com/oauth/api_scope/sell.stores.readonly"
    return redirect(ebay_auth_url)


@login_required
def ebay_callback(request):
    code = request.GET.get('code')
    if code:
        member = request.user.member
        member.ebay_authorization_code = code
        member.save()
        # Exchange code for an access token here
    return redirect('dashboard')


@login_required
def exchange_code_for_token(request):
    member = request.user.member
    if member.ebay_authorization_code:
        url = "https://api.ebay.com/identity/v1/oauth2/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {settings.EBAY_CLIENT_CREDENTIALS}'
        }
        data = {
            'grant_type': 'authorization_code',
            'code': member.ebay_authorization_code,
            'redirect_uri': settings.EBAY_REDIRECT_URI
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            json_response = response.json()
            member.ebay_access_token = json_response['access_token']
            member.token_expiry = timezone.now() + timedelta(seconds=json_response['expires_in'])
            member.save()
            # Redirect to the dashboard or another page
    return redirect('dashboard')