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


class QuizResponse(SQLModel):
    title: str
    book_id: Optional[int]
    questions: List[QuestionForm]

    @classmethod
    def from_quiz(cls, quiz: Quiz):
        return cls(
            title=quiz.title,
            book_id=quiz.book_id,
            questions=[QuestionForm(
                title=q.title,
                choice_1=q.choice_1,
                choice_2=q.choice_2,
                choice_3=q.choice_3,
                choice_4=q.choice_4,
                correct_choice=q.correct_choice
            ) for q in quiz.questions]
        )
    