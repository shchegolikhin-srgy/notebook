import asyncpg
from app.db.base import get_db_connection
from app.schemas.users import User
from argon2 import PasswordHasher

ph = PasswordHasher()

async def delete_user(user:User):
    async with get_db_connection() as connection:
        hash = ph.hash(user.password)
        await connection.execute("DELETE FROM users WHERE username =$1 AND hashed_password= $2;", 
            user.username, 
            hash
        )

async def check_user(user:User):
    async with get_db_connection() as connection:
        row = await connection.fetchrow("SELECT id, hashed_password FROM users WHERE username =$1;", 
            user.username
        )
        if row == []:
            return "user doesnt exist"
        try:
            ph.verify(row[1], user.password)
            return "success"
        except:
            return "invalide password"

async def add_user(user:User):
    async with get_db_connection() as connection:
        hash = ph.hash(user.password)
        if await check_exist_user(user.username) ==False:
            await connection.execute("INSERT INTO users (username, hashed_password) VALUES($1, $2);", 
                user.username, 
                hash
            )
            return "user created"
        else:
            return "user not created"