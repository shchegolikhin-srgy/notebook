import asyncpg
from database import pool

async def insertUser(username, password):
    async with pool.acquire() as conn:
        await conn.execute("INSERT INTO Users(username, password) VALUES('sergey', '1234');")

async def deleteUser(username, password):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM users WHERE username ='1' AND password = '1';")

async def checkUser(username, password):
    async with pool.acquire() as conn:
        await conn.execute(f"SELECT id FROM Users WHERE username ={username} AND password ={password};")
