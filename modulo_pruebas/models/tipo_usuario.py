# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class TipoUsuario(models.Model):

    _name = 'modulo_pruebas.tipo_usuario'
    _rec_name = 'nombre'

    nombre = fields.Char()
    clave = fields.Char()
