from django import template
register = template.Library()
@register.filter(name='json')
def _json(obj):
  #remember to make sure the contents are actually safe before you use this filter!
  return (json.dumps(obj)) 