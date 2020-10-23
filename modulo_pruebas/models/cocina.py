# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class Cocina(models.Model):
    _name = 'modulo_pruebas.cocina'
    _description = 'Tipo de cocina'
    _rec_name = 'nombre'

    nombre = fields.Char(string="Nombre")
    descripcion = fields.Text(string="Descripción")
    recetas = fields.One2many('modulo_pruebas.receta', 'cocina')

    def obten_recetas_disponibles(self, cocina_id):
        consulta = """SELECT COUNT(*) as cantidad 
        FROM modulo_pruebas_receta AS receta 
        WHERE receta.disponible = true AND receta.cocina = """ + str(cocina_id)
        self._cr.execute(consulta)
        resultado = self._cr.fetchone()
        return resultado