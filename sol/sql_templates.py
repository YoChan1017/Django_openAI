SQL_TEMPLATES = {
    "recommend_attractions": """
        SELECT num, name, city, city2, city3, city4, bunnum, roadadd, x, y
        FROM attractions
        WHERE city LIKE %s
        ORDER BY RAND()
        LIMIT 5;
    """,
    "recommend_restaurants": """
        SELECT num, name, address, call, post, x, y
        FROM restaurants
        WHERE address LIKE %s
        ORDER BY RAND()
        LIMIT 5;
    """,
    "recommend_accommodations": """
        SELECT num, name, address, latitude, longitude, cat
        FROM accommodations
        WHERE address LIKE %s
        ORDER BY RAND()
        LIMIT 5;
    """,
}
