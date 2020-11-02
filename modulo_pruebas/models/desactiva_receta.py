from odoo import models, fields, api
from odoo.exceptions import UserError


class DesactivaReceta(models.TransientModel):
    _name = 'modulo_pruebas.desactiva_receta'
    receta = fields.Many2one('modulo_pruebas.receta')
    justificacion = fields.Text()

    def desactiva(self):
        self.receta.write({'disponible': 0})
        return {'type': 'ir.actions.act_window_close'}
