# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class Cocina(models.Model):
    _name = 'modulo_pruebas.cocina'
    _description = 'Tipo de cocina'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre")
    descripcion = fields.Text(string="Descripción")
    recetas = fields.One2many('modulo_pruebas.receta', 'cocina')