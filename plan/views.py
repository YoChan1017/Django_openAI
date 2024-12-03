import uuid
from django.http import JsonResponse
import json
import os
import random
import pymysql
from dotenv import load_dotenv
from sol.views import process_natural_language
from django.views.decorators.csrf import csrf_exempt
import re

# Load environment variables (API key, etc.)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("환경 변수 OPENAI_API_KEY가 설정되지 않았습니다.")

# 데이터베이스 설정 가져오기
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306)),  # 기본값: 3306
}

# Cache to store the last generated itinerary
current_itinerary = None

# Function to get places from MySQL database
def get_places_from_db(location):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Get accommodations with latitude and longitude
        cursor.execute("""
            SELECT Name, Address, Latitude, Longitude 
            FROM accommodations 
            WHERE Address LIKE %s
        """, (f"%{location}%",))
        accommodations = [
            {
                "name": row[0],
                "address": row[1],
                "latitude": row[2],
                "longitude": row[3],
                "table": "accommodations"
            }
            for row in cursor.fetchall()
        ]

        conn.close()
        return {
            'accommodations': accommodations
        }
    except Exception as e:
        print(f"MySQL DB 오류: {str(e)}")
        return None

# Function to extract city and district from address
def extract_city_and_district(address):
    match = re.search(r'(\S+시|\S+도)\s+(\S+구|\S+군|\S+시)', address)
    if match:
        return match.group(1), match.group(2)
    return None, None

# Function to generate GPT description
def generate_gpt_description(place):
    if place["table"] == "accommodations":
        prompt = f"{place['name']}은(는) 어떤 숙박 시설인가요? 간략하고 짧은 한 줄 설명을 제공해주세요."
    elif place["table"] == "attractions":
        prompt = f"{place['name']}은(는) 어떤 명소인가요? 간략하고 짧은 한 줄 설명을 제공해주세요."
    elif place["table"] == "restaurants":
        prompt = f"{place['name']}은(는) 어떤 식당인가요? 간략하고 짧은 한 줄 설명을 제공해주세요."
    else:
        prompt = f"{place['name']}에 대해 간략하고 짧은 한 줄 설명을 제공해주세요."
    return process_natural_language(prompt).strip()

# Plan page view (JSON output)
@csrf_exempt
def plan(request, place_id=None):
    global current_itinerary  # Ensure we use the global current itinerary variable

    # Handle specific ID retrieval
    if place_id is not None:
        try:
            place_id = int(place_id)  # Ensure the ID is an integer
            if current_itinerary:  # Check if there is an existing itinerary
                for day in current_itinerary['itinerary']:
                    for place in day['schedule']:
                        if place['id'] == place_id:
                            # Skip description generation for "없음"
                            if place["name"] == "없음" or place["address"] in [
                                "해당 지역에 관광지가 없습니다.",
                                "해당 지역에 식당이 없습니다."
                            ]:
                                place['description'] = None  # Do not generate a description
                            else:
                                # Generate GPT description for valid places
                                place['description'] = generate_gpt_description(place)
                            return JsonResponse(place)
            return JsonResponse({'error': f'ID {place_id}에 해당하는 항목을 찾을 수 없습니다.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'상세 정보 처리 중 에러 발생: {str(e)}'}, status=500)

    # Generate a new itinerary on every request
    if request.method in ['GET', 'POST']:
        try:
            body_data = json.loads(request.body.decode('utf-8'))
            location = body_data.get('location')
            days = body_data.get('days')

            if location and days and str(days).isdigit():
                days = int(days)

                # Fetch places from the database
                places = get_places_from_db(location)
                if not places or not places['accommodations']:
                    return JsonResponse({'error': 'DB에 충분한 장소 정보가 없습니다.'}, status=500)

                accommodations = places['accommodations']

                itinerary = []
                place_id_counter = 1  # Start the ID counter

                for day in range(1, days + 1):
                    accommodation = random.choice(accommodations)
                    accommodation_name, accommodation_address, latitude, longitude = (
                        accommodation["name"],
                        accommodation["address"],
                        accommodation["latitude"],
                        accommodation["longitude"],
                    )
                    city_name, district_name = extract_city_and_district(accommodation_address)
                    if not city_name or not district_name:
                        return JsonResponse({'error': '숙소 주소에서 구/군/시 정보를 추출할 수 없습니다.'}, status=500)

                    day_schedule = [
                        {
                            "id": place_id_counter,
                            "name": accommodation_name,
                            "address": accommodation_address,
                            "latitude": latitude,
                            "longitude": longitude,
                            "table": "accommodations"
                        }
                    ]
                    place_id_counter += 1

                    try:
                        conn = pymysql.connect(**db_config)
                        cursor = conn.cursor()

                        # Get attractions with x and y coordinates
                        cursor.execute("""
                            SELECT Name, City, City2, City3, City4, x, y 
                            FROM attractions 
                            WHERE City = %s AND City2 = %s
                        """, (city_name, district_name))
                        attractions = [
                            {
                                "name": row[0],
                                "address": " ".join(filter(None, row[1:5])),
                                "x": row[5],
                                "y": row[6],
                                "table": "attractions"
                            }
                            for row in cursor.fetchall()
                        ]

                        # Get restaurants with x and y coordinates
                        cursor.execute("""
                            SELECT Name, Address, x, y 
                            FROM restaurants 
                            WHERE Address LIKE %s AND Address LIKE %s
                        """, (f"%{city_name}%", f"%{district_name}%"))
                        restaurants = [
                            {
                                "name": row[0],
                                "address": row[1],
                                "x": row[2],
                                "y": row[3],
                                "table": "restaurants"
                            }
                            for row in cursor.fetchall()
                        ]

                        conn.close()
                    except Exception as e:
                        print(f"MySQL DB 오류: {str(e)}")
                        return JsonResponse({'error': 'DB 조회 실패'}, status=500)

                    # If no attractions are found, add "없음" placeholders
                    while len(attractions) < 3:
                        attractions.append({
                            "name": "없음",
                            "address": "해당 지역에 관광지가 없습니다.",
                            "x": None,
                            "y": None,
                            "table": "attractions"
                        })

                    # If no restaurants are found, add "없음" placeholders
                    while len(restaurants) < 2:
                        restaurants.append({
                            "name": "없음",
                            "address": "해당 지역에 식당이 없습니다.",
                            "x": None,
                            "y": None,
                            "table": "restaurants"
                        })

                    # Add selected attractions and restaurants to the schedule
                    selected_attractions = random.sample(attractions, 3)  # Ensure 3 attractions
                    for attraction in selected_attractions:
                        attraction["id"] = place_id_counter  # Assign an ID
                        day_schedule.append(attraction)
                        place_id_counter += 1

                    selected_restaurants = random.sample(restaurants, 2)  # Ensure 2 restaurants
                    for restaurant in selected_restaurants:
                        restaurant["id"] = place_id_counter  # Assign an ID
                        day_schedule.append(restaurant)
                        place_id_counter += 1

                    itinerary.append({
                        "day": day,
                        "schedule": day_schedule
                    })

                response = {
                    "location": location,
                    "days": days,
                    "itinerary": itinerary
                }

                # Overwrite the global current itinerary
                current_itinerary = response
                return JsonResponse(response)
            else:
                return JsonResponse({'error': '유효하지 않은 location 또는 days 값입니다.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON 형식이 잘못되었습니다.'}, status=400)
    else:
        return JsonResponse({'error': 'GET 또는 POST 요청만 지원됩니다.'}, status=405)
