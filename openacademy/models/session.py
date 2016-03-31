# -*- coding: utf-8 -*-
# © <2016> <Luis Felipe Mileo>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import fields, models, api


class Session(models.Model):

    _name = "openacademy.session"
    _description = "Session"

    name = fields.Char(
        string=u"Name",
        required=True,
    )
    start_date = fields.Date(
        string=u"Data de inicio",
    )
    duration = fields.Integer(
        string=u"Duração (dias)"
    )
    seats = fields.Integer(
        string=u"Seats"
    )
    instructor_id = fields.Many2one(
        comodel_name="res.partner",
        domain="[('is_instructor', '=', 'True')]"
    )
    course_id = fields.Many2one(
        comodel_name="openacademy.course"
    )
    attendee_ids = fields.One2many(
        comodel_name='openacademy.attendee',
        inverse_name='session_id',
    )
    teacher_category = fields.Selection(
        selection=[
            ('level1', 'Level 1'),
            ('level2', 'Level 2'),
        ],
        string="Teacher Category",
    )
    teacher_domain = fields.Char(
        compute="_compute_teacher_domain"
    )
    available_seats = fields.Float(
        compute="_compute_available_seats"
    )

    @api.multi
    @api.depends('seats', 'attendee_ids')
    def _compute_available_seats(self):
        for record in self:
            if record.seats and record.seats > 0 and record.attendee_ids:
                record.available_seats = float(
                    len(record.attendee_ids.ids)) / float(record.seats) * 100

    @api.multi
    @api.depends('instructor_id')
    def _compute_teacher_domain(self):
        for record in self:
            result = []
            if record.instructor_id.category_id:
                for r in record.instructor_id.category_id:
                    if r.teacher_category:
                        result.append(r.teacher_category)
                record.teacher_domain = result
