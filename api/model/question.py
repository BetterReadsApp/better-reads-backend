from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class QuestionForm(SQLModel):
    title: str = "¿Cuál es la peor de las maldiciones imperdonables?"
    choice_1: str = "Reducto"
    choice_2: str = "Crucio"
    choice_3: str = "Imperio"
    choice_4: str = "Avada Kedavra"
    correct_choice: int = 4


class Question(QuestionForm, table=True):
    __tablename__ = "questions"

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: Optional[int] = Field(default=None, foreign_key="quizzes.id")

    quiz: Optional["Quiz"] = Relationship(back_populates="questions")
