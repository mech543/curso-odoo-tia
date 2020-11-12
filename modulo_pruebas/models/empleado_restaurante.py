# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class EmpleadoRestaurante(models.Model):
    _inherit = 'hr.employee'

    tipo = fields.Many2one('modulo_pruebas.tipo_usuario')
    activo = fields.Boolean(default=True)

    # Propiedades virtuales
    cuenta_pedidos = fields.Integer(compute='_cuenta_pedidos_empleado')

    def _cuenta_pedidos_empleado(self):
        auxiliar = {'R-RECEPCION': 'recepcionista', 'R-CHEF': 'cocinero', 'R-REPARTIDOR': 'repartidor'}
        for record in self:
            if record.tipo and record.tipo.clave:
                propiedad = auxiliar[record.tipo.clave]
                record.cuenta_pedidos = self.env['modulo_pruebas.pedido']\
                    .search_count([(propiedad, '=', record.id), ('activa', '=', True)])
            else:
                record.cuenta_pedidos = 0

    def lista_pedidos(self):
        auxiliar = {'R-RECEPCION': 'recepcionista', 'R-CHEF': 'cocinero', 'R-REPARTIDOR': 'repartidor'}
        propiedad = auxiliar[self.tipo.clave]
        return {
            'type': "ir.actions.act_window",
            "name": f"Pedidos de {self}",
            "res_model": 'modulo_pruebas.pedido',
            "view_mode": 'tree,form',
            "domain": [(propiedad, '=', self.id), ('activa', '=', True)],
            "context": {f'default_{propiedad}': self.id}
        }

