from __future__ import absolute_import

import sys

from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
from django.utils import six

from genshi.template import TemplateLoader
from genshi.template.base import TemplateSyntaxError \
    as GenshiTemplateSyntaxError
from genshi.template.loader import TemplateNotFound
from genshi.template.markup import MarkupTemplate


class Genshi(BaseEngine):

    app_dirname = 'genshi'

    def __init__(self, params):
        params = params.copy()
        options = params.pop('OPTIONS').copy()
        self.app_dirname = options.get('app_dirname', self.app_dirname)
        super(Genshi, self).__init__(params)
        self.loader = TemplateLoader(self.template_dirs)

    def from_string(self, template_code):
        return Template(MarkupTemplate(template_code))

    def get_template(self, template_name):
        try:
            return Template(self.loader.load(template_name))
        except TemplateNotFound as exc:
            six.reraise(TemplateDoesNotExist, TemplateDoesNotExist(exc.args),
                        sys.exc_info()[2])
        except GenshiTemplateSyntaxError as exc:
            six.reraise(TemplateSyntaxError, TemplateSyntaxError(exc.args),
                        sys.exc_info()[2])


class Template(object):

    def __init__(self, template):
        self.template = template

    def render(self, context=None, request=None):
        if context is None:
            context = {}

        if request is not None:
            context['request'] = request
            context['csrf_input'] = csrf_input_lazy(request)
            context['csrf_token'] = csrf_token_lazy(request)
        return self.template.generate(**context).render('html', doctype='html')
