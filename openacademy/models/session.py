# -*- coding: utf-8 -*-
# © <2016> <Luis Felipe Mileo>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import fields, models, api
from openerp.exceptions import Warning as UserError
import dateutil.relativedelta


class Session(models.Model):

    _name = "openacademy.session"
    _description = "Session"

    name = fields.Char(
        string=u"Name",
        required=True,
    )
    start_date = fields.Date(
        string=u"Data de inicio",
        default=fields.Date.today(),
        copy=False,
    )
    stop_date = fields.Date(
        string=u"Stop Date",
        compute='_compute_stop_date',
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
        related='instructor_id.teacher_category',
        readonly=True,
    )
    teacher_domain = fields.Char(
        compute="_compute_teacher_domain"
    )
    taken_seats = fields.Float(
        compute="_compute_taken_seats",
        store=True,
    )

    @api.multi
    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for record in self:
            if record.seats < 0:
                raise UserError("Computed seats < 0")
            if record.seats and record.attendee_ids:
                record.taken_seats = float(
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

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique per company!'),
    ]

    @api.constrains('name')
    def _check_seats(self):
        if self.seats < 0:
            raise UserError('Total de vagas deve ser maior que zero!')

    @api.one
    def copy(self, default=None):
        default['name'] = self.name + " (copy)"
        return super(Session, self).copy(default)

    @api.multi
    @api.depends('start_date', 'duration')
    def _compute_stop_date(self):
        for record in self:
            if record.start_date and record.duration:
                record.stop_date = (
                    fields.Date.from_string(record.start_date) +
                    dateutil.relativedelta.relativedelta(
                        days=record.duration)
                )
