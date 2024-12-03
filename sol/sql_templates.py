SQL_TEMPLATES = {
    # 기존 템플릿들 
    "recommend_attractions": """
        -- 특정 도시에서 관광지 5개를 랜덤 추천
        SELECT num, name, city, city2, city3, city4, bunnum, roadadd, x, y
        FROM attractions
        WHERE city LIKE %s
        ORDER BY RAND()
        LIMIT 5;
    """,
    "recommend_restaurants": """
        -- 특정 지역에서 레스토랑 5개를 랜덤 추천
        SELECT num, 'call', post, name, address, x, y
        FROM restaurants
        WHERE address LIKE %s
        ORDER BY RAND()
        LIMIT 5;
    """,
    "recommend_accommodations": """
        -- 특정 지역에서 숙소 5개를 랜덤 추천
        SELECT num, name, address, latitude, longitude, cat
        FROM accommodations
        WHERE address LIKE %s
        ORDER BY RAND()
        LIMIT 5;
    """,
    
    # 랜덤으로 하나씩 추천
    "recommend_one_attraction": """
        -- 관광지에서 하나를 랜덤 추천
        SELECT num, name, city, city2, city3, city4, bunnum, roadadd, x, y
        FROM attractions
        WHERE city LIKE %s
        ORDER BY RAND()
        LIMIT 1;
    """,
    "recommend_one_restaurant": """
        -- 레스토랑에서 하나를 랜덤 추천
        SELECT num, 'call', post, name, address, x, y
        FROM restaurants
        WHERE address LIKE %s
        ORDER BY RAND()
        LIMIT 1;
    """,
    "recommend_one_accommodation": """
        -- 숙소에서 하나를 랜덤 추천
        SELECT num, name, address, latitude, longitude, cat
        FROM accommodations
        WHERE address LIKE %s
        ORDER BY RAND()
        LIMIT 1;
    """
}
