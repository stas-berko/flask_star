"""Utilities for models to inherit or use"""
from flask import abort
from sqlalchemy.exc import SQLAlchemyError
import calendar


def get_object_or_404(model, mid):
    """Get an object by id or return a 404 not found response

    Args:
        model (object): object's model class
        mid (int): object's id

    Returns:
        object: returned from query

    Raises:
        404: if one object is returned from query

    """
    try:
        print(dir(model))
        return model.query.filter(model.id == mid).one()
    except SQLAlchemyError:
        abort(404)


def add_one_month(orig_date):
    new_year = orig_date.year
    new_month = orig_date.month + 1
    if new_month > 12:
        new_year += 1
        new_month -= 12

    last_day_of_month = calendar.monthrange(new_year, new_month)[1]
    new_day = min(orig_date.day, last_day_of_month)

    return orig_date.replace(year=new_year, month=new_month, day=new_day)
