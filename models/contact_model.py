from odoo import fields, models, api, _
from datetime import date


class ContactModel(models.Model):
    _name = "contact.model"
    _description = "contact model for boom lab"
    _rec_name = 'fullname'

    fullname = fields.Char(string='Fullname', size=200, required=True)
    firstname = fields.Char(string='Firstname', size=100, required=True)
    lastname = fields.Char(string='Lastname', size=200, required=True)
    birth_date = fields.Date(string='Birth date', required=True)
    bill_amount = fields.Float(string='Bill amount', required=True)
    gender = fields.Char(string='Gender', required=True)
    is_paid = fields.Boolean(string='Status paid', default=False)
    age = fields.Integer(string='Age', store=True, compute="_cal_age")
    description = fields.Char(string='Description', size=100)
    primary_phone_no = fields.Char(string='Primary phone no.', size=100)
    primary_phone_Type = fields.Selection([('home', 'Home'), ('office', 'Office'), ('mobile', 'Mobile')], required=True)
    contact_phone_id = fields.One2many('contact.phone.model', 'contact_id', string='Contact phone ID')

    @api.depends("birth_date")
    def _cal_age(self):
        today_date = date.today()
        for rec in self:
            if rec.birth_date:
                dob = fields.Datetime.to_datetime(rec.birth_date).date()
                total_age = int((today_date - dob).days / 365)
                rec.age = total_age

    @api.multi
    def _check(self):
        for rec in self:
            rec.primary_phone_no = '0123456789'


class ContactPhoneModel(models.Model):
    _name = "contact.phone.model"
    _description = "contact phone model for boom lab"
    _rec_name = 'phone_no'

    is_primary = fields.Boolean(string='Primary phone no.', default=True)
    phone_no = fields.Char(string='Phone no.', size=100, required=True)
    phone_type = fields.Selection([('home', 'Home'), ('office', 'Office'), ('mobile', 'Mobile')], required=True)
    contact_id = fields.Many2one('contact.model', string='Contact ID')

    # @api.model_create_multi
    # def xxx_xx(self, values):
    #     print("********************** self: ", self)
    #     print("00000000000000000 VALUE: ", values)
    #     x = self.env['contact.model'].browse([4])
    #     print("1111111111111111111 X: ", x)
    #     x.write({'primary_phone_no': '01111111111'})
    #     rtn = super(ContactPhoneModel, self).write(values)
    #     return rtn
