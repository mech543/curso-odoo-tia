# -*- coding: utf-8 -*-
# from odoo import http


# class ModuloPruebas(http.Controller):
#     @http.route('/modulo_pruebas/modulo_pruebas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modulo_pruebas/modulo_pruebas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('modulo_pruebas.listing', {
#             'root': '/modulo_pruebas/modulo_pruebas',
#             'objects': http.request.env['modulo_pruebas.modulo_pruebas'].search([]),
#         })

#     @http.route('/modulo_pruebas/modulo_pruebas/objects/<model("modulo_pruebas.modulo_pruebas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modulo_pruebas.object', {
#             'object': obj
#         })
