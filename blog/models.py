from django.db import models
from django import forms

from wagtail.core.models import Page
#from wagtail.core.fields import StreamField

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from modelcluster.fields import ParentalManyToManyField

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.snippets.models import register_snippet
# blocks
from streams import blocks


class BlogCategory(models.Model):
    """Blog category snippet"""

    name = models.CharField(max_length = 20)
    slug = models.SlugField(
        verbose_name='slug',
        allow_unicode=False,
        max_length=20,
        help_text='Категории постов'
    )

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    class Meta:
        verbose_name = "Категория поста"
        verbose_name_plural = "Категории постов"

register_snippet(BlogCategory)

class PostListPage(Page):
    template = 'blog/post_list_page.html'
    subpage_types = ['blog.PostPage',]
    max_count = 1

    subtitle = models.CharField(max_length = 200, null = True, blank = True)
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]


    def get_context(self, request, *args, **kwargs):
        """Custom stuff to page"""
        context = super().get_context(request, *args, **kwargs)
        all_posts = PostPage.objects.live().public().order_by('-first_published_at')       

        page = request.GET.get("page")
        category = request.GET.get("category")

        paginator = Paginator(all_posts, 9)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts

        return context



class PostPage(Page):
    """Model for page with a post"""

    template = 'blog/post_page.html'
    subpage_types = []

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

    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        ]),
        
        ImageChooserPanel("image"),
        StreamFieldPanel("content"),
    ]
