from sol.sql_templates import SQL_TEMPLATES
from sol.views import execute_query, process_natural_language
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import ChatSession, ChatMessage
from .travel_tags import accommodation_tag, attraction_tag, restaurant_tag

@api_view(['POST'])
def chatbot_chat(request):
    """
    사용자 질문에 따라 생성형 AI 응답과 데이터베이스 검색 결과를 자연스럽게 통합.
    """
    session_id = request.data.get('session_id')
    message = request.data.get('message')
    if not session_id or not message:
        return JsonResponse({"error": "Both 'session_id' and 'message' are required."}, status=400)

    try:
        # 세션 확인 
        session = ChatSession.objects.get(session_id=session_id)
    except ChatSession.DoesNotExist:
        return JsonResponse({"error": "Session not found."}, status=404)

    # 이전 대화 기록 가져오기
    previous_messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
    conversation_history = ""
    for chat in previous_messages:
        conversation_history += f"사용자: {chat.user_message}\nAI: {chat.bot_response}\n"

    # 데이터베이스 검색 조건 확인
    sql_template = None
    num_items = 1  # 기본적으로 한 개만 추천 
    if any(tag in message for tag in attraction_tag):
        sql_template = "recommend_one_attraction" if "하나" in message or "한 군데" in message else "recommend_attractions"
    elif any(tag in message for tag in restaurant_tag):
        sql_template = "recommend_one_restaurant" if "하나" in message or "한 군데" in message else "recommend_restaurants"
    elif any(tag in message for tag in accommodation_tag):
        sql_template = "recommend_one_accommodation" if "하나" in message or "한 군데" in message else "recommend_accommodations"

    # 데이터베이스 검색 및 결과 생성
    db_response = ""
    if sql_template:
        try:
            params = [session.location]
            results = execute_query(sql_template, params)

            if results:
                db_response = "\n아래는 관련된 추천 항목입니다:\n"
                for idx, row in enumerate(results, 1):
                    if sql_template in ["recommend_one_attraction", "recommend_attractions"]:
                        db_response += (
                            f"{idx}.\n"
                            f"name: {row[1]}\n"
                            f"address: {row[2]} {row[3]} {row[4]} {row[5]} {row[6]} {row[7]}\n "
                            f"latitude: {row[9]}\n"
                            f"longitude: {row[8]}\n"
                        )
                    elif sql_template in ["recommend_one_restaurant", "recommend_restaurants"]:
                        db_response += (
                            f"{idx}.\n"
                            f"name: {row[4]}\n"
                            f"call: {row[1]}\n"
                            f"address: {row[3]}\n "
                            f"post: {row[2]}\n"
                            f"latitude: {row[5]}\n"
                            f"longitude: {row[6]}"
                        )
                    elif sql_template in ["recommend_one_accommodation", "recommend_accommodations"]:
                        db_response += (
                            f"{idx}.\n"
                            f"name: {row[1]}\n"
                            f"address: {row[2]}\n"
                            f"cat: {row[5]}\n"
                            f"latitude: {row[3]}\n"
                            f"longitude: {row[4]}\n"
                        )
            else:
                db_response = "\n관련된 여행정보 검색 결과를 찾을 수 없습니다."
        except Exception as e:
            db_response = f"\n여행정보 검색 중 오류가 발생했습니다: {str(e)}"
            print(f"[DEBUG] DB Error: {e}")  # 디버깅 로그

    # 생성형 AI 응답 생성
    try:
        if db_response.strip():
            # 데이터베이스 결과를 포함하여 AI 응답 생성
            prompt = (
                f"다음은 사용자의 대화 기록입니다:\n\n{conversation_history}\n"
                f"사용자: {message}\n"
                f"다음은 데이터베이스 검색 결과입니다:\n{db_response}\n"
                f"이 정보를 참고하여 사용자가 이해하기 쉽게 자연스러운 응답을 생성하세요."
            )
        else:
            # 데이터베이스 결과가 없을 때 기본 응답 생성
            prompt = f"다음은 사용자의 대화 기록입니다:\n\n{conversation_history}\n사용자: {message}\nAI:"
        ai_response = process_natural_language(prompt)
    except Exception as e:
        ai_response = "AI 응답 생성 중 오류가 발생했습니다."

    # 최종 응답 통합
    final_response = ai_response

    # 대화 기록 저장
    ChatMessage.objects.create(session=session, user_message=message, bot_response=final_response)

    return JsonResponse({
        "session_id": session_id,
        "response": final_response
    })
