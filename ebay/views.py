from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from member.models import Member
from .models import EbayCategory, EbayCategoryAspect, ApiTest
import requests
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt

import os
import json
import base64
import hashlib
import logging
from OpenSSL import crypto
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import EbayApiLog

logger = logging.getLogger(__name__)


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


def get_best_category(title, access_token):
    url = "https://sandbox.api.ebay.com/commerce/taxonomy/v1/category_tree/0/get_category_suggestions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "title": title
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        category_suggestions = response.json()
        # Assuming we return the first suggestion for simplicity
        if 'categorySuggestions' in category_suggestions and len(category_suggestions['categorySuggestions']) > 0:
            return category_suggestions['categorySuggestions'][0]['category']
    return None


@login_required
def suggest_category(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        member = request.user.member
        category_suggestion = get_best_category(title, member.ebay_access_token)
        return render(request, 'ebay/suggest_category.html',
                      {'title': title, 'category_suggestion': category_suggestion})
    return render(request, 'ebay/suggest_category.html')


@login_required
def retrieve_category_aspects(request, category_id, category_tree_id):
    category = get_object_or_404(EbayCategory, category_id=category_id, category_tree_id=category_tree_id)
    access_token = request.user.member.ebay_access_token

    url = f"https://api.sandbox.ebay.com/commerce/taxonomy/v1/category_tree/{category_tree_id}/get_item_aspects_for_category?category_id={category_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        aspects_data = response.json().get('aspects', [])
        for aspect in aspects_data:
            EbayCategoryAspect.objects.update_or_create(
                category=category,
                aspect_name=aspect['aspectConstraint']['aspectName'],
                defaults={
                    'aspect_data_type': aspect.get('dataType', 'STRING'),
                    'aspect_mode': aspect.get('aspectMode', 'REQUIRED'),
                    'aspect_usage': aspect.get('aspectUsage', 'RECOMMENDED')
                }
            )
        return render(request, 'ebay/category_aspects.html', {'category': category, 'aspects': category.aspects.all()})
    else:
        messages.error(request, response.text)
        messages.error(request, f'URL:{url}')
        messages.error(request, f'headers:{headers}')
        messages.error(request, f'Token Expiration: {request.user.member.token_expiry}')
        return render(request, 'ebay/category_aspects.html', {'error': 'Failed to retrieve category aspects'})


@login_required
def api_test_view(request):
    member = get_object_or_404(Member, user=request.user)
    api_test = None

    if request.method == 'POST':
        endpoint = request.POST.get('endpoint', '')
        request_body = request.POST.get('request_body', '')

        headers = {
            'Authorization': f'Bearer {member.ebay_access_token}',
            'Content-Type': 'application/json',
        }

        response = requests.post(
            url=endpoint,
            headers=headers,
            data=request_body
        )

        # Store the request, endpoint, and response in the ApiTest model
        api_test = ApiTest.objects.create(
            member=member,
            endpoint=endpoint,
            request_body=request_body,
            response_body=response.text
        )

    # Retrieve all API tests for the current user
    api_tests = ApiTest.objects.filter(member=member).order_by('-created_at')

    return render(request, 'ebay/api_test.html', {'api_test': api_test, 'api_tests': api_tests})


class EbayApiLogListView(ListView):
    model = EbayApiLog
    template_name = 'ebay/ebay_api_log_list.html'
    context_object_name = 'logs'
    paginate_by = 10  # Number of logs to display per page
    ordering = ['-timestamp']  # Order logs by latest first


def log_request_response(request, response_status, response_body):
    EbayApiLog.objects.create(
        endpoint=request.path,
        request_method=request.method,
        request_headers=json.dumps(dict(request.headers)),
        request_body=request.body.decode('utf-8') if request.body else None,
        response_status=response_status,
        response_body=response_body
    )


class EbayMarketplaceAccountDeletion(APIView):
    CHALLENGE_CODE = 'challenge_code'
    VERIFICATION_TOKEN = settings.EBAY_VERIFICATION_TOKEN
    ENDPOINT = 'https://listingforge.com/dashboard/ebay/ebay_marketplace_account_deletion/'
    X_EBAY_SIGNATURE = 'X-Ebay-Signature'
    EBAY_BASE64_AUTHORIZATION_TOKEN = settings.EBAY_BASE64_AUTHORIZATION_TOKEN

    def get(self, request):
        """
        Get challenge code and return challengeResponse: challengeCode + verificationToken + endpoint
        :return: Response
        """
        challenge_code = request.GET.get(self.CHALLENGE_CODE)
        if not challenge_code:
            logger.error("Missing challenge code")
            return JsonResponse({"error": "Missing challenge code"}, status=status.HTTP_400_BAD_REQUEST)

        if not self.VERIFICATION_TOKEN:
            logger.error("Verification token not set")
            return JsonResponse({"error": "Verification token not set"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not self.ENDPOINT:
            logger.error("Endpoint not set")
            return JsonResponse({"error": "Endpoint not set"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        challenge_response = hashlib.sha256(
            challenge_code.encode('utf-8') +
            self.VERIFICATION_TOKEN.encode('utf-8') +
            self.ENDPOINT.encode('utf-8')
        )
        response_parameters = {
            "challengeResponse": challenge_response.hexdigest()
        }
        return JsonResponse(response_parameters, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            # Parse the JSON payload from eBay's request
            notification_data = request.body.decode('utf-8')

            # Save the notification data in the database

            # Respond with a success status to acknowledge receipt of the notification
            return JsonResponse({'message': 'Notification received and acknowledged'}, status=200)

        except Exception as e:
            # Log or handle any errors that occur
            return JsonResponse({'error': str(e)}, status=500)
