django-genshi-template
======================

**django-genshi-template** is a template backend that allows you to use Genshi with Django 1.8+

The following context variable are already pre-configured and usable:
    * 'static'     # staticfiles_storage.url
    * 'url'        # reverse
    * 'request'    # request
    * 'csrf_input' # csrf_input_lazy(request)
    * 'csrf_token' # csrf_token_lazy(request)


Usage/configuration
-------------------
In your settings.py, change the TEMPLATE section to the following::

    TEMPLATES = [
        {
            'BACKEND': 'django_genshi_template.backends.genshi.Genshi',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'auto_reload': False,
                'app_dirname': 'genshi',
                'serialization': 'html',
                'doctype': 'html',
            },
        },
    ]


Questions with answers
----------------------
* How do I add additional context variables or functions that are available to every template?

  Define a receiver function of the signal template_render and add context variables::

        from django.dispatch import receiver
        from django_template_backend_genshi import template_render

        @receiver(template_render)
        def add_render_globals(sender, **kwargs):
            genshi_context = kwargs['genshi_context']
            request = genshi_context['request']
            genshi_context['mynewvar'] = type(request)

