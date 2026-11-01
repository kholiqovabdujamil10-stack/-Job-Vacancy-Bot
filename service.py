from connection import *


async def create_vacancy(employer_id, company, position, salary, description, photo_file_id):
    try:
        conn = await connection_db()
        await conn.execute("""
            INSERT INTO vacancies
            (employer_id, company, position, salary, description, photo_file_id)
            VALUES ($1, $2, $3, $4, $5, $6)
        """, employer_id, company, position, salary, description, photo_file_id)

        vacancy = await conn.fetchrow("""
            SELECT id FROM vacancies
            WHERE employer_id = $1
            ORDER BY id DESC
            LIMIT 1
        """, employer_id)
        return vacancy["id"]

    except Exception as Error:
        print(f"Create vacancy Error: {Error}")

    finally:
        await conn.close()


async def get_vacancies():
    try:
        conn = await connection_db()
        vacancies = await conn.fetch("""
            SELECT * FROM vacancies
            WHERE status = 'open'
            ORDER BY created_at DESC
        """)
        return vacancies

    except Exception as Error:
        print(f"Get vacancies Error: {Error}")

    finally:
        await conn.close()


async def get_vacancy(vacancy_id):
    try:
        conn = await connection_db()
        vacancy = await conn.fetchrow("""
            SELECT * FROM vacancies
            WHERE id = $1
        """, vacancy_id)
        return vacancy

    except Exception as Error:
        print(f"Get vacancy Error: {Error}")

    finally:
        await conn.close()


async def create_application(user_id, vacancy_id):
    try:
        conn = await connection_db()

        vacancy = await conn.fetchrow("""
            SELECT employer_id, status FROM vacancies
            WHERE id = $1
        """, vacancy_id)

        if not vacancy:
            return "not_found"

        if vacancy["status"] == "closed":
            return "closed"

        if vacancy["employer_id"] == user_id:
            return "own"

        application = await conn.fetchrow("""
            SELECT id FROM applications
            WHERE user_id = $1 AND vacancy_id = $2
        """, user_id, vacancy_id)

        if application:
            return "exists"
        
        await conn.execute("""
            INSERT INTO applications (user_id, vacancy_id)
            VALUES ($1, $2)
        """, user_id, vacancy_id)
        return "success"

    except Exception as Error:
        print(f"Create application Error: {Error}")

    finally:
            await conn.close()


async def close_vacancy(vacancy_id, employer_id):
    try:
        conn = await connection_db()

        result = await conn.execute("""
            UPDATE vacancies
            SET status = 'closed'
            WHERE id = $1 AND employer_id = $2 AND status = 'open'
        """, vacancy_id, employer_id)

        return result == "UPDATE 1"

    except Exception as Error:
        print(f"Close vacancy Error: {Error}")

    finally:
        await conn.close()


async def get_applicants(vacancy_id, employer_id):
    try:
        conn = await connection_db()
        vacancy = await conn.fetchrow("""
            SELECT id FROM vacancies
            WHERE id = $1 AND employer_id = $2
        """, vacancy_id, employer_id)

        if not vacancy:
            return None
        applicants = await conn.fetch("""
            SELECT user_id, applied_at FROM applications
            WHERE vacancy_id = $1
            ORDER BY applied_at DESC
        """, vacancy_id)
        return applicants
    except Exception as Error:
        print(f"Get applicants Error: {Error}")

    finally:
        await conn.close()


async def get_my_applications(user_id):
    try:
        conn = await connection_db()
        applications = await conn.fetch("""
            SELECT
                applications.id,
                applications.applied_at,
                vacancies.position,
                vacancies.company,
                vacancies.status
            FROM applications
            JOIN vacancies ON applications.vacancy_id = vacancies.id
            WHERE applications.user_id = $1
            ORDER BY applications.applied_at DESC
        """, user_id)
        return applications

    except Exception as Error:
        print(f"Get my applications Error: {Error}")

    finally:
        await conn.close()


async def get_my_vacancies(employer_id):
    try:
        conn = await connection_db()
        vacancies = await conn.fetch("""
            SELECT * FROM vacancies
            WHERE employer_id = $1
        """, employer_id)
        return vacancies
    except Exception as Error:
        print(f"Get my vacancies Error: {Error}")
    finally:
        await conn.close()