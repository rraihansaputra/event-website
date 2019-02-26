import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_gt_today(date):
    if date < datetime.date.today():
        raise ValidationError(
            _('Your event finish date is in the past')
        )