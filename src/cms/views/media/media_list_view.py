"""
The module is working as the view component for the dynamic data loading for the media library.
Therefore, it's managing the region permissions and connects the different data structures.
Especially, the root file, the use of the file defined in the Document and the different meta data.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ...decorators import region_permission_required
from ...models import Document, Region
from ...models.media.directory import Directory


@method_decorator(login_required, name="dispatch")
@method_decorator(region_permission_required, name="dispatch")
class MediaListView(TemplateView):
    """
    Class representing the media management and renders the dynamic data into the HTML template.
    """

    template_name = "media/media_list.html"
    base_context = {"current_menu_item": "media"}

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("region_slug")
        region = Region.objects.get(slug=slug)
        directory_id = int(kwargs.get("directory_id"))
        breadcrumb = []

        if directory_id != 0:
            directory = Directory.objects.get(id=directory_id)
        else:
            directory = None
        documents = Document.objects.filter(region=region, path=directory)
        directories = Directory.objects.filter(region=region, parent=directory)

        current_breadcrumb = directory
        try:
            while current_breadcrumb:
                breadcrumb.append(current_breadcrumb)
                current_breadcrumb = current_breadcrumb.parent
        except Directory.DoesNotExist:
            pass

        breadcrumb.reverse()

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
                "documents": documents,
                "directory": directories,
                "directory_id": directory_id,
                "breadcrumb": breadcrumb,
            },
        )
