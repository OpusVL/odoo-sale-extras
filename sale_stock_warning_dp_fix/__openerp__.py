# -*- coding: utf-8 -*-

##############################################################################
#
# Fix for decimal places on sale stock warnings
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
    'name': 'Fix for decimal places on Sale Order stock warnings',
    'version': '0.1',
    'author': 'OpusVL',
    'website': 'http://opusvl.com/',
    'summary': 'Fix for decimal places on sale stock warnings',
    
    'description': """Changes the stock warnings that are shown when adding
a sale order line, so that they show the number of decimal places defined in the
Unit of Measure.  For example if the chosen Unit of Measure has an accuracy of
0.00100, then the quantities in the warnings will be shown to 3 decimal places.

The modified warnings are as follows:

* The 'Picking Information' message shown when you choose a Packaging that is incompatible with the Quantity you've asked for

* The 'Not enough Stock' message shown when you enter a quantity above that available.

By default, the number of decimal places in these messages is fixed.
Installing this module changes that behaviour.

A current known limitation is that if there were more than one warning
generated from a specific action, then the ones other than those targetted will
be suppressed.  If this turns out to be an issue for you, please file a bug.
""",
    'images': [
    ],
    'depends': [
        'sale_stock',
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
