import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

passw = os.getenv("PASSWORD_DB")

async def connection_db():
    return await asyncpg.connect(
        host="localhost",
        port=5432,
        user="postgres",
        database="lesson 1",
        password=passw
    )


async def create_table():
    try:
        conn = await connection_db()
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                employer_id BIGINT NOT NULL,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                salary NUMERIC(12, 2) NOT NULL CHECK (salary > 0),
                description TEXT NOT NULL,
                photo_file_id TEXT NOT NULL,
                status TEXT DEFAULT 'open' CHECK (status IN ('open', 'closed')),
                created_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS applications (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                vacancy_id INTEGER NOT NULL REFERENCES vacancies(id) ON DELETE CASCADE,
                applied_at TIMESTAMP DEFAULT NOW(),
            );
        """)

        print("Database tables created successfully")

    except Exception as error:
        print(f"Database creation error: {error}")

    finally:
        await conn.close()