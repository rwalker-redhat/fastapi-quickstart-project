from fastapi import Body, APIRouter
from pydantic import BaseModel


router = APIRouter()


class Pet(BaseModel):
    name: str 
    animal: str 
    age: int


@router.post('/api/pets')
def pets(pet: Pet):
    return pet

