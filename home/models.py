from django.db import models

from wagtail.core.models import Page, Orderable

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField


from modelcluster.fields import ParentalKey

from blog.models import PostPage


class HomePage(Page):
    subpage_types = ['home.EquipmentListPage', 'people.PersonListPage', 'blog.PostListPage', 'blog.PostPage']

    max_count = 1

    subtitle = models.CharField(max_length = 200, null = True, blank = True)
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]


    def get_context(self, request, *args, **kwargs):
        """Custom stuff to page"""
        context = super().get_context(request, *args, **kwargs)
        all_posts = PostPage.objects.live().public().order_by('-first_published_at')

        paginator = Paginator(all_posts, 9)

        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts

        return context


class EquipmentCarouselImages(Orderable):

    page = ParentalKey('home.EquipmentDetailPage', related_name='carousel_images')

    carousel_image = models.ForeignKey(
        'wagtailimages.Image',
        null = True,
        blank = False,
        on_delete = models.SET_NULL,
        related_name='+',
        verbose_name='Фото',
    )

    panels = [
        ImageChooserPanel('carousel_image')
    ]



class EquipmentDetailPage(Page):
    """Class for every person on kaf"""

    template = "equipment/tool.html"
    description = RichTextField(
        blank = False,
        null = True,
        verbose_name='Описание',
        features=['h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'embed', 'hr', 'superscript', 'subscript', 'strikethrough'],
        help_text='Общая информация'
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        MultiFieldPanel([
                InlinePanel('carousel_images', max_num=4, min_num=1, label="Image")
            ], heading="Фото оборудования"),
    ]

class EquipmentListPage(Page):
    """Class for all persons on kaf"""

    template = "equipment/equipment_list.html"
    subtitle = models.CharField(max_length = 300, blank = False, null = False, verbose_name='Коротко про оборудование')

    subpage_types = ['home.EquipmentDetailPage']

    def get_context(self, request, *args, **kwargs):
        """Custom stuff to page"""
        context = super().get_context(request, *args, **kwargs)
        context['tools'] = EquipmentDetailPage.objects.live().public()

        return context

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
    ]
