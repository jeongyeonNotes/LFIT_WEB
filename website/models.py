from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail import blocks
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey

class SectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)

    class Meta:
        icon = "doc-full"
        label = "Section"

class HomePage(Page):
    tagline = models.CharField(max_length=120, blank=True)
    body = StreamField([("section", SectionBlock())], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("tagline"),
        FieldPanel("body"),
    ]

class StandardPage(Page):
    intro = RichTextField(blank=True)
    body = StreamField([("section", SectionBlock())], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

class ServiceIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("intro")]

class ServicePage(Page):
    short_desc = models.CharField(max_length=200, blank=True)
    body = StreamField(
        [("section", SectionBlock()),
         ("faq", blocks.ListBlock(blocks.StructBlock([
             ("q", blocks.CharBlock()),
             ("a", blocks.RichTextBlock()),
         ])))],
        use_json_field=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("short_desc"),
        FieldPanel("body"),
    ]

class ContactFormField(AbstractFormField):
    page = ParentalKey("ContactPage", on_delete=models.CASCADE, related_name="form_fields")

class ContactPage(AbstractEmailForm):
    subtitle = models.CharField(max_length=255, blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("thank_you_text"),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("to_address"),
        FieldPanel("from_address"),
        FieldPanel("subject"),
    ]
