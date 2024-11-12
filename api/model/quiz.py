from sqlmodel import SQLModel
from .question import QuestionForm


class QuizForm(SQLModel):
    title: str = "Trivia sobre hechizos del mundo mágico"
    questions: list[QuestionForm]
