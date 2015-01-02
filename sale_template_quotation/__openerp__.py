# -*- coding: utf-8 -*-

##############################################################################
#
# Template Quotations
# Copyright (C) 2015 OpusVL (<http://opusvl.com/>)
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
    'name': 'Template Quotations',
    'version': '0.1',
    'author': 'OpusVL',
    'website': 'http://opusvl.com/',
    'summary': 'Allow quotations to be frozen for use as templates',
    
    'category': 'Sales',
    
    'description': """Allow quotations to be frozen for use as templates.

A new button is added to the Quotation screen, "Convert to Template", which
freezes the quotation preventing it from being edited or converted to a sales
order.

A new Quotation Reference field is also created which must be filled in
before conversion to a template.
""",
    'images': [
    ],
    'depends': [
        'sale',
    ],
    'data': [
        'sale_view.xml',
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
