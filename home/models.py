from django.db import models

from wagtail.core.models import Page

from wagtail.admin.edit_handlers import FieldPanel




from blog.models import PostPage
from blog.models import BlogCategory


class HomePage(Page):
    subpage_types = ['equipment.EquipmentListPage', 'people.PersonListPage', 'blog.PostListPage']

    max_count = 1

    subtitle = models.CharField(max_length = 200, null = True, blank = True)
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]


    def get_context(self, request, *args, **kwargs):
        """Custom stuff to page"""
        context = super().get_context(request, *args, **kwargs)

        context['posts'] = PostPage.objects.live().public().order_by('-first_published_at')[:9]
        context["categories"] = BlogCategory.objects.all()

        return context

