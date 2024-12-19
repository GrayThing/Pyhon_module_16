from fastapi import FastAPI, Path
from typing import Annotated


app = FastAPI()
users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/users')
async def get_all_users():
    return users


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=3,
                                                  max_length=15,
                                                  description='Имя пользователя',
                                                  example='mistic')],
                   age: Annotated[int, Path(ge=14,
                                            le=99,
                                            description='Ваш возраст',
                                            example='35')]):
    user_id = str(max([int(key) for key in users.keys()]) + 1)
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f'User {user_id} is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1,
                                                   le=1000,
                                                   description='ID пользователя',
                                                   example='35')],
                      username: Annotated[str, Path(min_length=3,
                                                    max_length=15,
                                                    description='Имя пользователя',
                                                    example='mistic')],
                      age: Annotated[int, Path(ge=14,
                                               le=99,
                                               description='Ваш возраст',
                                               example='35')]):
    users[str(user_id)] = f"Имя: {username}, возраст: {age}"
    return f'The user {user_id} is updated'


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1,
                                                   le=1000,
                                                   description='ID пользователя',
                                                   example='35')]):
    users.pop(str(user_id))
    return f'The user {user_id} is deleted'

