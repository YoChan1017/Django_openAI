from django.shortcuts import render 
from sol.models import TABLES
import openai
from django.db import connection
import os
from .sql_templates import SQL_TEMPLATES

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_natural_language(query):
    """
    OpenAI를 사용하여 자연어를 SQL 쿼리로 변환합니다.
    """
    table_descriptions = "\n".join([
        f"테이블 {table}: {info['description']}, 컬럼: {', '.join(info['columns'])}"
        for table, info in TABLES.items()
    ])

    system_prompt = f"""
    당신은 MySQL 전문가입니다. 다음은 사용 가능한 데이터베이스 테이블 목록입니다:
    {table_descriptions}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )
    generated_query = response['choices'][0]['message']['content']
    return generated_query


def execute_query(template_name, params):
    """
    사전 정의된 SQL 템플릿을 실행합니다.
    """
    if template_name not in SQL_TEMPLATES:
        raise ValueError(f"Invalid SQL template name: {template_name}")

    sql = SQL_TEMPLATES[template_name]
    try:
        with connection.cursor() as cursor:
            # Python에서 파라미터 전처리
            params = [f"%{params[0]}%"]  # LIKE 조건에 맞게 전처리
            print(f"Executing SQL: {sql} with params: {params}")  # 디버그 출력
            cursor.execute(sql, params)
            rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"[DEBUG] SQL Execution Error: {str(e)}")  # 디버깅 로그
        raise ValueError(f"SQL Execution Error: {str(e)}")
