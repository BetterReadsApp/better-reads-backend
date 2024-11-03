from fastapi import FastAPI
from api.db import init_db
from api.controllers import auth, books, shelves, users


app = FastAPI(
    title="BetterReads",
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "arta"},
        "tryItOutEnabled": True,
    },
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(shelves.router)


@app.on_event("startup")
def on_startup():
    init_db()
