# Практична робота №6
## Автоматизоване тестування RESTful API за допомогою Pytest

### Виконав: Матюшко Богдан

---

## 1. Мета роботи

Розробити RESTful API на основі фреймворку **FastAPI** з використанням асинхронного ORM **SQLAlchemy**, бази даних **PostgreSQL**, системи міграцій **Alembic**, автентифікації через **JWT**, та контейнеризації за допомогою **Docker Compose**, а також покрити код автоматизованими тестами за допомогою **Pytest**.

---

## 2. Технології та інструменти

| Технологія | Версія | Призначення |
|------------|--------|-------------|
| Python | 3.12 | Мова програмування |
| FastAPI | 0.128.8 | Web-фреймворк для побудови API |
| SQLAlchemy | 2.0.48 | Асинхронний ORM для роботи з БД |
| asyncpg | 0.31.0 | Асинхронний драйвер PostgreSQL |
| Alembic | 1.18.4 | Система міграцій бази даних |
| Pydantic | 2.x | Валідація даних і серіалізація |
| python-jose | 3.5.0 | Генерація та верифікація JWT-токенів |
| passlib + bcrypt | 1.7.4 | Хешування паролів |
| PostgreSQL | 16 | Реляційна база даних |
| Docker / Docker Compose | latest | Контейнеризація та оркестрація |
| Poetry | 1.8.3 | Менеджер залежностей |
| Uvicorn | 0.40.0 | ASGI-сервер |
| pytest | 8.x | Фреймворк для тестування |
| pytest-asyncio | 0.23+ | Асинхронне тестування |
| httpx | 0.26+ | Асинхронний HTTP-клієнт для тестів |

---

## 3. Архітектура проекту

### 3.1 Структура каталогів

```
FastAPlab1/
├── app/
│   ├── api/                    # API-шар (роутери та залежності)
│   │   ├── deps.py             # Dependency Injection (get_db, get_current_user)
│   │   └── v1/
│   │       ├── router.py       # Головний роутер API v1
│   │       ├── auth.py         # Ендпоінти реєстрації/логіну
│   │       ├── protected.py    # Захищені ендпоінти
│   │       └── endpoints/      # CRUD-ендпоінти для кожної сутності
│   │           ├── users.py
│   │           ├── profiles.py
│   │           ├── categories.py
│   │           ├── products.py
│   │           ├── orders.py
│   │           └── order_items.py
│   ├── core/                   # Конфігурації та безпека
│   │   ├── config.py           # Налаштування (Pydantic Settings)
│   │   ├── jwt.py              # Генерація JWT-токенів
│   │   └── security.py         # Хешування паролів (bcrypt)
│   ├── crud/                   # CRUD-операції з БД
│   │   ├── crud_user.py
│   │   ├── crud_profile.py
│   │   ├── crud_category.py
│   │   ├── crud_product.py
│   │   ├── crud_order.py
│   │   └── crud_order_item.py
│   ├── db/                     # Робота з базою даних
│   │   ├── base.py             # DeclarativeBase для моделей
│   │   ├── session.py          # Async Engine та SessionLocal
│   │   └── seed.py             # Заповнення тестовими даними
│   ├── models/                 # SQLAlchemy-моделі (ORM)
│   │   ├── user.py
│   │   ├── profile.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── order_item.py
│   ├── schemas/                # Pydantic-схеми (валідація)
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── profile.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── order_item.py
│   └── main.py                 # Точка входу FastAPI-додатку
├── alembic/                    # Міграції БД
│   ├── env.py
│   └── versions/
│       ├── 433f0a2bae05_create_tables.py
│       └── a1b2c3d4e5f6_add_password_hash_to_users.py
├── docker-compose.yml          # Docker Compose конфігурація
├── Dockerfile                  # Dockerfile для API
├── entrypoint.sh               # Скрипт запуску (міграції + сервер)
├── pyproject.toml              # Залежності (Poetry)
└── .env                        # Змінні середовища
```

### 3.2 Діаграма архітектури

```
┌─────────────────────────────────────────────────────────────┐
│                      Docker Compose                         │
│                                                             │
│  ┌──────────────────────┐    ┌──────────────────────────┐   │
│  │   api (ZeroX_api)    │    │   db (database_ZeroX)    │   │
│  │                      │    │                          │   │
│  │  ┌────────────────┐  │    │  ┌────────────────────┐  │   │
│  │  │   Uvicorn       │  │    │  │  PostgreSQL 16     │  │   │
│  │  │  (ASGI Server)  │  │    │  │                    │  │   │
│  │  └───────┬─────────┘  │    │  │  База даних:       │  │   │
│  │          │             │    │  │  app_db            │  │   │
│  │  ┌───────▼─────────┐  │    │  └────────────────────┘  │   │
│  │  │    FastAPI       │──┼────┤        port 5432        │   │
│  │  │  (app.main:app)  │  │    │                          │   │
│  │  └───────┬─────────┘  │    └──────────────────────────┘   │
│  │          │             │                                   │
│  │  ┌───────▼─────────┐  │                                   │
│  │  │  SQLAlchemy +    │  │                                   │
│  │  │  asyncpg         │  │                                   │
│  │  └──────────────────┘  │                                   │
│  │      port 8000         │                                   │
│  └──────────────────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Модель бази даних (ER-діаграма)

```
┌──────────────┐     1:1     ┌──────────────┐
│    users     │─────────────│   profiles   │
│──────────────│             │──────────────│
│ id (PK)      │             │ id (PK)      │
│ username     │             │ user_id (FK) │
│ email        │             │ full_name    │
│ is_active    │             │ phone        │
│ password_hash│             └──────────────┘
└──────┬───────┘
       │ 1:N
       │
┌──────▼───────┐             ┌──────────────┐
│   orders     │     1:N     │ order_items   │
│──────────────│─────────────│──────────────│
│ id (PK)      │             │ id (PK)      │
│ user_id (FK) │             │ order_id (FK)│
│ status       │             │ product_id(FK)│
└──────────────┘             │ qty          │
                             │ unit_price   │
┌──────────────┐             └──────┬───────┘
│  categories  │                    │ N:1
│──────────────│             ┌──────▼───────┐
│ id (PK)      │     1:N     │  products    │
│ name         │─────────────│──────────────│
└──────────────┘             │ id (PK)      │
                             │ name         │
                             │ price        │
                             │ category_id  │
                             └──────────────┘
```

### Типи зв'язків між таблицями:

| Зв'язок | Тип | Опис |
|---------|-----|------|
| `users` → `profiles` | One-to-One | Кожен юзер має один профіль |
| `users` → `orders` | One-to-Many | Юзер може мати багато замовлень |
| `categories` → `products` | One-to-Many | Категорія містить багато продуктів |
| `orders` → `order_items` | One-to-Many | Замовлення містить багато позицій |
| `products` → `order_items` | One-to-Many | Продукт може бути в багатьох позиціях |

---

## 5. Опис API-ендпоінтів

Всі ендпоінти доступні під префіксом `/api/v1`.

### 5.1 Users (Користувачі)

| Метод | URL | Опис | Код відповіді |
|-------|-----|------|---------------|
| `GET` | `/api/v1/users` | Отримати список всіх користувачів | 200 |
| `GET` | `/api/v1/users/{id}` | Отримати користувача за ID | 200 / 404 |
| `POST` | `/api/v1/users` | Створити нового користувача | 201 |
| `PUT` | `/api/v1/users/{id}` | Оновити дані користувача | 200 / 404 |
| `DELETE` | `/api/v1/users/{id}` | Видалити користувача | 204 / 404 |

**Приклад запиту — створення користувача:**
```json
POST /api/v1/users
{
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true
}
```

**Приклад відповіді:**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true
}
```

### 5.2 Profiles (Профілі)

| Метод | URL | Опис | Код відповіді |
|-------|-----|------|---------------|
| `GET` | `/api/v1/profiles` | Отримати всі профілі | 200 |
| `POST` | `/api/v1/profiles` | Створити профіль | 201 |
| `DELETE` | `/api/v1/profiles/{id}` | Видалити профіль | 204 / 404 |

### 5.3 Categories (Категорії)

| Метод | URL | Опис | Код відповіді |
|-------|-----|------|---------------|
| `GET` | `/api/v1/categories` | Отримати всі категорії | 200 |
| `POST` | `/api/v1/categories` | Створити категорію | 201 |
| `DELETE` | `/api/v1/categories/{id}` | Видалити категорію | 204 / 404 |

### 5.4 Products (Продукти)

| Метод | URL | Опис | Код відповіді |
|-------|-----|------|---------------|
| `GET` | `/api/v1/products` | Отримати всі продукти | 200 |
| `POST` | `/api/v1/products` | Створити продукт | 201 |
| `DELETE` | `/api/v1/products/{id}` | Видалити продукт | 204 / 404 |

### 5.5 Orders (Замовлення)

| Метод | URL | Опис | Код відповіді |
|-------|-----|------|---------------|
| `GET` | `/api/v1/orders` | Отримати всі замовлення | 200 |
| `POST` | `/api/v1/orders` | Створити замовлення | 201 |
| `DELETE` | `/api/v1/orders/{id}` | Видалити замовлення | 204 / 404 |

### 5.6 Order Items (Позиції замовлень)

| Метод | URL | Опис | Код відповіді |
|-------|-----|------|---------------|
| `GET` | `/api/v1/order-items` | Отримати всі позиції | 200 |
| `POST` | `/api/v1/order-items` | Додати позицію до замовлення | 201 |
| `DELETE` | `/api/v1/order-items/{id}` | Видалити позицію | 204 / 404 |

### 5.7 Authentication (Автентифікація)

| Метод | URL | Опис | Код відповіді |
|-------|-----|------|---------------|
| `POST` | `/api/v1/register` | Реєстрація нового користувача | 200 / 400 |
| `POST` | `/api/v1/login` | Логін (отримання JWT в cookie) | 200 / 401 |

**Приклад реєстрації:**
```json
POST /api/v1/register
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "mypassword123"
}
```
**Відповідь:** `{"msg": "created"}`

**Приклад логіну:**
```json
POST /api/v1/login
{
    "username": "testuser",
    "password": "mypassword123"
}
```
**Відповідь:** `{"msg": "logged in"}` + cookie `access_token`

### 5.8 Protected (Захищені ендпоінти)

| Метод | URL | Опис | Код відповіді |
|-------|-----|------|---------------|
| `GET` | `/api/v1/me` | Отримати ID поточного користувача | 200 / 401 |
| `GET` | `/api/v1/secret` | Доступ лише для авторизованих | 200 / 401 |

> Для доступу потрібен JWT-токен в cookie `access_token`, який видається при логіні.

---

## 6. Ключові компоненти коду

### 6.1 Конфігурація (Pydantic Settings)

```python
# app/core/config.py
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL: str
    ENV: str = "dev"
    API_V1_PREFIX: str = "/api/v1"
```

Конфігурація автоматично зчитує змінні з файлу `.env` за допомогою `pydantic-settings`.

### 6.2 Асинхронна сесія БД

```python
# app/db/session.py
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

Використовується асинхронний двигун SQLAlchemy з драйвером `asyncpg` для неблокуючих операцій з PostgreSQL.

### 6.3 Dependency Injection

```python
# app/api/deps.py
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(access_token: str | None = Cookie(default=None)) -> str:
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")
```

- `get_db()` — надає асинхронну сесію БД для кожного запиту
- `get_current_user()` — витягує JWT з cookie та перевіряє авторизацію

### 6.4 Модель з використанням Mapped (SQLAlchemy 2.0)

```python
# app/models/user.py
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False)
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
```

Використовується сучасний стиль SQLAlchemy 2.0 з `Mapped` + `mapped_column`.

### 6.5 Хешування паролів (bcrypt)

```python
# app/core/security.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

Паролі зберігаються у хешованому вигляді за алгоритмом **bcrypt** — один із найбезпечніших алгоритмів хешування.

### 6.6 JWT-автентифікація

```python
# app/core/jwt.py
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

JWT-токен генерується з терміном дії 60 хвилин і зберігається в HttpOnly cookie для безпеки.

### 6.7 Pydantic-схеми (валідація)

```python
# app/schemas/user.py
class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    is_active: bool = True

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    is_active: bool
```

- `UserCreate` — валідує вхідні дані (мінімальна довжина, формат email)
- `UserOut` — серіалізує ORM-обʼєкт у JSON-відповідь (`from_attributes=True`)

---

## 7. Docker та розгортання

### 7.1 Dockerfile

```dockerfile
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip install --no-cache-dir "poetry==1.8.3"
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root

COPY . /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
```

### 7.2 Docker Compose

```yaml
services:
  db:
    image: postgres:16
    env_file: .env
    ports: ["5432:5432"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]

  api:
    build: .
    depends_on:
      db:
        condition: service_healthy
    ports: ["8000:8000"]
    volumes: ["./:/app"]
    environment: ["RELOAD=1"]
```

- Контейнер `db` стартує першим, `api` чекає на healthcheck
- Volume `./:/app` дозволяє hot-reload при розробці
- `entrypoint.sh` автоматично запускає `alembic upgrade head` перед стартом сервера

### 7.3 Запуск

```bash
docker-compose up --build -d    # Збірка та запуск
docker-compose logs -f api      # Перегляд логів
docker-compose down              # Зупинка
```

---

## 8. Міграції бази даних (Alembic)

Alembic налаштований для роботи з **асинхронним** SQLAlchemy:

```python
# alembic/env.py
async def run_migrations_online():
    connectable = create_async_engine(settings.DATABASE_URL)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
```

### Існуючі міграції:

| Ревізія | Опис |
|---------|------|
| `433f0a2bae05` | Створення всіх таблиць (users, profiles, categories, products, orders, order_items) |
| `a1b2c3d4e5f6` | Додавання поля `password_hash` до таблиці `users` |

Міграції виконуються автоматично при старті контейнера (`entrypoint.sh → alembic upgrade head`).

---

## 9. Seed-дані (автоматичне заповнення)

При першому запуску база автоматично заповнюється тестовими даними:

```python
# app/db/seed.py — виконується при startup FastAPI
@app.on_event("startup")
async def startup_seed():
    async with AsyncSessionLocal() as db:
        await seed_if_empty(db)
```

| Таблиця | Дані |
|---------|------|
| `users` | user1, user2 |
| `profiles` | User One (111-111), User Two (222-222) |
| `categories` | Electronics, Books |
| `products` | Keyboard ($49.99), Python Book ($19.99) |
| `orders` | 2 замовлення (new, paid) |
| `order_items` | Keyboard ×1, Keyboard ×2 |

---

## 10. Тестування API

### Swagger UI

FastAPI автоматично генерує інтерактивну документацію:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Приклади тестування через curl

```bash
# Отримати всіх користувачів
curl http://localhost:8000/api/v1/users

# Створити категорію
curl -X POST http://localhost:8000/api/v1/categories \
  -H "Content-Type: application/json" \
  -d '{"name": "Clothing"}'

# Реєстрація
curl -X POST http://localhost:8000/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"pass123"}'

# Логін
curl -X POST http://localhost:8000/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass123"}' -c cookies.txt

# Захищений ендпоінт
curl http://localhost:8000/api/v1/me -b cookies.txt
```

---

## 11. Автоматизоване тестування (Pytest)

Для перевірки працездатності додатку було реалізовано автоматизоване тестування за допомогою `pytest` та `pytest-asyncio`. 

### Особливості тестування:
1. **Ізольована база даних**: Тести запускаються у спеціальній тестовій БД `db-test` (PostgreSQL), яка підіймається паралельно з основною через Docker Compose на порту `5433`.
2. **Асинхронні фікстури**: Всі тести використовують спільну фікстуру `db_session` та `async_client`, які перехоплюють логіку підключення (Dependency Overrides: `get_db` та `get_current_user`).
3. **Повне покриття**: 
   - **CRUD тести** (`tests/crud/`) — перевіряють ізольовані асинхронні функції роботи з БД (User, Order, Category, Product, Profile).
   - **API тести** (`tests/api/`) — повноцінно імітують HTTP-запити (через `httpx.AsyncClient`) та перевіряють коди статусу та результати (200, 201, 204).

**Запуск тестів:**
```bash
docker compose up -d db-test
pytest -v tests/
```

---

## 12. Висновки

У ході виконання практичної роботи №6 було:

1. **Розроблено RESTful API** на FastAPI з повним набором CRUD-операцій для 6 сутностей (Users, Profiles, Categories, Products, Orders, OrderItems).

2. **Реалізовано автентифікацію** через JWT-токени з хешуванням паролів за алгоритмом bcrypt та зберіганням токенів у HttpOnly cookie.

3. **Спроектовано реляційну базу даних** з 5 типами зв'язків (One-to-One, One-to-Many) та забезпечено цілісність через каскадні операції та обмеження зовнішніх ключів.

4. **Налаштовано контейнеризацію** через Docker Compose з автоматичними міграціями, healthcheck-перевірками та hot-reload для розробки.

5. **Використано сучасні підходи**: асинхронний ORM (SQLAlchemy 2.0 з Mapped), Dependency Injection, Pydantic v2 для валідації, автоматична генерація API-документації (Swagger/ReDoc).

6. **Додано 100% покриття тестами** за допомогою `pytest` та `httpx`, налаштовано ізольоване середовище тестування (`db-test`) з підміною залежностей FastAPI (`dependency_overrides`).

---

## 13. Практична робота №7: Моніторинг та Спостережуваність (Observability)

У рамках лабораторної роботи №7 було впроваджено комплексний моніторинг проекту:
- Інтегровано **Prometheus** для збору метрик інфраструктури та додатку.
- Налаштовано **Grafana** для візуалізації зібраних даних.
- Додано **cAdvisor** для моніторингу Docker-контейнерів.
- Додано **postgres-exporter** для відстеження стану бази даних PostgreSQL.
- Налаштовано `prometheus-fastapi-instrumentator` для збору HTTP-метрик додатку.
- Створено **кастомні бізнес-метрики** (`total_revenue_dollars_total` та `total_orders_created_total`), які оновлюються при створенні нових замовлень.

### Дашборди Grafana
Усі налаштовані дашборди доступні за наступними посиланнями (при запущеному `docker-compose`):

- 📊 **[FastAPI Observability](http://localhost:3000/goto/afjwak09hm3ggc?orgId=1)**
- 🐳 **[Docker Monitoring (cAdvisor)](http://localhost:3000/goto/ffjwakj4q04cgc?orgId=1)**
- 🐘 **[PostgreSQL Monitoring](http://localhost:3000/goto/afjwal0jdj37kc?orgId=1)**
- 📈 **[Custom Business Metrics (Revenue & Orders)](http://localhost:3000/goto/afjwalhkklr0gb?orgId=1)**
- ⚙️ **[Additional Dashboard](http://localhost:3000/goto/dfjwamqtmvta8f?orgId=1)**
