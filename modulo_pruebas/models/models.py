# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class Ingrediente(models.Model):
    _name = 'modulo_pruebas.ingrediente'
    _description = "Ingredientes"
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre")


class Receta(models.Model):
    _name = 'modulo_pruebas.receta'
    _description = 'Recetas'
    _rec_name = 'nombre'

    def activa(self):
        print("Estableciendo default")
        return True

    secuencia = fields.Char(string="Secuencia", readonly=True)
    nombre = fields.Char(string="Nombre")
    ingredientes = fields.One2many('modulo_pruebas.ingrediente_receta', 'receta')
    disponible = fields.Boolean(string="Disponible", default=activa)
    cocina = fields.Many2one('modulo_pruebas.cocina', string="Tipo de cocina")
    imagen = fields.Binary(string="Imágen")
    autor = fields.Many2one('res.users', string="Autor de la receta")
    precio = fields.Float()

    # propiedad relacionadas
    autor_imagen = fields.Image(related="autor.image_128", string="Foto del autor")

    # propiedades virtuales
    ingredientes_resumen = fields.Char(compute='_resumen_ingredientes')

    def activa_receta(self):
        self.disponible = not self.disponible
        print(f"Receta activada: {self.disponible}")
        return False

    @api.depends('ingredientes', 'cocina')
    def _resumen_ingredientes(self):
        for record in self:
            if record.ingredientes:
                resumen = ""
                for i in record.ingredientes:
                    resumen = (resumen and f"{resumen},") + f"{i.ingrediente.nombre}:{i.cantidad}"
                record.ingredientes_resumen = resumen
            else:
                record.ingredientes_resumen = "Sin ingredientes"

    @api.model
    def create(self, values):
        if not values['nombre']:
            raise UserError("El nombre no puede estar vacío")

        if not values['cocina']:
            italiana = self.env['modulo_pruebas.cocina'].search([('nombre', 'ilike', 'italiana')])
            values['cocina'] = italiana.id

        values['secuencia'] = self.env['ir.sequence'].next_by_code('modulo_pruebas.receta_secuencia')
        nuevo = super(Receta, self).create(values)
        return nuevo

    def write(self, values):
        if 'nombre' in values and not values['nombre']:
            values['nombre'] = self.nombre
        modificada = super(Receta, self).write(values)
        return modificada


class IngredienteReceta(models.Model):
    _name = 'modulo_pruebas.ingrediente_receta'

    receta = fields.Many2one('modulo_pruebas.receta')
    cantidad = fields.Integer()
    ingrediente = fields.Many2one('modulo_pruebas.ingrediente')


class Cocina(models.Model):
    _name = 'modulo_pruebas.cocina'
    _description = 'Tipo de cocina'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre")
    descripcion = fields.Text(string="Descripción")
    recetas = fields.One2many('modulo_pruebas.receta', 'cocina')


class Pedido(models.Model):
    _name = 'modulo_pruebas.pedido'
    _description = 'Pedidos de recetas'
    _rec_name = "estado"

    numero = fields.Char()
    cliente = fields.Many2one('res.users')
    estado = fields.Many2one('modulo_pruebas.estado_pedido', group_expand='_estados_del_pedido')
    detalles = fields.One2many('modulo_pruebas.detalle_pedido', 'pedido')

    # Propiedad virtual
    resumen = fields.Char(compute='_calcula_resumen')
    total = fields.Float(compute='_calcula_total')

    def _estados_del_pedido(self, grupo, dominio, orden):
        return self.env['modulo_pruebas.estado_pedido'].search([], order='orden Asc')

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
        super().write(values)

    def actualiza_cupon_1(self):
        cupones = self.env['modulo_pruebas.cupon'].search([('id', '=', 1)])
        for cupon in cupones:
            cupon.write({'nombre': '10% de descuento por cada 3 pedidos'})


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


class EstadoPedido(models.Model):
    _name = 'modulo_pruebas.estado_pedido'
    _description = 'Pedidos de recetas'
    _rec_name = 'nombre'

    orden = fields.Char()
    nombre = fields.Char()
