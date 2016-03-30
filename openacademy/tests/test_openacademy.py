# -*- coding: utf-8 -*-
# © 2015 Luis Felipe Mileo
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests.common import TransactionCase
from openerp import fields


class Tests(TransactionCase):
    def setUp(self):

        super(Tests, self).setUp()
        self.responsible_1_id = self.ref(
            'base.res_partner_address_35')
        self.instructor_1_id = self.ref(
            'base.res_partner_address_34')

    def test_01_create_attendee(self):
        self.attendee_model = self.env['openacademy.attendee']
        self.attendee_01_id = self.attendee_model.create({
            'name': 'Attendee 01',
            'partner_id': self.responsible_1_id,
        })
    #
    # def test_02_create_session(self):
    #
    #     self.session_model = self.env['openacademy.session']
    #     self.session_model.create({
    #         'name': '2016/1',
    #         'description': 'Ciencias da computacao',
    #         'start_date': fields.Date.today(),
    #         'duration': 60,
    #         'instructor_id': self.instructor_1_id,
    #         'course_id': self.course_01_id.id,
    #         'attendee_ids': [(0, 0, {
    #             'partner_id': self.ref(
    #                 'sale_commission.res_partner_pritesh_sale_agent'),
    #         })]
    #     })
