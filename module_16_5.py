from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory='templates')
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
async def list_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/users/{user_id}')
async def get_user(request: Request, user_id) -> HTMLResponse:
    return_user = [user for user in users if str(user.id) == user_id]
    return templates.TemplateResponse('users.html', {'request': request, 'user': return_user[0]})


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=3,
                                                  max_length=15,
                                                  description='Имя пользователя',
                                                  example='mistic')],
                   age: Annotated[int, Path(ge=14,
                                            le=99,
                                            description='Ваш возраст',
                                            example='35')]):
    try:
        user_id = str(int(users[len(users) - 1].id) + 1)
    except:
        user_id = '1'
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


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
    found = False
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            updated = user
            found = True
            break
    if found:
        return updated
    else:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1,
                                                   le=1000,
                                                   description='ID пользователя',
                                                   example='35')]):
    found = False
    index = 0
    for user in users:
        if user.id == user_id:
            deleted = users.pop(index)
            found = True
            break
        else:
            index += 1
    if found:
        return deleted
    else:
        raise HTTPException(status_code=404, detail='User was not found')