def validate_form_data(data, form):
    try:
        form_data = form(data['formData'])
        if form_data.is_valid():
            return {'error': '', 'type': 'OK', 'status': 200}
        else:
            error = {}
            for field in form_data.errors:
                error[field] = [field_errors for field_errors in form_data.errors[field]]
            return {'error': error, 'type': 'ValidationError', 'status': 400}
    except:
        return {'error': 'Введите корректные данные.', 'type': 'BadRequest', 'status': 400}