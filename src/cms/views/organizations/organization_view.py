from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from ...decorators import staff_required
from ...forms.organizations import OrganizationForm
from ...models import Organization


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_required, name="dispatch")
class OrganizationView(PermissionRequiredMixin, TemplateView):
    permission_required = "cms.manage_organizations"
    raise_exception = True

    template_name = "organizations/organization_form.html"
    base_context = {"current_menu_item": "organizations"}

    def get(self, request, *args, **kwargs):
        organization_id = self.kwargs.get("organization_id", None)
        if organization_id:
            organization = Organization.objects.get(id=organization_id)
            form = OrganizationForm(instance=organization)
        else:
            form = OrganizationForm()
        return render(request, self.template_name, {"form": form, **self.base_context})

    def post(self, request, organization_id=None):
        # TODO: error handling
        if organization_id:
            organization = Organization.objects.get(id=organization_id)
            form = OrganizationForm(request.POST, instance=organization)
            success_message = _("Organization was successfully created")
        else:
            form = OrganizationForm(request.POST)
            success_message = _("Organization was successfully saved")

        if form.is_valid():
            form.save()
            messages.success(request, success_message)
            # TODO: improve messages
        else:
            messages.error(request, _("Errors have occurred."))

        return render(request, self.template_name, {"form": form, **self.base_context})
