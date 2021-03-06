# -*- coding: utf-8 -*-

##############################################################################
#
# Compute taxes on sale order line
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
    'name': 'Compute taxes on sale order line',
    'version': '0.1',
    'author': 'OpusVL',
    'website': 'http://opusvl.com/',
    'summary': 'Compute taxes on sale order line',
    
    'category': 'Technical',
    
    'description': """Compute taxes on sale order line.

    Adds tax_on_subtotal, subtotal_untaxed and subtotal_taxed to sale.order.line

    This is a technical module for use by other modules and through the API.

    Addition to reports and views should be done in a different module
    that depends on this one.

""",
    'images': [
    ],
    'depends': [
        'sale',
    ],
    'data': [
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
