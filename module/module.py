# -*- coding: utf-8 -*-

from openerp import http, models, fields, api, exceptions, SUPERUSER_ID, _

### Module
class Module(models.Model):
    _name = 'module.module'

    name = fields.Char(string="Title")
