import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

ET_POSTAL_CODE_RE = re.compile(r"^\d{4}$")


def validate_ethiopian_postal_code(value: str) -> None:
    value = (value or "").strip()

    if not ET_POSTAL_CODE_RE.fullmatch(value):
        raise ValidationError(
            _("Enter a valid Ethiopian postal code (exactly 4 digits)."),
            code="invalid_postal_code",
        )
