class QuizFormatter:
    @classmethod
    def format_answer_for_user(cls, quiz, user):
        user_answers = list(
            filter(
                lambda answer: answer.question.quiz_id == quiz.id,
                user.questions_answered,
            )
        )
        quiz_dict = quiz.__dict__
        quiz_dict["questions_answered"] = [] if user_answers else None
        for answer in user_answers:
            answer_dict = {"selected_choice": answer.selected_choice}
            answer_dict.update(answer.question)
            answer_dict.pop("quiz_id")
            quiz_dict["questions_answered"].append(answer_dict)
        return quiz_dict
