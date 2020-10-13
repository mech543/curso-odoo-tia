from odoo import models, fields, api
from odoo.exceptions import UserError


class DetallePedido(models.Model):
    _name = 'modulo_pruebas.detalle_pedido'
    _description = 'Pedidos de recetas'
    _rec_name = "cantidad"

    cantidad = fields.Integer()
    receta = fields.Many2one('modulo_pruebas.receta')
    foto_receta = fields.Image(related="receta.imagen")
    pedido = fields.Many2one('modulo_pruebas.pedido')

    # Campos relacionados
    receta_precio = fields.Float(related='receta.precio')

    # Campos virtuales
    importe = fields.Float(compute='_calcula_precio')

    @api.depends('cantidad', 'receta')
    def _calcula_precio(self):
        for detalle in self:
            detalle.importe = detalle.receta_precio * detalle.cantidad

    @api.model
    def create(self, values):

        if values['cantidad'] < 1:
            raise UserError('Se requiere un valor minimo de 1 para la receta')

        if not values['receta']:
            raise UserError('Se requiere una receta')

        return super().create(values)