from api.model.user import UserMini


class ShelfFormatter:
    @staticmethod
    def format_for_user(shelf, user):
        shelf_dict = shelf.__dict__
        shelf_dict_books = []
        active_books = [book for book in shelf.books if book.is_active]
        for book in active_books:
            book_dict = book.__dict__
            book_dict["total_ratings"] = len(book.ratings)
            if user:
                book_dict["your_rating"] = next(
                    (
                        rating.value
                        for rating in book.ratings
                        if rating.user_id == user.id
                    ),
                    None,
                )
            book_dict["author"] = UserMini.model_validate(book.author)
            book_dict.pop("ratings")
            book_dict.pop("genre")
            book_dict.pop("author_id")
            book_dict.pop("summary")
            shelf_dict_books.append(book_dict)
        shelf_dict["books"] = shelf_dict_books
        return shelf_dict
