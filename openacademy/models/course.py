
from openerp import models, fields, api


class Course(models.Model):

    _name = "course.course"
    _description = "Course"

    name = fields.Char(
        string="Name"
    )
    description = fields.Text(
        string="Descricao"
    )

