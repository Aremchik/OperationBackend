from datetime import datetime, timedelta
from typing import Optional
import jwt

# Секретный ключ для подписи JWT токенов
SECRET_KEY = "SECRET_KEY"
# Алгоритм, используемый для подписи токенов
ALGORITHM = "HS256"
# Время истечения токена по умолчанию (в минутах)
ACCESS_TOKEN_EXPIRE_MINUTES = 180


# Генерация JWT токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Создает JWT токен с заданными данными и сроком действия.
    """
    # Копируем данные для сохранения в токене
    to_encode = data.copy()

    # Устанавливаем время истечения токена
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Добавляем время истечения в данные токена
    to_encode.update({"exp": expire})

    # Генерируем токен с использованием секретного ключа и алгоритма
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Проверка JWT токена
def verify_token(token: str):
    """
    Проверяет валидность JWT токена и возвращает его данные, если токен действителен.
    """
    try:
        # Декодируем токен и проверяем его подпись и срок действия
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # payload содержит декодированные данные токена
    except jwt.PyJWTError:
        # Возвращаем None, если токен недействителен или истек
        return None
