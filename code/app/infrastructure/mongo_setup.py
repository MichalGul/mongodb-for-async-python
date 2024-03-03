import beanie
import motor.motor_asyncio
import models

async def init_connection(address:str, port: str, db_name: str, user: str = "user", password: str = "password", auth_source: str = "admin"):
    conn_str = f"mongodb://{user}:{password}@{address}:{port}/{db_name}?authSource={auth_source}"
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_str)

    await beanie.init_beanie(database=client[db_name], document_models=models.all_models)

    print(f"Connected to {db_name}.")
