"""
    Side by side view
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from ...constants import status
from ...decorators import region_permission_required
from ...forms.pages import PageTranslationForm
from ...models import Page, Region, Language


@method_decorator(login_required, name="dispatch")
@method_decorator(region_permission_required, name="dispatch")
class PageSideBySideView(PermissionRequiredMixin, TemplateView):
    permission_required = "cms.view_pages"
    raise_exception = True

    template_name = "pages/page_sbs.html"
    base_context = {"current_menu_item": "pages"}

    def get(self, request, *args, **kwargs):

        region = Region.objects.get(slug=kwargs.get("region_slug"))
        page = Page.objects.get(pk=kwargs.get("page_id"))

        target_language = Language.objects.get(code=kwargs.get("language_code"))
        source_language_node = region.language_tree_nodes.get(
            language=target_language
        ).parent

        if source_language_node:
            source_language = source_language_node.language
        else:
            messages.error(
                request,
                _(
                    "You cannot use the side-by-side-view for the region's default language (in this case {default_language})."
                ).format(default_language=target_language.translated_name),
            )
            return redirect(
                "edit_page",
                **{
                    "page_id": page.id,
                    "region_slug": region.slug,
                    "language_code": target_language.code,
                }
            )

        source_page_translation = page.get_translation(source_language.code)
        target_page_translation = page.get_translation(target_language.code)

        if not source_page_translation:
            messages.error(
                request,
                _(
                    "You cannot use the side-by-side-view if the source translation (in this case {source_language}) does not exist."
                ).format(source_language=source_language.translated_name),
            )
            return redirect(
                "edit_page",
                **{
                    "page_id": page.id,
                    "region_slug": region.slug,
                    "language_code": target_language.code,
                }
            )

        page_translation_form = PageTranslationForm(
            instance=target_page_translation,
        )

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
                "page_translation_form": page_translation_form,
                "source_page_translation": source_page_translation,
                "target_language": target_language,
            },
        )

    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):

        if not request.user.has_perm("cms.edit_pages"):
            raise PermissionDenied

        region = Region.objects.get(slug=kwargs.get("region_slug"))
        page = Page.objects.get(pk=kwargs.get("page_id"))

        target_language = Language.objects.get(code=kwargs.get("language_code"))
        source_language_node = region.language_tree_nodes.get(
            language=target_language
        ).parent

        if source_language_node:
            source_page_translation = page.get_translation(
                source_language_node.language.code
            )
        else:
            messages.error(
                request,
                _(
                    "You cannot use the side-by-side-view for the region's default language (in this case {default_language})."
                ).format(default_language=target_language.translated_name),
            )
            return redirect(
                "edit_page",
                **{
                    "page_id": page.id,
                    "region_slug": region.slug,
                    "language_code": target_language.code,
                }
            )

        page_translation_instance = page.get_translation(target_language.code)

        if not source_page_translation:
            messages.error(
                request,
                _(
                    "You cannot use the side-by-side-view if the source translation (in this case {source_language}) does not exist."
                ).format(source_language=source_language_node.language.translated_name),
            )
            return redirect(
                "edit_page",
                **{
                    "page_id": page.id,
                    "region_slug": region.slug,
                    "language_code": target_language.code,
                }
            )

        page_translation_form = PageTranslationForm(
            request.POST,
            instance=page_translation_instance,
            region=region,
            language=target_language,
        )

        if not page_translation_form.is_valid():
            messages.error(request, _("Errors have occurred."))
        elif not page_translation_form.has_changed():
            messages.info(request, _("No changes detected."))
        else:
            page_translation = page_translation_form.save(page=page, user=request.user)
            published = page_translation.status == status.PUBLIC
            if not page_translation_instance:
                if published:
                    messages.success(
                        request,
                        _("Translation was successfully created and published"),
                    )
                else:
                    messages.success(
                        request, _("Translation was successfully created")
                    )
            else:
                if published:
                    messages.success(
                        request, _("Translation was successfully published")
                    )
                else:
                    messages.success(request, _("Translation was successfully saved"))

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
                "page_translation_form": page_translation_form,
                "source_page_translation": source_page_translation,
                "target_language": target_language,
            },
        )
