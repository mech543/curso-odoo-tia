# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class Pedido(models.Model):
    _name = 'modulo_pruebas.pedido'
    _description = 'Pedidos de recetas'
    _rec_name = "estado"

    numero = fields.Char()
    cliente = fields.Many2one('res.users')
    estado = fields.Many2one('modulo_pruebas.estado_pedido', group_expand='_estados_del_pedido')
    detalles = fields.One2many('modulo_pruebas.detalle_pedido', 'pedido')
    recepcionista = fields.Many2one('hr.employee')
    cocinero = fields.Many2one('hr.employee')
    repartidor = fields.Many2one('hr.employee')
    activa = fields.Boolean(default=True)

    # Propiedad virtual
    resumen = fields.Char(compute='_calcula_resumen')
    total = fields.Float(compute='_calcula_total')

    def obten_porcentaje_cliente_exitoso(self):
        orden_cliente = self.cliente.id
        consulta = """ 
            SELECT
                estado.orden
            FROM
                modulo_pruebas_pedido AS pedido
                    INNER JOIN res_users AS cliente ON pedido.cliente = cliente.id
                    INNER JOIN modulo_pruebas_estado_pedido AS estado ON pedido.estado = estado.id
            WHERE
                cliente.id = 
                   """ + str(orden_cliente)
        self._cr.execute(consulta)
        pedidos_cliente = self._cr.fetchall()
        cancelados = len([a for a in pedidos_cliente if '6' in a])
        porcentaje = ((len(pedidos_cliente) - cancelados)*100)/len(pedidos_cliente)
        return int(porcentaje)

    def obten_pedidos_cliente(self):
        return self.env['modulo_pruebas.pedido'].search([('cliente', '=', self.cliente.id), ('id', '!=', self.id)])

    def _estados_del_pedido(self, grupo, dominio, orden):
        return self.env['modulo_pruebas.estado_pedido'].search([('orden', '<', 6)], order='orden Asc')

    def _calcula_resumen(self):
        for record in self:
            fila = '<li class="list-group-item">'
            if record.detalles:
                resumen = '<ul class="list-group">'
                for i in record.detalles:
                    resumen = f'{resumen}{fila}{i.cantidad} {i.receta.nombre}</li>'
                record.resumen = f'{resumen}</ul>'
            else:
                record.resumen = "Pedido vacío"

    @api.depends('detalles')
    def _calcula_total(self):
        for pedido in self:
            pedido.total = sum([detalle.importe for detalle in pedido.detalles])

    @api.model
    def create(self, values):
        if not values['cliente']:
            raise UserError("Se requiere un cliente")

        if 'detalles' not in values:
            raise UserError("Se requiere al menos un detalle en el pedido")

        estado = self.env['modulo_pruebas.estado_pedido'].search([('nombre', 'ilike', 'sin atender')])
        values['estado'] = estado.id

        values['numero'] = self.env['ir.sequence'].next_by_code('modulo_pruebas.pedido_secuencia')

        retorno = super().create(values)
        pedidos_cliente = self.env['modulo_pruebas.pedido'].search([('cliente', '=', values['cliente'])])
        if len(pedidos_cliente) % 3 == 0:
            dic_cupon = {'nombre': '10% descuento por 3 pedidos', 'descuento': 10, 'cliente': values['cliente']}
            self.env['modulo_pruebas.cupon'].create(dic_cupon)
        return retorno

    def write(self, values):
        estado_anterior = int(self.estado.orden)
        edo = self.env['modulo_pruebas.estado_pedido'].browse(values['estado']).orden if 'estado' in values else -1
        edo = int(edo)
        es_asignable = estado_anterior in [0, 5, 6] and self.activa and edo not in [0, 5, 6]
        es_reactivada = not self.activa and 'activa' in values and values['activa']

        if es_asignable or es_reactivada:
            pedidos_en_proceso = self.search(['&', ('estado.orden', 'in', ['1', '2', '3', '4']), ('activa', '=', 1)])
            if len(pedidos_en_proceso) >= 5:
                raise UserError("No se puede atender esta orden, el restaurante está saturado.")

        super().write(values)

    def actualiza_cupon_1(self):
        cupones = self.env['modulo_pruebas.cupon'].search([('id', '=', 1)])
        for cupon in cupones:
            cupon.write({'nombre': '10% de descuento por cada 3 pedidos'})

    def finaliza_turno(self):
        no_finalizados = self.env['modulo_pruebas.pedido'].search([('estado.orden', '<', 5)])
        if no_finalizados:
            op_cancelada = self.env['modulo_pruebas.estado_pedido'].search([('nombre', 'ilike', 'cancelada')])
            for no_finalizado in no_finalizados:
                no_finalizado.write({'activa': False, 'estado': op_cancelada.id})

        finalizadas = self.env['modulo_pruebas.pedido'].search([('estado.nombre', 'ilike', 'finalizada')])
        if finalizadas:
            for finalizada in finalizadas:
                finalizada.write({'activa': False})

    def genera_reporte_administrador(self):
        pedidos = self.search([('activa', '=', True), ('cliente.name', 'ilike', 'administrador')])
        return self.env.ref('modulo_pruebas.action_report_pedidos').report_action(pedidos)

    @api.onchange('recepcionista')
    def seleccion_recepcionista(self):
        return self.seleccion_empleado('recepcionista', self.recepcionista.id)

    @api.onchange('cocinero')
    def seleccion_cocinero(self):
        return self.seleccion_empleado('cocinero', self.cocinero.id)

    @api.onchange('repartidor')
    def seleccion_repartidor(self):
        return self.seleccion_empleado('repartidor', self.repartidor.id)

    def seleccion_empleado(self, tipo, id_empleado):

        if self.id:
            cuenta = self.env['modulo_pruebas.pedido']\
                .search_count(['&', (tipo, '=', id_empleado), ('id', '!=', self.id), ('activa', '=', True)])
        else:
            cuenta = self.env['modulo_pruebas.pedido'] \
                .search_count(['&', (tipo, '=', id_empleado), ('activa', '=', True)])

        if cuenta:
            return {
                'warning': {
                    'title': 'Advertencia',
                    'message': 'Este empleado ya está asignado a otro pedido',
                    'type': 'notification'
                }
            }


