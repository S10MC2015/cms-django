from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ...decorators import region_permission_required
from ...models import Document
from ...models.media.directory import Directory
from ...utils.media_utils import get_thumb


@method_decorator(login_required, name="dispatch")
@method_decorator(region_permission_required, name="dispatch")
class MediaListView(TemplateView):
    template_name = "media/media_list.html"
    base_context = {"current_menu_item": "media"}

    def get(self, request, *args, **kwargs):
        documents = Document.objects.all()
        results = {}
        for doc in documents:
            thumbnail = get_thumb(doc, 300, 300, True)
            results[doc.id] = thumbnail
        directories = Directory.objects.all()

        return render(
            request,
            self.template_name,
            {
                **self.base_context,
                "documents": documents,
                "thumbnails": results,
                "directory": directories,
            },
        )
