from django.shortcuts import render 
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import ChatSession, ChatMessage
import uuid

@api_view(['POST'])
def create_chatbot(request):
    location = request.data.get('location')
    days = request.data.get('days')
    if not location or not days:
        return JsonResponse({"error": "Both 'location' and 'days' are required."}, status=400)

    # 세션 생성
    session_id = str(uuid.uuid4())
    session = ChatSession.objects.create(session_id=session_id, location=location, days=days)

    # 초기 메시지 생성
    initial_message = f"안녕하세요! '{location}'에서 {days}일 동안의 여행을 도와드릴게요. 궁금한 점이 있으면 말씀해주세요!"
    ChatMessage.objects.create(session=session, user_message="", bot_response=initial_message)

    return JsonResponse({
        "session_id": session.session_id,
        "response": initial_message
    })

@api_view(['POST'])
def chatbot_log(request):
    session_id = request.data.get('session_id')  # POST 요청의 JSON 본문에서 session_id 추출
    if not session_id:
        return JsonResponse({"error": "'session_id' is required."}, status=400)

    try:
        session = ChatSession.objects.get(session_id=session_id)
    except ChatSession.DoesNotExist:
        return JsonResponse({"error": "Session not found."}, status=404)

    messages = session.messages.all().order_by('timestamp')
    chat_history = [
        {
            "user_message": msg.user_message,
            "bot_response": msg.bot_response,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in messages
    ]

    return JsonResponse({"chat_history": chat_history})
