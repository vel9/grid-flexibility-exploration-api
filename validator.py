class ValidatorResult:

    def __init__(self, has_errors: bool, errors: dict):
        """
        Object representing validation result

        :param has_errors: if validation potentially failed
        :param errors: dictionary detailing errors
        """
        self.has_errors = has_errors
        self.errors = errors


def validate_add_resource(name: str, hour: str):
    """
    Validate name and hour values for resource

    :param name: resource name
    :param hour: number of hours for resource
    :return: validator result
    """
    errors = {}
    if not name:
        errors['name'] = "Name must not be empty"

    if not hour:
        errors['hours'] = "Hour must not be empty"
    elif not hour.isdigit():
        errors['hours'] = "Hour must be an integer"
    elif int(hour) < 1 or int(hour) > 23:
        errors['hours'] = "Hour must be between 1 and 23"

    return ValidatorResult(bool(errors), errors)
