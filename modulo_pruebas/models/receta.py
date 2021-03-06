from odoo import models, fields, api
from odoo.exceptions import UserError


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
    cuenta_ingredientes = fields.Integer(compute='_calcula_cuenta_ingredientes')


    def activa_receta(self):
        self.disponible = not self.disponible
        print(f"Receta activada: {self.disponible}")
        return False

    @api.onchange('ingredientes', 'cocina')
    def ejemplo_change(self):
        def calcula_precio():
            return 10 * 800
        # warning, domain, value
        if self.cocina.nombre == 'Italiana':
            return {
                'warning': {
                    'title': 'Advertencia',
                    'message': 'Solo hay un chef para la cocina italiana',
                    'type': 'notification'
                },
                'domain': {
                    'autor': []
                },
                'value': {
                    'precio': calcula_precio()
                }
            }

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

    def _calcula_cuenta_ingredientes(self):
        for record in self:
            record.cuenta_ingredientes = self.env['modulo_pruebas.ingrediente_receta']\
                                .search_count([('receta', '=', record.id)])

    def lista_ingredientes(self):
        return {
            'type': "ir.actions.act_window",
            "name": f"Ingredientes de {self.nombre}",
            "res_model": 'modulo_pruebas.ingrediente_receta',
            "view_mode": 'tree,form',
            'domain': [('receta', '=', self.id)],
            'context': {'default_receta': self.id, 'default_cantidad': 2}
        }
