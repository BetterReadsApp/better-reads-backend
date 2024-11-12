from sqlmodel import SQLModel


class QuestionForm(SQLModel):
    title: str = "¿Cuál es la peor de las maldiciones imperdonables?"
    choice_1: str = "Reducto"
    choice_2: str = "Crucio"
    choice_3: str = "Imperio"
    choice_4: str = "Avada Kedavra"
    correct_choice: int = 4
