from odoo import models, fields, api, exceptions
from datetime import date


class Hospital(models.Model):
    _name = "hms.patient"
    _rec_name = "first_name"
    first_name = fields.Text(required=True)
    last_name = fields.Text(required=True)
    email = fields.Text(required=True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    pcr = fields.Boolean()
    image = fields.Image()
    blood_type = fields.Selection([
        ('A', 'A Types'),
        ('B', 'B Types'),
        ('C', 'C Types'),
        ('O', 'O Types'),
    ])
    state = fields.Selection([
        ('u', 'Undetermined'),
        ('g', 'Good'),
        ('f', 'Fair'),
        ('s', 'Serious'),
    ], default='u')


    age = fields.Integer(compute='calc_age', store=True)

    department_id = fields.Many2one(comodel_name='hms.department', string="Department")
    logs = fields.One2many(comodel_name='hms.logs', inverse_name='patient_id', string="Logs")

    doctors = fields.Many2many(comodel_name='hms.doctor')

    department_open = fields.Boolean(related='department_id.is_opened')

    def next_state(self):
        if self.state == 'u':
            self.state = 'g'
            self.changeState('Good')
        elif self.state == 'g':
            self.state = 'f'
            self.changeState('Fair')

        elif self.state == 'f':
            self.state = 's'
            self.changeState('Serious')

        elif self.state == 's':
            self.state = 'u'
            self.changeState('Undetermined')

    def changeState(self, state):
        self.env['hms.logs'].create({
            'details': "Patient State Changed To " + state,
            'patient_id': self.id
        })

    @api.model
    def create(self, val):
        new_pationts = super().create(val)
        return new_pationts

    @api.onchange('department_id')
    def onchange_department_id(self):
        if not self.department_open and self.first_name:
            raise exceptions.UserError("This Department is closed.")

    @api.onchange('age')
    def onchange_age(self):
        if self.first_name and self.age < 30:
            self.pcr = True
            return {
                'warning': {'title': 'take attention', 'message': 'The PCR option has been checked because age > 30.'}}


    @api.constrains("email")
    def check_email(self):
        if "@" not in self.email:
            raise exceptions.UserError("Invalid Email address.")
        return True


    _sql_constraints = [
        ('Duplicate_Email', 'UNIQUE(email)', 'email is already exists')]

    @api.depends("birth_date")
    def calc_age(self):
        for rec in self:
            if rec.birth_date :
                today = date.today()
                rec.age = today.year - rec.birth_date.year - (
                        (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day))
            else:
                rec.age=0