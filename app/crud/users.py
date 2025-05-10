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

async def check_exist_user(username):
    async with get_db_connection() as connection:
        result =await connection.fetchval("SELECT id FROM users WHERE username =$1;", 
            username
        )
        return result !=None

async def check_user(user:User):
    async with get_db_connection() as connection:
        hash = ph.hash(user.password)
        result = await connection.fetchval("SELECT id FROM users WHERE username =$1 AND hashed_password = $2;", 
            user.username, 
            hash
        )
        existUser= await check_exist_user(user.username)
        if result == None:
            return "Invalid username or password"
        else:
            return "success"

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