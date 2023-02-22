# -*- coding: utf-8 -*-
# Copyright (c) 2020 Lunel, Inc (https://www.lunel.co). All rights reserved.

{

    # App information
    'name': 'Automatic Bank Synchronization',
    'category': 'Accounting',
    'version': '15.0',
    'summary': 'Automatically import your bank transactions into Odoo with Plaid',
    'license': 'OPL-1',

    # Author
    'author': 'Lunel, Inc',
    'website': 'https://www.lunel.co',
    'maintainer': 'LuNel Inc.',

    # Dependencies
    'depends': ['stock'],

    # Views
    'data': [
         'wizard/images_import.xml',
    ],

    'demo': ['https://www.lunel.co/contactus'],
    'images': ['static/description/plaid_thumbnail.png'],
    'live_test_url': '',
    'installable': True,
    'application': False,
    'auto_install': False,

}
