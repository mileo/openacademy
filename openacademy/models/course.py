# -*- coding: utf-8 -*-

from openerp import models, fields


class Course(models.Model):
    """

    """
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one(
        'res.users',
        ondelete='set null', string="Responsible",
        index=True
    )
    session_ids = fields.One2many(
        'openacademy.session',
        'course_id',
        string="Sessions"
    )


class Session(models.Model):
    """

    """
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(help="Duration in days")
    seats = fields.Integer(string="Number of seats")

    instructor_id = fields.Many2one('res.partner', string="Instructor")
    course_id = fields.Many2one(
        'openacademy.course',
        ondelete='cascade',
        string="Course",
        required=True)
    attendee_ids = fields.One2many(
        'openacademy.attendee',
        'session_id',
        string="Attendees")


class Attendee(models.Model):
    """

    """
    _name = 'openacademy.attendee'

    name = fields.Char(required=False)

    partner_id = fields.Many2one(
        'res.partner',
        string="Partner")
    session_id = fields.Many2one(
        'openacademy.session',
        ondelete='cascade',
        string="Session")
