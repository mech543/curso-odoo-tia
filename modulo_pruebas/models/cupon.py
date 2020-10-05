# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class Cupon(models.Model):
    _name = 'modulo_pruebas.cupon'
    _rec_name = 'nombre'

    nombre = fields.Char()
    descuento = fields.Integer()
    cliente = fields.Many2one('res.users')
