from django.http import JsonResponse
import json
import os
import random
import pymysql
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
from sol.views import process_natural_language
import re

# Load environment variables (API key, etc.)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("환경 변수 OPENAI_API_KEY가 설정되지 않았습니다.")

db_config = {
    'user': 'root',
    'password': '0000',
    'host': 'localhost',
    'database': 'sollaim',
    'port': 3306
}

# Cache to store generated itineraries
itinerary_cache = {}

# Function to get places from MySQL database
def get_places_from_db(location):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        # Get accommodations from the database
        cursor.execute("""
            SELECT Name, Address FROM accommodations WHERE Address LIKE %s
        """, (f"%{location}%",))
        accommodations = list(cursor.fetchall())

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

# Plan page view (JSON output)
@csrf_exempt
def plan(request, place_id=None):
    # Handle specific ID retrieval
    if place_id is not None:
        # Check if the requested ID exists in the cached itineraries
        for cache_key, itinerary in itinerary_cache.items():
            for day in itinerary['itinerary']:
                for place in day['schedule']:
                    if place['id'] == place_id:
                        return JsonResponse(place)  # Return the specific place as JSON
        return JsonResponse({'error': f'ID {place_id}에 해당하는 항목을 찾을 수 없습니다.'}, status=404)

    # Handle itinerary generation or retrieval
    if request.method in ['GET', 'POST']:
        try:
            # Parse JSON data for both GET and POST requests
            body_data = json.loads(request.body.decode('utf-8'))
            location = body_data.get('location')
            days = body_data.get('days')

            if location and days and str(days).isdigit():
                days = int(days)  # Convert days to an integer
                cache_key = f"{location}_{days}"

                # Check if itinerary already exists in cache
                if cache_key in itinerary_cache:
                    return JsonResponse(itinerary_cache[cache_key])

                # Get places from the database
                places = get_places_from_db(location)
                if not places or not places['accommodations']:
                    response = {'error': 'DB에 충분한 장소 정보가 없습니다.'}
                    return JsonResponse(response, status=500)

                accommodations = places['accommodations']

                itinerary = []
                place_id_counter = 1

                for day in range(1, days + 1):
                    # Randomly select an accommodation for the day
                    accommodation = random.choice(accommodations)
                    accommodation_name, accommodation_address = accommodation

                    # Extract city and district from the accommodation's address
                    city_name, district_name = extract_city_and_district(accommodation_address)
                    if not city_name or not district_name:
                        response = {'error': '숙소 주소에서 구/군/시 정보를 추출할 수 없습니다.'}
                        return JsonResponse(response, status=500)

                    try:
                        conn = pymysql.connect(**db_config)
                        cursor = conn.cursor()

                        # Get attractions from the database matching city and district
                        cursor.execute("""
                            SELECT Name, City, City2, City3, City4 
                            FROM attractions 
                            WHERE City = %s AND City2 = %s
                        """, (city_name, district_name))
                        attractions = [
                            {
                                "name": row[0],
                                "address": " ".join(filter(None, row[1:])),
                                "table": "attractions"  # Include table name
                            }
                            for row in cursor.fetchall()
                        ]

                        # Get restaurants from the database matching city and district
                        cursor.execute("""
                            SELECT Name, Address 
                            FROM restaurants 
                            WHERE Address LIKE %s AND Address LIKE %s
                        """, (f"%{city_name}%", f"%{district_name}%"))
                        restaurants = [
                            {
                                "name": row[0],
                                "address": row[1],
                                "table": "restaurants"  # Include table name
                            }
                            for row in cursor.fetchall()
                        ]

                        conn.close()
                    except Exception as e:
                        print(f"MySQL DB 오류: {str(e)}")
                        return JsonResponse({'error': 'DB 조회 실패'}, status=500)

                    # Create the day's schedule
                    day_schedule = [
                        {
                            "id": place_id_counter,
                            "name": accommodation_name,
                            "address": accommodation_address,
                            "table": "accommodations"  # Include table name
                        }
                    ]
                    place_id_counter += 1

                    # Select up to 3 attractions within the district
                    selected_attractions = random.sample(attractions, min(3, len(attractions)))
                    for attraction in selected_attractions:
                        day_schedule.append({
                            "id": place_id_counter,
                            "name": attraction["name"],
                            "address": attraction["address"],
                            "table": attraction["table"]
                        })
                        place_id_counter += 1

                    # Select up to 2 restaurants within the district
                    selected_restaurants = random.sample(restaurants, min(2, len(restaurants)))
                    for restaurant in selected_restaurants:
                        day_schedule.append({
                            "id": place_id_counter,
                            "name": restaurant["name"],
                            "address": restaurant["address"],
                            "table": restaurant["table"]
                        })
                        place_id_counter += 1

                    # Generate descriptions for each place using GPT
                    for place in day_schedule:
                        if place["table"] == "accommodations":
                            prompt = f"{place['name']}은(는) 어떤 숙박 시설인가요? 간략하고 짧은 한 줄 설명을 제공해주세요."
                        elif place["table"] == "attractions":
                            prompt = f"{place['name']}은(는) 어떤 명소인가요? 간략하고 짧은 한 줄 설명을 제공해주세요."
                        elif place["table"] == "restaurants":
                            prompt = f"{place['name']}은(는) 어떤 식당인가요? 간략하고 짧은 한 줄 설명을 제공해주세요."

                        try:
                            # process_natural_language가 문자열을 반환한다고 가정
                            place['description'] = process_natural_language(prompt).strip()
                        except Exception as e:
                            # 오류 발생 시 기본 설명 제공
                            place['description'] = "설명을 생성하는 중 오류가 발생했습니다."

                    itinerary.append({
                        "day": day,
                        "schedule": day_schedule
                    })

                response = {
                    "location": location,
                    "days": days,
                    "itinerary": itinerary
                }

                # Cache the generated itinerary
                itinerary_cache[cache_key] = response

                return JsonResponse(response)
            else:
                return JsonResponse({'error': '유효하지 않은 location 또는 days 값입니다.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON 형식이 잘못되었습니다.'}, status=400)
    else:
        return JsonResponse({'error': 'GET 또는 POST 요청만 지원됩니다.'}, status=405)
