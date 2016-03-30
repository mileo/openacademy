# -*- coding: utf-8 -*-

from openerp import models, fields


class Course(models.Model):
    """
       
    """
    _name = 'openacademy.course'
    _description = "Course"    

    name = fields.Char(
        string="Title",
        required=True
    )
    description = fields.Text()
