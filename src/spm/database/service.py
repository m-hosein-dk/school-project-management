from typing import TypeVar
from sqlalchemy.orm import Session
from fastapi import Query, Depends
from .core import (
    Base,
    SearchPaginationParameters,
    apply_fiql_filters
)
from .model import (
    SearchPaginationOutput
)

T = TypeVar("T", bound=Base)

def search_pagination(
    model:type[T],
    params:SearchPaginationParameters,
    session: Session
) -> tuple[SearchPaginationOutput, list[T]]:
    query = session.query(model)

    # applying FIQL filters
    query = apply_fiql_filters(query, model, params.q)
    total = query.count()

    # applying sorting
    sort_column = getattr(model, params.sortby, None)
    if sort_column is not None:
        if params.order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

    # applying pagination
    query = query.limit(params.page_size).offset((params.page - 1) * params.page_size)
    
    items = query.all()

    total_pages = (total + params.page_size - 1) // params.page_size
    return SearchPaginationOutput(
        total_count=total,
        total_pages=total_pages,
        current_page=params.page,
        page_size=params.page_size,
    ), items