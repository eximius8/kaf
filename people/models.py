from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
# blocks
from streams import blocks



class Person(Page):
    """Class for every person on kaf"""

    template = "people/person.html" 

    body = StreamField([       
        ('person', blocks.PersonBlock()),        
    ])

    content_panels = Page.content_panels + [        
        StreamFieldPanel('body'),
    ]

