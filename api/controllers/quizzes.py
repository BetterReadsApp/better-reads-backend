from fastapi import APIRouter, Depends, Header, HTTPException
from sqlmodel import Session, select
from typing import Annotated
from api.db import (
    get_session,
    get_book_by_id,
    get_user_by_field,
)
from api.model.quiz import QuizForm, Quiz, QuizResponse
from api.model.question import Question

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])
AUTH_HEADER_DESCRIPTION = "Id del usuario **logeado actualmente**"
MIN_QUESTIONS_PER_QUIZ = 1


@router.post("")
def create_quiz(
    quiz_form: QuizForm,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    if len(quiz_form.questions) < MIN_QUESTIONS_PER_QUIZ:
        raise HTTPException(
            status_code=400,
            detail=f"A quiz should have at least {MIN_QUESTIONS_PER_QUIZ} question",
        )

    book = get_book_by_id(quiz_form.book_id, session)
    user = get_user_by_field("id", auth, session)
    if user.id != book.author.id:
        raise HTTPException(
            status_code=401,
            detail="You must be the author of the book to create a quiz",
        )

    query = (
        select(Quiz)
        .where(Quiz.book_id == quiz_form.book_id)
        .where(Quiz.title == quiz_form.title)
    )
    quiz_with_same_title = session.exec(query).first()
    if quiz_with_same_title:
        raise HTTPException(
            status_code=403,
            detail="Title already taken by another quiz for the same book",
        )

    questions = list(map(Question.model_validate, quiz_form.questions))
    quiz = Quiz(title=quiz_form.title, book=book, questions=questions)

    session.add(quiz)
    session.commit()
    session.refresh(quiz)
    return quiz


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: int,
    session: Session = Depends(get_session),
):
    quiz = session.exec(select(Quiz).where(Quiz.id == quiz_id)).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz
