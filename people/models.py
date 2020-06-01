from django.db import models

from wagtail.core.models import Page
#from wagtail.core.fields import StreamField

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
# blocks
from streams import blocks



class PersonDetailPage(Page):
    """Class for every person on kaf"""

    subpage_types = []

    template = "people/person.html"    
    degree = models.CharField(max_length = 50, blank = True, null = True, help_text='Степень')
    education = models.CharField(max_length = 200, blank = True, null = True, help_text='Образование')
    position = models.CharField(max_length = 50, blank = True, null = True, help_text='Позиция')
    email = models.EmailField(blank = True, null = True)
    bio = RichTextField(blank = True, 
        null = True, 
        features=['h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul','embed', 'hr', 'superscript', 'subscript', 'strikethrough'],
        help_text='Общая информация'
        )
    photo = models.ForeignKey(
        "wagtailimages.Image",
        blank=True, 
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )    

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [    
                ImageChooserPanel('photo'),
                FieldPanel('email'),            
                FieldPanel('degree'),
                FieldPanel('education'),
                FieldPanel('position'),
                FieldPanel('bio'),
            ],
        )     
    ]

class PersonListPage(Page):
    """Class for all persons on kaf"""

    template = "people/person_list.html"
    subtitle = models.CharField(max_length = 300, blank = False, null = False, verbose_name='Наш девиз')

    subpage_types = ['people.PersonDetailPage']
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        """Custom stuff to page"""
        context = super().get_context(request, *args, **kwargs)
        context['people'] = PersonDetailPage.objects.order_by('title').live().public()

        return context   

    content_panels = Page.content_panels + [        
        FieldPanel('subtitle'),
    ]