# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class Ingrediente(models.Model):
    _name = 'modulo_pruebas.ingrediente'
    _description = "Ingredientes"
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre")
