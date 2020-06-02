from django.db import models
from django import forms

from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel

from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalManyToManyField

class EquipmentCarouselImages(Orderable):

    page = ParentalKey('equipment.EquipmentDetailPage', related_name='carousel_images')

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
    categories = ParentalManyToManyField("equipment.EquipmentCategory", blank=True)
    subpage_types = []
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
         MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        ]),
    ]

class EquipmentListPage(Page):
    """Class for all persons on kaf"""

    template = "equipment/equipment_list.html"
    subtitle = models.CharField(max_length = 300, blank = False, null = False, verbose_name='Коротко про оборудование')

    subpage_types = ['equipment.EquipmentDetailPage']
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        """Custom stuff to page"""
        context = super().get_context(request, *args, **kwargs)
        context['tools'] = EquipmentDetailPage.objects.live().public()

        return context
    

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
    ]


class EquipmentCategory(models.Model):
    """Equipment category snippet"""

    name = models.CharField(max_length = 20)
    slug = models.SlugField(
        verbose_name='slug',
        allow_unicode=False,
        max_length=20,
        help_text='Категории оборудования'
    )

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    class Meta:
        verbose_name = "Категория оборудования"
        verbose_name_plural = "Категории оборудования"

register_snippet(EquipmentCategory)
