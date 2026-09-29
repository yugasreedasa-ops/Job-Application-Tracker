import sqlite3

DB_NAME = "applications.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            job_role TEXT NOT NULL,
            application_date TEXT NOT NULL,
            status TEXT NOT NULL,
            job_link TEXT,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_application(
    company,
    job_role,
    application_date,
    status,
    job_link,
    notes
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications
        (company, job_role, application_date, status, job_link, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        company,
        job_role,
        application_date,
        status,
        job_link,
        notes
    ))

    conn.commit()
    conn.close()


def get_applications():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM applications
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def update_application(
    application_id,
    company,
    job_role,
    application_date,
    status,
    job_link,
    notes
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET company = ?,
            job_role = ?,
            application_date = ?,
            status = ?,
            job_link = ?,
            notes = ?
        WHERE id = ?
    """, (
        company,
        job_role,
        application_date,
        status,
        job_link,
        notes,
        application_id
    ))

    conn.commit()
    conn.close()


def delete_application(application_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (application_id,)
    )

    conn.commit()
    conn.close()