import os
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # ✅ Groq client

def chatbot_page(request):
    return render(request, 'index.html')

def get_response(request):
    user_message = request.GET.get('message', '')

    try:
        # Send message to Groq
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False
        )

        answer = completion.choices[0].message.content.strip()

        # Emoji selection based on sentiment
        emotion = "🤖"
        lowered = answer.lower()
        if any(word in lowered for word in ['happy', 'glad', 'joy', 'great']):
            emotion = "😊"
        elif any(word in lowered for word in ['sad', 'sorry', 'unhappy']):
            emotion = "😢"
        elif any(word in lowered for word in ['angry', 'mad', 'furious']):
            emotion = "😠"
        elif any(word in lowered for word in ['love', 'like', 'heart']):
            emotion = "❤️"
        elif any(word in lowered for word in ['confused', 'lost', "don't know"]):
            emotion = "😕"

        return JsonResponse({"response": answer, "emoji": emotion})

    except Exception as e:
        return JsonResponse({"response": f"Error: {str(e)}", "emoji": "⚠️"})