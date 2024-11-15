from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class AnswerForm(SQLModel):
    question_id: int = Field(default=None, foreign_key="questions.id")
    selected_choice: int = Field(ge=1, le=4, nullable=False)


class QuizAnswerForm(SQLModel):
    answers: list[AnswerForm]


class Answer(AnswerForm, table=True):
    __tablename__ = "answers"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

    user: "User" = Relationship(back_populates="questions_answered")
    question: "Question" = Relationship(back_populates="answers")
