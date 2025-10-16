from fastapi import FastAPI,HTTPException,Request
from pydantic import BaseModel,fields
from typing import Union,Optional
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid input. Please check your request data.",
            "details": exc.errors()  
        }
    )
@app.exception_handler(HTTPException)
async def global_http_handler(request: Request,exc:Exception):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc.detail)}
    )

@app.get("/err")
def get_error():
    return 1/0

class Author(BaseModel):
    name: str=fields(..., min_length=3)
    email: str

class Book(BaseModel):
    id: int=fields(..., gt=0)
    title: str=fields(..., min_length=3)
    author: Author
    publish_year: int | None = None
    price: float | None = None
    in_stock: bool | None = None



books: list[Book] = []

@app.post("/books")
def create_book(book: Book):
    new_book_ids = [b for b in books if b.id == book.id]
    if new_book_ids:
        raise HTTPException(status_code=400, detail="Book with this ID already exists")
    books.append(book)
    return book

@app.get("/books/")
def get_books(author:Optional[str]=None,limit:Optional[int]=None):
    new_books=[b for b in books if (author is None or b.author.name==author)]
    if limit is not None:
        new_books=new_books[:limit]
    return new_books
#since both query parameters are optional, we can call this endpoint without any query parameters too

@app.get("/books/{book_id}")
def get_books(book_id: str):
    if not book_id.isdigit():
        raise HTTPException(status_code=400, detail="ID must be a number")
    id = int(book_id)
    book = next((book for book in books if book.id == id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/books/search/")
def search_books(title:str=None,author:str=None,max_price:float=None):
    new_books=[b for b in books if (b.title==title) and (b.author.name==author) and (b.price<=max_price)]
    return new_books
#FastAPI inspects your function parameters, reads matching query parameters from the URL, converts them using type hints, and injects them into your function automatically.

@app.delete("/books/{book_id}")
def update_book(book_id: int, book: Book):
    global books
    books=[b for b in books if b.id!=book.id]
    return 

@app.put("/books/{book_id}/", response_model=Book)
def update_book(book_id: int,new_title:str,author:Optional[Author]=None):
    global books
    new_book=[b for b in books if b.id==book_id][0]
    books=[b for b in books if b.id!=book_id]

    new_book.title=new_title
    if author:
        new_book.author=author
    books.append(new_book)
    return new_book


    
