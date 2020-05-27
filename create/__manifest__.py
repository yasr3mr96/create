# -*- coding: utf-8 -*-
{
    'name': "Create Your App",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Yasser Omar",
    'website': "yasr3mr@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/module.xml',
        'views/model.xml',
        # 'views/field.xml',
        'views/save.xml',
    ],
    'images': ['static/description/2.png'],
}
