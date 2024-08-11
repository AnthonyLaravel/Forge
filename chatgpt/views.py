# chatgpt/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
