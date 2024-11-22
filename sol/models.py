# models.py
# 데이터베이스 테이블과 컬럼 정보
TABLES = {
    "restaurants": {
        "columns": ["num", "call", "post", "address", "name", "x", "y"],
        "description": "식당 정보를 저장하는 테이블"
    },
    "accommodations": {
        "columns": ["num", "name", "address", "latitude", "longitude", "cat"],
        "description": "숙박 정보를 저장하는 테이블"
    },
    "attractions": {
        "columns": ["num", "name", "city", "city2", "city3", "city4", "bunnum", "roadadd", "x", "y"],
        "description": "관광지 정보를 저장하는 테이블"
    }
}
