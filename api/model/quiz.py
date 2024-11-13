from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .question import QuestionForm


class QuizForm(SQLModel):
    title: str
    questions: List[QuestionForm]


class Quiz(SQLModel, table=True):
    __tablename__ = "quizzes"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    book_id: Optional[int] = Field(default=None, foreign_key="books.id")

    book: Optional["Book"] = Relationship(back_populates="quizzes")
    questions: List["Question"] = Relationship(back_populates="quiz")
