from api.model.question import QuestionWithId


class QuizFormatter:
    @classmethod
    def format(cls, quiz):
        quiz_dict = quiz.__dict__
        quiz_dict["questions"] = list(
            map(QuestionWithId.model_validate, quiz.questions)
        )
        return quiz_dict

    @classmethod
    def format_answer(cls, quiz, user):
        user_answers = list(
            filter(
                lambda answer: answer.question.quiz_id == quiz.id,
                user.questions_answered,
            )
        )
        quiz_dict = quiz.__dict__
        quiz_dict["questions_answered"] = []
        for answer in user_answers:
            answer_dict = {"selected_choice": answer.selected_choice}
            answer_dict.update(answer.question)
            answer_dict.pop("quiz_id")
            quiz_dict["questions_answered"].append(answer_dict)
        return quiz_dict
