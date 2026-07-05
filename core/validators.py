from __future__ import annotations

from core.exceptions import ValidationError


def validate_positive(value: float, field: str) -> None:

    if value <= 0:

        raise ValidationError(

            f"{field} must be greater than zero."

        )


def validate_non_negative(value: float, field: str) -> None:

    if value < 0:

        raise ValidationError(

            f"{field} cannot be negative."

        )


def validate_not_empty(value: str, field: str) -> None:

    if value is None or str(value).strip() == "":

        raise ValidationError(

            f"{field} cannot be empty."

        )


def validate_percentage(value: float, field: str) -> None:

    if value < 0 or value > 100:

        raise ValidationError(

            f"{field} must be between 0 and 100."

        )


def validate_units(units: float) -> None:

    validate_positive(

        units,

        "Units"

    )


def validate_amount(amount: float) -> None:

    validate_positive(

        amount,

        "Amount"

    )


def validate_nav(nav: float) -> None:

    validate_positive(

        nav,

        "NAV"

    )