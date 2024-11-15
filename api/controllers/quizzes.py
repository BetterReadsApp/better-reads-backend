from fastapi import APIRouter, Depends, Header, HTTPException
from sqlmodel import Session, select
from typing import Annotated
from api.db import get_session, get_book_by_id, get_user_by_field, get_quiz_by_id
from api.model.quiz import QuizForm, Quiz
from api.model.question import Question
from api.model.answer import QuizAnswerForm, Answer
from api.formatters.quiz_formatter import QuizFormatter

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


@router.get("/{quiz_id}")
def get_quiz(
    quiz_id: int,
    session: Session = Depends(get_session),
):
    quiz = get_quiz_by_id(quiz_id, session)
    return QuizFormatter.format(quiz)


@router.put("/{quiz_id}")
def edit_quiz(
    quiz_id: int,
    quiz_form: QuizForm,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    if len(quiz_form.questions) < MIN_QUESTIONS_PER_QUIZ:
        raise HTTPException(
            status_code=400,
            detail=f"A quiz should have at least {MIN_QUESTIONS_PER_QUIZ} question",
        )

    quiz = get_quiz_by_id(quiz_id, session)

    user = get_user_by_field("id", auth, session)
    if user.id != quiz.book.author.id:
        raise HTTPException(
            status_code=401,
            detail="You must be the author of the book to edit the quiz",
        )

    query = (
        select(Quiz)
        .where(Quiz.book_id == quiz.book_id)
        .where(Quiz.id != quiz.id)
        .where(Quiz.title == quiz_form.title)
    )
    quiz_with_same_title = session.exec(query).first()
    if quiz_with_same_title:
        raise HTTPException(
            status_code=403,
            detail="Title already taken by another quiz for the same book",
        )

    quiz.title = quiz_form.title
    session.query(Question).filter(Question.quiz_id == quiz.id).delete()
    quiz.questions = [
        Question(
            title=q.title,
            choice_1=q.choice_1,
            choice_2=q.choice_2,
            choice_3=q.choice_3,
            choice_4=q.choice_4,
            correct_choice=q.correct_choice,
            quiz_id=quiz.id,
        )
        for q in quiz_form.questions
    ]

    session.commit()
    session.refresh(quiz)
    return QuizFormatter.format(quiz)


@router.get("/{quiz_id}/answers")
def get_quiz_answer(
    quiz_id: int,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    user = get_user_by_field("id", auth, session)
    quiz = get_quiz_by_id(quiz_id, session)
    return QuizFormatter.format_answer(quiz, user)


@router.post("/{quiz_id}/answers")
def answer_quiz(
    quiz_id: int,
    quiz_answer: QuizAnswerForm,
    session: Session = Depends(get_session),
    auth: Annotated[int, Header(description=AUTH_HEADER_DESCRIPTION)] = None,
):
    user = get_user_by_field("id", auth, session)
    quiz = get_quiz_by_id(quiz_id, session)

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
