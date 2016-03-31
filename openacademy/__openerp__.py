# -*- coding: utf-8 -*-
# © <2016> <Luis Felipe Mileo>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Open Academy",
    "summary": "Module summary",
    "version": "8.0.1.0.0",
    "category": "custom",
    "website": "https://odoo-community.org/",
    "author": "KMEE, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/openacademy.xml',
        'views/res_partner_view.xml',
    ]
}
