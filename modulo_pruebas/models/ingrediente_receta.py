from odoo import models, fields


class IngredienteReceta(models.Model):
    _name = 'modulo_pruebas.ingrediente_receta'

    receta = fields.Many2one('modulo_pruebas.receta')
    cantidad = fields.Integer()
    ingrediente = fields.Many2one('modulo_pruebas.ingrediente')