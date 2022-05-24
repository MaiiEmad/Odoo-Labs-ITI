from odoo import api, models, fields
from odoo.exceptions import UserError


class CrmCustomersInherit(models.Model):
    _inherit = 'res.partner'

    salary = fields.Float()

    vat = fields.Char(compute="calc_tax")

    related_patient_id = fields.Many2one("hms.patient")

    @api.depends('salary')
    def calc_tax(self):
        for record in self:
            record.vat = record.salary * 0.2

    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise UserError("Can't delete customer,this customer have patient")
        super().unlink()

    @api.constrains("related_patient_id")
    def check_email(self):
        for record in self:
            if record.email != record.related_patient_id.email:
                customers = self.env["hms.patient"].search([('email', '=', record.email)])
                if len(customers) == 1:
                    raise UserError('u can`t choose this patient')
                