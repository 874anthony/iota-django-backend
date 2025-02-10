import os
from rest_framework.decorators import api_view
from openai import OpenAI
from django.http import JsonResponse

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

    return JsonResponse({
        "gpt_response": response.choices[0].message.content
    })
