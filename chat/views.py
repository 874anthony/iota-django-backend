import os
from rest_framework.decorators import api_view
from openai import OpenAI
from django.http import JsonResponse
from .models import ChatMessage

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@api_view(["POST"])
def chat_with_gpt(request):
    """Handles user chat messages and returns responses from OpenAI's GPT model."""
    user_message = request.data.get("message", "")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        # store=True 
        messages=[{"role": "user", "content": user_message}]
        )
    
    gpt_response = response.choices[0].message.content

    ChatMessage.objects.create(
        user=request.user,
        message=user_message,
        response=gpt_response
    )

    return JsonResponse({
        "gpt_response": response.choices[0].message.content
    })

@api_view(["GET"])
def chat_history(request):
    """Returns the chat history for the current user."""
    chat_messages = ChatMessage.objects.filter(user=request.user).order_by("created_at")
    
    chat_history = [
        {
            "message": chat.message,
            "response": chat.response,
            "created_at": chat.created_at
        }
        for chat in chat_messages
    ]
    
    return JsonResponse({"chat_history": chat_history})