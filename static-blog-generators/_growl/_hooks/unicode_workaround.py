"""
Workarounds for growl to work with unicode
"""

#
# Overwrite default renderTemplate.
#
def renderTemplate(template, context):
    if isinstance(template, str):
        template = unicode(template, 'utf-8')
    return jinja2_env.from_string(template).render(context)

@wrap(Template.transform)
def unicodeAwareTransform(forig, self):
    transformed = forig(self)
    if isinstance(transformed, str):
        transformed = unicode(transformed, 'utf-8')
    return transformed

