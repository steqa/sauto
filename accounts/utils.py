from .forms import UserCreationForm
from typing import NamedTuple, Literal


class Response(NamedTuple):
    body: dict
    type: Literal['OK'] | Literal['ValidationError'] | Literal['BadRequest']
    status: int


def validate_form_data(form_data: UserCreationForm) -> Response:
    try:
        if form_data.is_valid():
            return Response(body={}, type='OK', status=200)
        else:
            error = {}
            for field in form_data.errors:
                error[field] = [field_errors for field_errors in form_data.errors[field]]
            return Response(body=error, type='ValidationError', status=400)
    except:
        return Response(body={'error': 'Некорректные данные.'}, type='BadRequest', status=400)