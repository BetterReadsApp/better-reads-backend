from api.model.user import UserMini
from api.model.shelf import ShelfMini


class UserFormatter:
    @classmethod
    def format_for_user(cls, user, requester_user):
        user_dict = user.__dict__
        if user != requester_user:
            user_dict["is_following"] = any(
                follower.id == requester_user.id for follower in user.followers
            )
        user_dict["shelves"] = list(map(ShelfMini.model_validate, user.shelves))
        user_dict["followers"] = list(map(UserMini.model_validate, user.followers))
        user_dict["following"] = list(map(UserMini.model_validate, user.following))
        user_dict["rated_books"] = cls.format_ratings(user.rated_books)
        user_dict["reviewed_books"] = cls.format_reviews(user.reviewed_books)
        user_dict.pop("password")
        return user_dict

    @classmethod
    def format_ratings(cls, ratings):
        return list(
            map(
                lambda rating: {
                    "value": rating.value,
                    "book_id": rating.book_id,
                    "title": rating.book.title,
                    "cover_image_url": rating.book.cover_image_url,
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
                    "book_id": review.book_id,
                    "title": review.book.title,
                    "cover_image_url": review.book.cover_image_url,
                },
                reviews,
            )
        )
