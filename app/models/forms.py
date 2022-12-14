from typing import List, Optional

from fastapi import Request

from app.models.helpers import is_digit


class PostLocationForm:
    """Модель формы получения и валидации данных локации и радиуса."""

    def __init__(self, request: Request):
        """Инициализация параметров формы."""
        self.request: Request = request
        self.location: Optional[str] = None
        self.radius: Optional[str] = None
        self.errors: List = []

    async def load_data(self):
        """Метод получения данных их формы."""
        form = await self.request.form()
        self.location = form.get("location", False)
        self.radius = form.get("radius", False)

    def is_valid(self):
        """Проверка валидности полученных данных."""
        if not self.location:
            self.errors.append("Введите адрес")
        if self.radius and not is_digit(self.radius):
            self.errors.append("Введите число")
        if not self.errors:
            return True
        return False
