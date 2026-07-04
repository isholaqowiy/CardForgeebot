import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                title TEXT,
                company TEXT,
                phone TEXT,
                email TEXT,
                website TEXT,
                tagline TEXT,
                template TEXT DEFAULT 'Modern'
            )
        ''')
        await db.commit()

async def register_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def save_card(user_id: int, data: dict):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT OR REPLACE INTO cards (user_id, name, title, company, phone, email, website, tagline, template)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, data.get('name'), data.get('title'), data.get('company'), 
              data.get('phone'), data.get('email'), data.get('website'), data.get('tagline'), data.get('template', 'Modern')))
        await db.commit()

async def get_card(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT name, title, company, phone, email, website, tagline, template FROM cards WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "name": row[0], "title": row[1], "company": row[2],
                    "phone": row[3], "email": row[4], "website": row[5],
                    "tagline": row[6], "template": row[7]
                }
            return None

async def get_total_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def get_total_cards():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM cards") as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

