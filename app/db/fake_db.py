from typing import Dict  # Для типізації словника

from app.schemas.user import UserInDB  # Pydantic-модель користувача, як він зберігається в "БД"


class FakeUserDB:
    def __init__(self) -> None:
        # _data — це словник, який імітує базу даних.
        # Ключ: int (id користувача)
        # Значення: UserInDB (модель користувача)
        self._data: Dict[int, UserInDB] = {}

        # _id_seq — лічильник для автоматичної генерації ID
        self._id_seq: int = 0

    def next_id(self) -> int:
        # Збільшуємо лічильник на 1
        self._id_seq += 1

        # Повертаємо новий унікальний ID
        return self._id_seq

    @property
    def data(self) -> Dict[int, UserInDB]:
        # Повертає словник з усіма користувачами
        # Використовується CRUD-логікою
        return self._data


# Створюємо один глобальний екземпляр "бази даних"
# Його будуть використовувати всі CRUD-функції
fake_user_db = FakeUserDB()