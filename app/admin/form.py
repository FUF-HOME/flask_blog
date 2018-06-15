#!/usr/bin/env python
# -*-coding:utf-8-*-


from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


    # class MessageAdmin(ModelView):
    #     extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    #
    #     form_overrides = {
    #         'body': CKTextAreaField
    #     }
