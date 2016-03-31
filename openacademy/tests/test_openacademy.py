from openerp.tests.common import TransactionCase
from openerp import fields


class Tests(TransactionCase):
    def setUp(self):

        super(Tests, self).setUp()
        self.responsible_1_id = self.ref(
            'base.user_demo')
        self.instructor_1_id = self.ref(
            'base.res_partner_address_34')

    def test_01_create_course(self):
        self.course_model = self.env['openacademy.course']
        self.course_01_id = self.course_model.create({
            'name': 'Administracao',
            'description': "Principios de pessoal",
            'responsible_id': self.responsible_1_id
        })
        self.assertEquals(self.course_01_id.responsible_id.id,
                          self.responsible_1_id)

    def test_02_create_session(self):
        self.session_model = self.env['openacademy.session']
        self.test_01_create_course()
        self.session_01_id = self.session_model.create({
            'name': u'Sessao 01',
            'start_date': fields.Date.today(),
            'duration': 30,
            'seats': 100,
            'active': True,
            'instructor_id': self.instructor_1_id,
            'course_id': self.course_01_id.id,
        })
        self.assertEquals(self.session_01_id.instructor_id.id,
                          self.instructor_1_id)
        self.assertEquals(self.session_01_id.course_id.id,
                          self.course_01_id.id)
        self.assertIn(
            self.session_01_id.id,
            self.course_01_id.session_ids.ids
        )

    def test_03_create_attendee(self):
        self.attendee_model = self.env['openacademy.attendee']
        self.test_02_create_session()
        self.attendee_01_id = self.attendee_model.create({
            'name': 'Attendee 01',
            'partner_id': self.instructor_1_id,
            'session_id': self.session_01_id.id,
        })
        self.assertEquals(self.attendee_01_id.partner_id.id,
                          self.instructor_1_id)
        self.assertEquals(self.attendee_01_id.session_id.id,
                          self.session_01_id.id)
        self.assertIn(
            self.attendee_01_id.id,
            self.session_01_id.attendee_ids.ids
        )

