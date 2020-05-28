"""Streamfields live in here."""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class PersonBlock(blocks.StructBlock):
    """Title and text and nothing else."""

    first_name = blocks.CharBlock(required=True, help_text="Имя отчество")
    last_name = blocks.CharBlock(required=True, help_text="Фамилия")
    position = blocks.CharBlock(required=True, help_text="Ученое звание")
    degree = blocks.CharBlock(required=False, help_text="Ученая степень")
    bio = blocks.RichTextBlock(required=False, help_text="Био", features = ['bold', 'italic', 'link'])
    email = blocks.EmailBlock(required=True, help_text="email")
    photo = ImageChooserBlock(icon='user')

    class Meta:  # noqa
        template = "streams/person_block.html"
        icon = "user"
        label = "Данные преподавателя"


