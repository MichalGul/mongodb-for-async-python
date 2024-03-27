from typing import Optional

import beanie
import motor.motor_asyncio
import models


# async def init_connection(address:str, port: str, db_name: str, user: str = "user", password: str = "password", auth_source: str = "admin", use_ssl: bool = False, silent: bool = False):
#     conn_str = f"mongodb://{user}:{password}@{address}:{port}/{db_name}?authSource={auth_source}"
#     client = motor.motor_asyncio.AsyncIOMotorClient(conn_str)
#
#     await beanie.init_beanie(database=client[db_name], document_models=models.all_models)
#
#     print(f"Connected to {db_name}.")


async def init_connection(database: str, server: Optional[str] = 'localhost',
                  port: int = 27017, username: Optional[str] = None, password: Optional[str] = None,
                  use_ssl: bool = False, auth_source:str = "admin"):
    server = server or 'localhost'
    port = port or 27017

    await _motor_init(database=database, password=password, port=port, server=server,
                      use_ssl=use_ssl, username=username, models_classes=models.all_models)


async def _motor_init(database: str, password: Optional[str], port: int, server: str,
                      use_ssl: bool, username: Optional[str], models_classes):

    conn_string = create_connection_string(password, port, server, use_ssl, username)

    print(f'Initializing motor connection for db {database} on {server}:{port}')
    print(f'Connection string: {conn_string.replace(password or "NO_PASSWORD", "***********")}')

    # Crete Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_string)

    # Init beanie with the Product document class
    await beanie.init_beanie(database=client[database], document_models=models_classes)
    print(f"Init done for db {database}")


def create_connection_string(password, port, server, use_ssl, username):
    if username or password:
        use_ssl = str(use_ssl).lower()
        return f"mongodb://{username}:{password}@{server}:{port}/?authSource=admin&tls={use_ssl}&tlsInsecure=true"
    else:
        return f"mongodb://{server}:{port}"
