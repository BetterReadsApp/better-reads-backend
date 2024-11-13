from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class QuestionForm(SQLModel):
    title: str
    choice_1: str
    choice_2: str
    choice_3: str
    choice_4: str
    correct_choice: int


class Question(QuestionForm, table=True):
    __tablename__ = "questions"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: Optional[int] = Field(default=None, foreign_key="quizzes.id")

    quiz: Optional["Quiz"] = Relationship(back_populates="questions")
