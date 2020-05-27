# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Module(models.Model):
    _name = 'module.module'
    name = fields.Char(required=True)


class Model(models.Model):
    _name = 'model.model'
    name = fields.Char()
    menu_name = fields.Char(string="Menu Name", )

    module_name = fields.Many2one(comodel_name="module.module", string="Module Name", required=True, ondelete="cascade")
    fields = fields.One2many(comodel_name="field.field", inverse_name="model_name", string="Fields")


class Fields(models.Model):
    _name = 'field.field'
    name = fields.Char(required=True)
    string = fields.Char()
    type = fields.Selection(selection=[
        ('Char', 'Char'),
        ('Integer', 'Integer'),
        ('Float', 'Float'),
        ('Boolean', 'Boolean'),
        ('Date', 'Date'),
        ('Datetime', 'Datetime'),
        ('Html', 'Html'),
        ('Text', 'Text'),
        ('Binary', 'Binary'),

    ], required=True)
    model_name = fields.Many2one(comodel_name="model.model", string="Model Name", required=True, ondelete="cascade")
    required = fields.Boolean(string="Required?")
    readonly = fields.Boolean(string="Readonly?")

