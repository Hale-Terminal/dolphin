import json
import logging

from typing import List
from pydantic import BaseModel

from fastapi import Depends, Query

from sqlalchemy import and_, not_, or_, orm, func, desc
from sqlalchemy.exc import InvalidRequestError, ProgrammingError
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy_filters import apply_pagination, apply_sort
from sqlalchemy_filters.exceptions import BadFilterFormat, FieldNotFound
from sqlalchemy_filters.models import Field, get_model_from_spec

from .core import (
    Base,
    get_db,
    get_class_by_tablename
)


def search(*, query_str: str, query: Query, model: str, sort=False):
    search_model = get_class_by_tablename(model)

    if not query_str.strip():
        return query

    vector = search_model.search_vector




def search_filter_sort_paginate(
    db_session,
    model,
    query_str: str = None,
    filter_spec: List[dict] = None,
    page: int = 1,
    items_per_page: int = 5,
    sort_by: List[str] = None,
    descending: List[bool] = None
):
    model_cls = get_class_by_tablename(model)
    try:
        query = db_session.query(model_cls)


    except Exception as e:
        raise e

    if items_per_page == -1:
        items_per_page = None

    query, pagination = apply_pagination(query, page_number=page, page_size=items_per_page)

    return {
        "items": query.all(),
        "itemsPerPage": pagination.page_size,
        "page": pagination.page_number,
        "total": pagination.total_results
    }
