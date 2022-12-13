from typing import NamedTuple, Literal
from accounts.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from seller.forms import SellerCreationForm
from announcement.forms import AnnouncementCreationForm


class Response(NamedTuple):
    body: dict
    type: Literal['OK'] | \
          Literal['redirect'] | \
          Literal['ValidationError'] | \
          Literal['ImageValidationError'] | \
          Literal['BadRequest'] | \
          Literal['EmailSendingError'] | \
          Literal['AuthenticationError'] | \
          Literal['NotFound']
    status: Literal[200] | Literal[400]


def validate_form_data(form_data:
                       UserCreationForm |
                       AuthenticationForm |
                       PasswordResetForm |
                       SetPasswordForm |
                       AnnouncementCreationForm |
                       SellerCreationForm) -> Response:
    try:
        if form_data.is_valid():
            return Response(body={}, type='OK', status=200)
        else:
            error = {}
            for field in form_data.errors:
                error[field] = [field_errors for field_errors in form_data.errors[field]]
            return Response(body=error, type='ValidationError', status=400)
    except:
        return Response(
            body={'error': 'Некорректные данные.'},
            type='BadRequest', status=400)