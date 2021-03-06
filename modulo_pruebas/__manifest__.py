# -*- coding: utf-8 -*-
{
    'name': "modulo_pruebas",

    'summary': """
        Modulo creado en TIA durante el curso
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.tecinfadm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/ingrediente.xml',
        'views/templates.xml',
        'views/receta.xml',
        'views/cocina.xml',
        'views/pedido.xml',
        'views/tipousuario.xml',
        'views/usuario.xml',
        'views/desactiva_receta.xml',
        'views/lista_ingredientes.xml',
        'views/asigna_personal.xml',
        'views/empleado_restaurante.xml',
        'views/detalle_ingrediente.xml',
        'secuencias/receta.secuencia.xml',
        'reportes/reporte.xml',
        'reportes/cocinaRecetasTemplate.xml',
        'reportes/pedidos.reporte.xml',
        'reportes/pedidos.template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
