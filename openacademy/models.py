# -*- coding: utf-8 -*-

from datetime import timedelta
from openerp import models, fields, api, exceptions, _


class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null', string="Responsible",
                                     index=True)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    @api.constrains('name', 'description')
    def _check_close_date_validity(self):
        for r in self:
            if r.name == r.description:
                raise exceptions.ValidationError(
                    _("The description cannot be the name!"))

    _sql_constraints = [
        ('name_unique_check',
         'UNIQUE(name)',
         "Duplicated name! The course name must be unique."),
    ]


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    end_date = fields.Date(string="End Date", store=True,
                           compute='_compute_end_date')
    duration = fields.Float(help="Duration in days")
    duration_hours = fields.Float(string="Duration in hours",
                         compute='_compute_duration_hours')
    seats = fields.Integer(string="Number of seats")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    active = fields.Boolean(default=True)

    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=['|', ('is_instructor', '=', True),
                                            ('category_id.name', 'ilike',
                                             "Teacher")])
    course_id = fields.Many2one('openacademy.course',
                                ondelete='cascade', string="Course",
                                required=True)
    attendee_ids = fields.One2many(
        'openacademy.attendee', 'session_id', string="Attendees")
    attendees = fields.Integer(
        string="Number of Attendees", compute='_compute_attendees', store=True)
    color = fields.Integer()
    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'
        self.active = 0

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for r in self:
            if (r.start_date and r.duration):
                start = fields.Datetime.from_string(r.start_date)
                duration = timedelta(days=r.duration, seconds=-1)
                r.end_date = start + duration

    @api.depends('duration')
    def _compute_duration_hours(self):
        for r in self:
            if r.duration:
                r.duration_hours = r.duration * 24

    @api.depends('attendee_ids')
    def _compute_attendees(self):
        for r in self:
            r.attendees = len(r.attendee_ids)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Seats less than zero",
                    'message': "You can't have less than zero seats",
                },
            }


class Attendee(models.Model):
    _name = 'openacademy.attendee'

    name = fields.Char(required=False)

    partner_id = fields.Many2one('res.partner', string="Partner")
    session_id = fields.Many2one('openacademy.session',
                                 ondelete='cascade', string="Session")


class Partner(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean("Instructor", default=False)
