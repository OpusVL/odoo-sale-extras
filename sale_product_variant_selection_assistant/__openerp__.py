# -*- coding: utf-8 -*-

##############################################################################
#
# Sale - Product Variant Selection Assistant
# Copyright (C) 2016 OpusVL (<http://opusvl.com/>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Sale - Product Variant Selection Assistant',
    'version': '0.1',
    'author': 'OpusVL',
    'website': 'http://opusvl.com/',
    'summary': 'Adds fields to Sale Order Line form allowing easier selection of product variants based on product attributes',
    
    'category': 'Sales',
    
    'description': """Adds fields to Sale Order Line form allowing easier selection of product variants based on product attributes.
    In order for a user to use this features, they must be in "Sales / Own Leads" and "Technical Settings / Properties on lines"
""",
    'images': [
    ],
    'depends': [
        'sale',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
