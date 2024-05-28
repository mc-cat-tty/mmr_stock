from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def snake_to_capitalized(text: str) -> str:
  return ' '.join(
    map(
      lambda word: word.capitalize(),
      text.split('_')
    )
  )