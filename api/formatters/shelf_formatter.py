class ShelfFormatter:
    @staticmethod
    def format_for_user(shelf, user):
        shelf_dict = {
            "id": shelf.id,
            "name": shelf.name,
            "user_id": shelf.user_id,
            "books": [],
        }
        for book in shelf.books:
            book_dict = {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "pages": book.pages,
                "publication_date": book.publication_date,
                "average_rating": book.average_rating,
                "total_ratings": len(book.ratings),
            }
            if user:
                book_dict["your_rating"] = next(
                    (
                        rating.value
                        for rating in book.ratings
                        if rating.user_id == user.id
                    ),
                    None,
                )
            shelf_dict["books"].append(book_dict)
        return shelf_dict
