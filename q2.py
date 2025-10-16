from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from typing import Optional
app = FastAPI()


class BaseConfigModel(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, 
        validate_assignment=True     
    )

class Base_book(BaseConfigModel):
    id :Optional[int] = None
    isbn:str
    publish_year:int
  

class Base_author(BaseConfigModel):
    name:str
    email:str
class BookCreate(Base_book):
    price:int
    stock:int

class BookResponse(Base_book):
    id:int
    available:bool


class BookWithAuthor(BookCreate, Base_author):
    pass
old_book = BookCreate(
    isbn="123-456",
    publish_year=2024,
    price=49,
    stock=20
)
print("Original book:", old_book)
# Create new edition
new_edition = old_book.model_copy(update={
    "published_year": 2025,
    "stock": 50
})


print("New edition:", new_edition)


book_response = new_edition.model_validate({**new_edition.model_dump(), "id": 1,
"available": True})
print("Book response:", book_response)

class BookWithNestedAuthor(BookCreate):
    author: Base_author

book_with_author = BookWithNestedAuthor.model_validate({**new_edition.model_dump(), "author": {
    "name": "John Doe",
    "email": "john.doe@example.com"
}})
print("Book with author:", book_with_author)