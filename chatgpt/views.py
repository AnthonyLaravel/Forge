# chatgpt/views.py
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from .models import ChatRequest
from openai import OpenAI
import openai


@login_required
def chatgpt_interact(request):
    if request.method == 'POST':
        # Configure your OpenAI API key
        openai.api_key = settings.OPENAI_API_KEY

        prompt = request.POST.get('prompt')

        # Interact with ChatGPT API
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
            max_tokens=300,
        )

        # Store the prompt and response in the database
        chat_request = ChatRequest.objects.create(
            user=request.user,
            prompt=prompt,
            response=response.choices[0].message.content
        )
        chat_request.save()

        return redirect('chatgpt_history')

    return render(request, 'chatgpt/chatgpt_form.html')


@login_required
def chatgpt_history(request):
    chat_requests = ChatRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chatgpt/chatgpt_history.html', {'chat_requests': chat_requests})

@login_required
def chat_request_history(request):
    chat_requests = ChatRequest.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'chat_requests': chat_requests
    }
    return render(request, 'chatgpt/chatgpt_request_history.html', context)


@login_required
def analyze_images(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    images = listing.images.all()

    if request.method == 'POST':
        analyzed_details = []
        # Configure your OpenAI API key
        openai.api_key = settings.OPENAI_API_KEY
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        for image in images:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {"type": "image_url", "image_url": {"url": image.image.url}},
                    ],
                }
            ]
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What’s in this image?"},
                            {"type": "image_url", "image_url": {"url": image.image.url}},
                        ],
                    }
                ],
                max_tokens=300,
            )
            # Extract details from the response
            extracted_details = response.choices[0].message.content
            image.alt_text = extracted_details
            image.save()
            # Store the prompt and response in the database
            chat_request = ChatRequest.objects.create(
                user=request.user,
                prompt=messages,
                response=response.choices[0].message.content
            )
            chat_request.save()
            analyzed_details.append(extracted_details)

        # Update listing description with analyzed details
        listing.description = "\n".join(analyzed_details)
        listing.save()
        return redirect('dashboard')

    return render(request, 'chatgpt/chatgpt_analyze_images.html', {'listing': listing, 'images': images})


