# -*- coding: utf-8 -*-
# © 2015 Luis Felipe Mileo
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import fields


class TestOpenAcademy(common.TransactionCase):
    def setUp(self):
        super(TestOpenAcademy, self).setUp()
        self.res_partner_model = self.env['res.partner']
        responsible = self.res_partner_model.create({
            'name': 'Test Responsible',
            'customer': True,
            'supplier': True,
            'lang': 'en_US',
        })
        instructor = self.res_partner_model.create({
            'name': 'Test Instructor',
            'start_date': True,
            'supplier': True,
            'lang': 'en_US',
        })
        self.course_model = self.env['openacademy.course']
        course = self.course_model.create({
            'name': 'CCO',
            'description': 'Ciencias da computacao',
            'responsible_id': responsible.id,
        })
        self.session_model = self.env['openacademy.session']
        self.session_model.create({
            'name': '2016/1',
            'description': 'Ciencias da computacao',
            'start_date': fields.Date.today(),
            'duration': 60,
            'instructor_id': instructor.id,
            'course_id': course.id,
            'attendee_ids': [(0, 0, {
                'partner_id': self.ref(
                    'sale_commission.res_partner_pritesh_sale_agent'),
            })]
        })
