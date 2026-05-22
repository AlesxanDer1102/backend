from datetime import date
from typing import Optional

from sqlalchemy import Select, select

from db.models.autor import Autor
from db.models.genero import Genero
from db.models.libro import Libro


# patron builder : esta clase construye de forma fluida y paso a paso
# la consulta de busqueda de libros sobre el modelo ORM `Libro`.
class BookQueryBuilder:

    _DEFAULT_LIMIT = 20
    _DEFAULT_OFFSET = 0

    def __init__(self) -> None:
        self._query: Select = select(Libro)
        self._limit: int = self._DEFAULT_LIMIT
        self._offset: int = self._DEFAULT_OFFSET

    def with_title(self, title: Optional[str]) -> "BookQueryBuilder":
        if title:
            self._query = self._query.where(Libro.titulo.ilike(f"%{title}%"))
        return self

    def with_author(self, author: Optional[str]) -> "BookQueryBuilder":
        if author:
            self._query = self._query.join(Libro.autores).where(
                Autor.nombre.ilike(f"%{author}%")
            )
        return self

    def with_genre(self, genre: Optional[str]) -> "BookQueryBuilder":
        if genre:
            self._query = self._query.join(Libro.generos).where(
                Genero.nombre.ilike(f"%{genre}%")
            )
        return self

    def with_language(self, language: Optional[str]) -> "BookQueryBuilder":
        if language:
            self._query = self._query.where(Libro.lenguaje == language)
        return self

    def published_from(self, from_date: Optional[date]) -> "BookQueryBuilder":
        if from_date:
            self._query = self._query.where(from_date <= Libro.fecha_publicacion)
        return self

    def published_until(self, to_date: Optional[date]) -> "BookQueryBuilder":
        if to_date:
            self._query = self._query.where(Libro.fecha_publicacion <= to_date)
        return self

    def paginate(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> "BookQueryBuilder":
        if limit is not None:
            self._limit = limit
        if offset is not None:
            self._offset = offset
        return self

    def build(self) -> Select:
        """Devuelve la consulta final con orden y paginacion aplicados."""
        return (
            self._query
            .distinct()
            .order_by(Libro.id)
            .offset(self._offset)
            .limit(self._limit)
        )
