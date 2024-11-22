from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from sol.views import execute_query
from sol.views import process_natural_language

CACHE = {}

@api_view(['POST'])
def travel_recommendations(request):
    """
    특정 여행지의 관광지 추천 정보를 반환합니다.
    """
    location = request.data.get('location', '').strip()  # 입력값 정리
    if not location:
        return JsonResponse({"error": "Location parameter is required."}, status=400)

    try:
        # SQL 실행 (sol 앱의 execute_query 활용)
        results = execute_query("recommend_attractions", [location])

        # 캐시에 저장
        CACHE['recommendations'] = [
            {
                "id": i,
                "name": row[1],
                "address": f"{row[2] or ''} {row[3] or ''} {row[4] or ''} {row[5] or ''} {row[6] or ''} {row[7] or ''}".strip()
            }
            for i, row in enumerate(results, start=1)
        ]

        return JsonResponse({
            "location": location,
            "recommendations": CACHE['recommendations']
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
def travel_detail(request, id):
    """
    특정 추천 관광지의 상세 정보를 반환합니다.
    """
    if 'recommendations' not in CACHE:
        return JsonResponse({"error": "No recommendations found. Make a POST request to /sol/travel/ first."}, status=400)

    try:
        # ID에 해당하는 추천 정보를 검색
        recommendation = next((item for item in CACHE['recommendations'] if item['id'] == int(id)), None)
        if not recommendation:
            return JsonResponse({"error": "Recommendation not found."}, status=404)

        # location 값을 추출
        location = recommendation.get("address", "").split()[0]  # 주소에서 첫 단어를 location으로 추출

        # OpenAI를 사용해 짧은 설명 생성
        try:
            description = process_natural_language(
                f"대한민국 'location'에 있는 {recommendation['name']}라는 관광에 대한 설명을 두 줄로 작성해줘."
            )
            recommendation['description'] = description.strip()  # 짧은 설명 추가
        except Exception as ai_error:
            recommendation['description'] = "AI 설명 생성 실패"  # 실패 시 기본 메시지

        return JsonResponse({"recommendation": recommendation})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)