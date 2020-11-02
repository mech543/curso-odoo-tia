from odoo import models, fields, api
from odoo.exceptions import UserError


class ListaIngredientes(models.TransientModel):
    _name = 'modulo_prubeas.lista_ingredientes'

    def inicia_ingrediente(self):
        id_receta = self._context['active_id']
        return self.env['modulo_pruebas.ingrediente'].browse(id_receta)

    def lista_ingredientes(self):
        id_receta = self._context['active_id']
        return self.env['modulo_pruebas.receta']\
            .search([('ingredientes.ingrediente.id', '=', id_receta)])

    ingrediente = fields.Many2one('modulo_pruebas.ingrediente', default=inicia_ingrediente)
    recetas = fields.Many2many('modulo_pruebas.receta', default=lista_ingredientes)

