# -*- coding: utf-8 -*-

from openerp import http, models, fields, api, exceptions, SUPERUSER_ID, _

class ModelA(models.Model):

    _name = "model.a"
    _description = "Model A"

    a1 = fields.Integer(string="A1")
    f1 = fields.Float(string="Float 1")

    def call(self):
        return "Model: {}".format(self._model)

class ModelB(models.Model):
    """
        Class Inheritance
            - Used to add features
            - New Class compatible with existing views
            - Stored in same tables
    """
    _inherit = "model.a"

    b1 = fields.Char(String="ModelB New feature")

class ModelC(models.Model):
    """
        Prototype Inheritance
            - Used to copy features
            - New Class Ignored by existing views
            - Stored in different tables
    """
    _name = "model.c"
    _inherit = "model.a"

    c1 = fields.Integer(
        string="C1"
    )

class ModelD(models.Model):
    """
        Delegation inheritance
            - Multiple inheritance is possible
            - New Class Ignored by existing views
            - Stored in different tables
            - 'new' instances contain embedded 'Model A' instance with synchronized values
    """

    _name = "model.d"
    _inherits = {'model.a': 'model_a_id'}

    d1 = fields.Integer(
        string="D1"
    )

class ModelE(ModelA):
    """
        Herança padrão do python
    """
    _name = "model.e"
    _description = "Model E"

    e1 = fields.Integer(
        string="E1"
    )
