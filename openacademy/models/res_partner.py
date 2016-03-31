# -*- coding: utf-8 -*-
# © <2016> <Luis Felipe Mileo>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import fields, models
from openerp.addons.openacademy.models.session import Session

class ResPartnerCategory(models.Model):

    _inherit = 'res.partner.category'

    teacher_category = fields.Selection(
        selection=Session.teacher_category.selection,
        string=Session.teacher_category.string,
    )


class ResPartner(models.Model):

    _inherit = 'res.partner'

    is_instructor = fields.Boolean(
        string="Instructor"
    )
    session_ids = fields.One2many(
        comodel_name="openacademy.session",
        inverse_name="instructor_id",
    )
    teacher_category = fields.Selection(
        selection=Session.teacher_category.selection,
        string=Session.teacher_category.string,
    )
