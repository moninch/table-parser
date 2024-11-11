from typing import Optional
from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    Наименование: Optional[str] = None
    Город: Optional[str] = None
    Категория: Optional[str] = None
    Для_кого: Optional[str] = None
    Стоимость: Optional[int] = None
    Кол_во_ягод: Optional[int] = None
    Размер_упаковки: Optional[str] = None
    Шоколад: Optional[str] = None
    Наполнение_набора: Optional[str] = None
    Ссылка: Optional[str] = None
