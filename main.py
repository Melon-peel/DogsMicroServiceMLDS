from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]



# Путь / 
@app.get('/')
def root():
    return "Для доступа к документации перейдите в раздел /docs"

# Путь /post 
@app.post('/post', response_model=Timestamp)
def get_post():
    current_time = datetime.now()
    new_id = post_db[-1].id + 1
    new_timestamp = Timestamp(id=new_id,
                 timestamp=int(round(current_time.timestamp())))
    return new_timestamp




@app.get('/dog', response_model=List[Dog])
def get_dogs(kind: DogType = None):
    # Получение списка собак
    if kind is None:
        return [i for i in dogs_db.values]
    else:
        # Получение собак по типу 
        searched_dogs = [{"name": dog.name, "pk": dog.pk, "kind": kind} for dog in dogs_db.values() if dog.kind == kind]
        return searched_dogs

# Запись собак 
@app.post('/dog', response_model=Dog)
def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=404, detail="Собака с таким ID уже существует")
    else:
        dogs_db.update({dog.pk: dog})
    return dog
    
# Получение собаки по id 
@app.get('/dog/{pk}', response_model=Dog)
def get_dog_by_pk(pk: int):
    dog_retrieved = dogs_db.get(pk)
    if dog_retrieved is None:
        raise HTTPException(status_code=404, detail="Собака с таким ID не найдена")
    else:
        return dog_retrieved

# Обновление собаки по id
@app.patch('/dog/{pk}', response_model=Dog)
def update_dog(pk: int, dog: Dog):
    if pk != dog.pk:
        raise HTTPException(status_code=404, detail="ID собаки и не совпадает с указанным")
    if pk in dogs_db:
        dogs_db.update({dog.pk: dog})
        return dog
    else:
        raise HTTPException(status_code=404, detail="Собака с таким ID не найдена")

