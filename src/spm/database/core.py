import re
from typing import Annotated, Literal, TypeVar
from datetime import datetime
from sqlalchemy import String, Float, Integer, Boolean, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Query
from fastapi import Depends, Query as FastApiQuery
from spm import config
from .model import (
    SearchPaginationInputs
)

if not config.DATABASE_URL:
    raise ValueError('"DATABASE_URL" needs to be set as an environment variable')

engine = create_engine(
    config.DATABASE_URL,
)

class Base(DeclarativeBase):
    pass

T = TypeVar("T", bound=Base)

def create_all():
    Base.metadata.create_all(engine)


def search_pagination_parameters(
    page:Annotated[int, FastApiQuery(gt=0, lt=2147483647)],
    page_size:Annotated[int, FastApiQuery(gt=0, lt=2147483647)],
    q:Annotated[str, FastApiQuery(description="filter result using FIQL")] = "",
    sortby:Annotated[str, FastApiQuery()] = "id",
    order:Annotated[Literal["asc", "desc"], FastApiQuery()] = "asc",
) -> SearchPaginationInputs:
    return SearchPaginationInputs(
        page=page,
        page_size=page_size,
        q=q,
        sortby=sortby,
        order=order
    )

SearchPaginationParameters = Annotated[SearchPaginationInputs, Depends(search_pagination_parameters)]

def cast_value(column, value: str):
    col_type = column.type

    try:
        if isinstance(col_type, Integer):
            return int(value)

        if isinstance(col_type, Float):
            return float(value)

        if isinstance(col_type, Boolean):
            return value.lower() in ("true", "1", "yes")

        if isinstance(col_type, DateTime):
            # ISO 8601 → 2024-01-01T12:00:00
            return datetime.fromisoformat(value)

        if isinstance(col_type, String):
            return value

    except ValueError:
        return value  # fallback امن

    return value


def apply_fiql_filters(
    query: Query[T],
    model: type[T],
    fiql_str: str
) -> Query[T]:

    if not fiql_str:
        return query

    expressions = fiql_str.split(';')
    pattern = re.compile(r"(\w+)(==|!=|=gt=|=lt=|=ge=|=le=)(.+)")

    for expr in expressions:
        match = pattern.match(expr)
        if not match:
            continue

        field_name, operator, raw_value = match.groups()

        if not hasattr(model, field_name):
            continue

        column = getattr(model, field_name)
        value = cast_value(column, raw_value)

        if operator == "==":
            query = query.where(column == value)
        elif operator == "!=":
            query = query.where(column != value)
        elif operator == "=gt=":
            query = query.where(column > value)
        elif operator == "=lt=":
            query = query.where(column < value)
        elif operator == "=ge=":
            query = query.where(column >= value)
        elif operator == "=le=":
            query = query.where(column <= value)

    return query