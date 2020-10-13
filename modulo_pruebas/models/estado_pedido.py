# -*- coding: utf-8 -*-

from odoo import models, fields


class EstadoPedido(models.Model):
    _name = 'modulo_pruebas.estado_pedido'
    _description = 'Pedidos de recetas'
    _rec_name = 'nombre'

    orden = fields.Char()
    nombre = fields.Char()
