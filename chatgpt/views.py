# chatgpt/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRequest
from openai import OpenAI


@login_required
def chatgpt_interact(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')

        # Interact with ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        # Store the prompt and response in the database
        chat_request = ChatRequest.objects.create(
            user=request.user,
            prompt=prompt,
            response=response['choices'][0]['message']['content']
        )
        chat_request.save()

        return redirect('chatgpt_history')

    return render(request, 'chatgpt/chatgpt_form.html')


@login_required
def chatgpt_history(request):
    chat_requests = ChatRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chatgpt/chatgpt_history.html', {'chat_requests': chat_requests})
