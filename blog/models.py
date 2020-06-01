from django.db import models

from wagtail.core.models import Page
#from wagtail.core.fields import StreamField

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
# blocks
from streams import blocks


class PostListPage(Page):
    template = 'blog/post_list_page.html'

    subpage_types = ['blog.PostPage',]

    subtitle = models.CharField(max_length = 200, null = True, blank = True)
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]


    def get_context(self, request, *args, **kwargs):
        """Custom stuff to page"""
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = PostPage.objects.live().public().order_by('created_at')

        return context



class PostPage(Page):
    """Model for page with a post"""

    template = 'blog/post_page.html'
    date = models.DateTimeField("Дата публикации", auto_now=True)

    subtitle = models.CharField(max_length = 200, null = True, blank = True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    content = StreamField(
        [
            ("description", blocks.SimpleRichtextBlock()),
            ("ctablock", blocks.CTABlock()),
            ("cardblock", blocks.CardBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),

        ImageChooserPanel("image"),
        StreamFieldPanel("content"),
    ]
