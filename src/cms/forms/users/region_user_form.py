import logging

from django.contrib.auth import get_user_model

from .user_form import UserForm


logger = logging.getLogger(__name__)


class RegionUserForm(UserForm):
    """
    Form for creating and modifying region user objects
    """

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email", "is_active"]

    def __init__(self, data=None, instance=None):

        logger.info(
            "RegionUserForm instantiated with data %s and instance %s", data, instance
        )

        # Instantiate ModelForm
        super().__init__(data=data, instance=instance)

    def save(self, *args, **kwargs):

        logger.info(
            "RegionUserForm saved with cleaned data %s and changed data %s",
            self.cleaned_data,
            self.changed_data,
        )

        # save ModelForm
        return super().save(*args, **kwargs)
