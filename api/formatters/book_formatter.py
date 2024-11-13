from api.model.user import UserMini


class BookFormatter:
    @classmethod
    def format_for_user(cls, book, user):
        book_dict = book.__dict__
        book_dict["author"] = UserMini.model_validate(book.author)

        if user:
            book_dict["your_rating"] = cls.get_user_rating(user, book.ratings)
            book_dict["your_review"] = cls.get_user_review(user, book.reviews)
        book_dict["ratings"] = cls.format_ratings(book.ratings)
        book_dict["reviews"] = cls.format_reviews(book.reviews)
        book_dict["has_quizzes"] = len(book.quizzes) > 0
        book_dict.pop("author_id")
        return book_dict

    @classmethod
    def get_user_rating(cls, user, ratings):
        return next(
            (rating.value for rating in ratings if rating.user_id == user.id), None
        )

    @classmethod
    def get_user_review(cls, user, reviews):
        return next(
            (review.review for review in reviews if review.user_id == user.id), None
        )

    @classmethod
    def format_ratings(cls, ratings):
        return list(
            map(
                lambda rating: {
                    "value": rating.value,
                    "user_id": rating.user_id,
                    "name": rating.user.name,
                    "last_name": rating.user.last_name,
                },
                ratings,
            )
        )

    @staticmethod
    def format_reviews(reviews):
        return list(
            map(
                lambda review: {
                    "review": review.review,
                    "user_id": review.user_id,
                    "name": review.user.name,
                    "last_name": review.user.last_name,
                },
                reviews,
            )
        )
