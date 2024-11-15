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
from api.model.answer import QuizAnswerForm, Answer

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


@router.put("/{quiz_id}", response_model=QuizResponse)
def edit_quiz(
    quiz_id: int,
    quiz_update: QuizForm,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    if len(quiz_update.questions) < MIN_QUESTIONS_PER_QUIZ:
        raise HTTPException(
            status_code=400,
            detail=f"A quiz should have at least {MIN_QUESTIONS_PER_QUIZ} question",
        )

    quiz_original = session.exec(select(Quiz).where(Quiz.id == quiz_id)).first()
    if not quiz_original:
        raise HTTPException(status_code=404, detail="Quiz not found")

    user = get_user_by_field("id", auth, session)
    if user.id != quiz_original.book.author.id:
        raise HTTPException(
            status_code=401,
            detail="You must be the author of the book to edit the quiz",
        )

    query = (
        select(Quiz)
        .where(Quiz.book_id == quiz_original.book_id)
        .where(Quiz.id != quiz_original.id)
        .where(Quiz.title == quiz_update.title)
    )
    quiz_with_same_title = session.exec(query).first()
    if quiz_with_same_title:
        raise HTTPException(
            status_code=403,
            detail="Title already taken by another quiz for the same book",
        )

    quiz_original.title = quiz_update.title
    session.query(Question).filter(Question.quiz_id == quiz_original.id).delete()
    quiz_original.questions = [
        Question(
            title=q.title,
            choice_1=q.choice_1,
            choice_2=q.choice_2,
            choice_3=q.choice_3,
            choice_4=q.choice_4,
            correct_choice=q.correct_choice,
            quiz_id=quiz_original.id,
        )
        for q in quiz_update.questions
    ]

    session.commit()
    session.refresh(quiz_original)
    return quiz_original


@router.post("/{quiz_id}/answers")
def answer_quiz(
    quiz_id: int,
    quiz_answer: QuizAnswerForm,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    user = get_user_by_field("id", auth, session)
    quiz = session.exec(select(Quiz).where(Quiz.id == quiz_id)).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if any(answer.question.quiz_id == quiz_id for answer in user.questions_answered):
        raise HTTPException(status_code=403, detail="You already answered this quiz")

    if len(quiz.questions) != len(quiz_answer.answers):
        raise HTTPException(
            status_code=400, detail="You must answer all quiz questions at once"
        )

    questions_dict = {question.id: question for question in quiz.questions}

    for answer_form in quiz_answer.answers:
        answer = Answer.model_validate(answer_form)
        answer.user = user
        try:
            question = questions_dict[answer.question_id]
        except KeyError:
            raise HTTPException(
                status_code=403,
                detail=f"Question with id {answer.question_id} does not belong to this quiz",
            )
        question.answers.append(answer)

    session.add(quiz)
    session.commit()
    return {"detail": "Quiz answered successfully"}
