from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from sqlalchemy import create_engine
from database import get_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///turini.db"

engine = create_engine(DATABASE_URL)

@app.get("/")
def home():
    return {"message": "Turini Server Running!"}


@app.get("/test-db")
def test_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables = cursor.fetchall()

    conn.close()

    return {
        "tables": [table[0] for table in tables]
    }
from database import get_connection

@app.get("/learning-quiz")
def get_learning_quiz():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Learning_Quiz
        LIMIT 720
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "quiz_id": row[1],
            "category": row[2],
            "difficulty": row[3],
            "question_type": row[4],
            "question_text": row[5],
            "choice_1": row[6],
            "choice_2": row[7],
            "choice_3": row[8],
            "choice_4": row[9],
            "answer": row[10]
        })

    conn.close()

    return result
from database import get_connection

@app.get("/learning-quiz")
def get_learning_quiz(category: str = None, difficulty: str = None):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT *
        FROM Learning_Quiz
        WHERE 1=1
    """
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if difficulty:
        query += " AND difficulty = ?"
        params.append(difficulty)

    query += " ORDER BY RANDOM()"
    query += " LIMIT 15"

    cursor.execute(query, params)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "learning_quiz_id": row[0],
            "quiz_id": row[1],
            "category": row[2],
            "difficulty": row[3],
            "question_type": row[4],
            "question_text": row[5],
            "choice_1": row[6],
            "choice_2": row[7],
            "choice_3": row[8],
            "choice_4": row[9],
            "answer": row[10],
            "answer_explanation": row[11],
            "weakness_tag": row[12],
            "learning_goal": row[13]
        })

    conn.close()

    return result