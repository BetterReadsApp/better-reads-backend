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
        user_dict.pop("password")
        user_dict.pop("email")
        return user_dict
