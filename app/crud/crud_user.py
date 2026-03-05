from typing import List, Optional
# List — список значень
# Optional — значення може бути типу або None

from app.db.fake_db import fake_user_db
# fake_user_db — це наш словник, який імітує базу даних

from app.schemas.user import UserCreate, UserInDB, UserUpdate
# UserCreate — схема для створення (POST)
# UserUpdate — схема для оновлення (PUT)
# UserInDB — модель, яка зберігається у "БД"


def _hash_password(password: str) -> str:
    # Проста заглушка для хешування пароля
    # У реальному проєкті тут має бути bcrypt або інший алгоритм
    return "hashed:" + password


def list_users() -> List[UserInDB]:
    # Повертає список всіх користувачів із словника
    return list(fake_user_db.data.values())


def get_user(user_id: int) -> Optional[UserInDB]:
    # Повертає користувача по ID
    # Якщо ID не існує — поверне None
    return fake_user_db.data.get(user_id)


def get_user_by_email(email: str) -> Optional[UserInDB]:
    # Пошук користувача по email
    # Проходимо по всіх значеннях словника
    for u in fake_user_db.data.values():
        if u.email == email:
            return u
    return None


def create_user(user_in: UserCreate) -> UserInDB:
    # Перевірка: чи не існує вже користувач з таким email
    if get_user_by_email(user_in.email) is not None:
        raise ValueError("Email already exists")

    # Генеруємо новий ID
    user_id = fake_user_db.next_id()

    # Створюємо об'єкт користувача для зберігання
    user = UserInDB(
        id=user_id,
        email=user_in.email,
        full_name=user_in.full_name,
        is_active=user_in.is_active,
        hashed_password=_hash_password(user_in.password),
    )

    # Записуємо в словник
    fake_user_db.data[user_id] = user

    return user


def update_user(user_id: int, user_in: UserUpdate) -> Optional[UserInDB]:
    # Отримуємо існуючого користувача
    existing = get_user(user_id)

    # Якщо користувача немає — повертаємо None
    if existing is None:
        return None

    # Якщо змінюється email — перевіряємо, щоб він не був зайнятий
    if user_in.email is not None and user_in.email != existing.email:
        if get_user_by_email(user_in.email) is not None:
            raise ValueError("Email already exists")

    # Перетворюємо модель у словник
    data = existing.model_dump()

    # Беремо тільки ті поля, які реально передали в PUT
    patch = user_in.model_dump(exclude_unset=True)

    # Якщо оновлюється пароль — хешуємо його
    if "password" in patch:
        data["hashed_password"] = _hash_password(patch.pop("password"))

    # Оновлюємо дані
    data.update(patch)

    # Створюємо новий об'єкт моделі
    updated = UserInDB(**data)

    # Перезаписуємо в словнику
    fake_user_db.data[user_id] = updated

    return updated


def delete_user(user_id: int) -> bool:
    # Видаляємо користувача зі словника
    # pop повертає None, якщо ключа немає
    return fake_user_db.data.pop(user_id, None) is not None