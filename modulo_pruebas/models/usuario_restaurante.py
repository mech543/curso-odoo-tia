# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class UsuarioRestaurante(models.Model):

    _inherit = 'res.users'

    tipo = fields.Many2one('modulo_pruebas.tipo_usuario')
    activo = fields.Boolean(default=True)