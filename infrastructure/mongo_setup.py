from typing import Optional

import motor.motor_asyncio
import beanie

from mongo_beanie import models


# async def init_connection(db_name: str):
#     conn_str = await create_connection_string(db_name)
#     client = motor.motor_asyncio.AsyncIOMotorClient(conn_str)
#
#     await beanie.init_beanie(database=client[db_name], document_models=models.all_models)
#
#     print(f'Connected to {db_name}')


async def _motor_init(database: str, server: str, port: int, username: Optional[str],
                      password: Optional[str], models: list, use_ssl: bool):
    conn_string = create_connection_string(server, port, username, password, use_ssl)

    # Create Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(conn_string)

    # Initialize Beanie with Package and User models
    await beanie.init_beanie(database=client[database], document_models=models)

    print(f'Init done for {database}')


async def init_db(database: str, server: Optional[str] = 'localhost', port: Optional[int] = 27017,
                  username: Optional[str] = None, password: Optional[str] = None, use_ssl: bool = False, ):
    server = server or 'localhost'
    port = port or 27017

    await _motor_init(database, server, port, username, password, models.all_models, use_ssl)


def create_connection_string(server, port, username, password, use_ssl):
    if username and password:
        use_ssl = str(use_ssl).lower()
        return f"mongodb://{username}:{password}@{server}:{port}/?authSource=admin&tls={use_ssl}&tlsInsecure=true"
    else:
        return f"mongodb://{server}:{port}"
