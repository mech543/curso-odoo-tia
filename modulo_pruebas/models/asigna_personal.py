from odoo import models, fields


class AsignaPersonal(models.TransientModel):
    _name = 'modulo_pruebas.mt_asigna_personal'

    def obten_pedido(self):
        id_pedido = self._context['active_id']
        return self.env['modulo_pruebas.pedido'].browse(id_pedido)

    def obten_recepcionista(self):
        return self.obten_pedido().recepcionista

    def obten_chef(self):
        return self.obten_pedido().cocinero

    def obten_repartidor(self):
        return self.obten_pedido().repartidor

    pedido = fields.Many2one('modulo_pruebas.pedido', default=obten_pedido)
    personal_recepcion = fields.Many2one('hr.employee', default=obten_recepcionista)
    personal_preparacion = fields.Many2one('hr.employee', default=obten_chef)
    personal_entrega = fields.Many2one('hr.employee', default=obten_repartidor)

    # Propiedades relacionadas image_1920

    personal_recepcion_foto = fields.Image(related='personal_recepcion.image_1920')
    personal_preparacion_foto = fields.Image(related='personal_preparacion.image_1920')
    personal_entrega_foto = fields.Image(related='personal_entrega.image_1920')

    def actualiza_pedido(self):
        self.pedido.write({
            'recepcionista': self.personal_recepcion.id,
            'cocinero': self.personal_preparacion.id,
            'repartidor': self.personal_entrega.id
        })
        return {'type': 'ir.actions.act_window_close'}

