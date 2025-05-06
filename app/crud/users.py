import asyncpg
from app.db.base import pool
from app.schemas.users import User

async def insertUser(user:User):
    async with pool.acquire() as conn:
        await conn.execute("INSERT INTO users (username, password) VALUES(%s, %s);", (
            user.username, 
            user.password
        ))

async def deleteUser(user:User):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM users WHERE username =%s AND password = %s;", (
            user.username, 
            user.password
        ))

async def checkExistUser(usesname):
    async with pool.acquire() as conn:
        result await conn.fetch("SELECT id FROM users WHERE username =%s;", (
            user.username,
            user.password
        ))
        return result != None

async def checkUser(user:User):
    async with pool.acquire() as conn:
        result = await conn.fetchrow("SELECT id FROM users WHERE username =%s AND password = %s;", (
            user.username, 
            user.password
        ))
        existUser= await checkExistUser(user.username)

        if userExist == false:
            return "User doesnt exist"
        elif result = None:
            return "Invalid username or password"
        else
            return "success"