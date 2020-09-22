from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from ...decorators import staff_required
from ...forms.languages import LanguageForm
from ...models import Language


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_required, name="dispatch")
class LanguageView(PermissionRequiredMixin, TemplateView):
    permission_required = "cms.manage_languages"
    raise_exception = True

    template_name = "languages/language_form.html"
    base_context = {"current_menu_item": "languages"}

    def get(self, request, *args, **kwargs):
        language_code = self.kwargs.get("language_code", None)
        language = Language.objects.filter(code=language_code).first()
        form = LanguageForm(instance=language)
        return render(request, self.template_name, {"form": form, **self.base_context})

    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        language_code = self.kwargs.get("language_code", None)
        language = Language.objects.filter(code=language_code).first()
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            if language_code:
                messages.success(request, _("Language was successfully saved"))
            else:
                messages.success(request, _("Language was successfully created"))
        else:
            # TODO: error handling
            # TODO: improve messages
            messages.error(request, _("An error has occurred."))

        return render(request, self.template_name, {"form": form, **self.base_context})
