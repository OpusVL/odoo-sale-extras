# -*- coding: utf-8 -*-

##############################################################################
#
# Split SKU from Description on Sale Order printout
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

from openerp import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    description_without_sku = fields.Char(
        compute="_description_without_sku_compute",
        readonly=True,
    )

    product_sku = fields.Char(
        related=['product_id', 'default_code'],
        readonly=True,
    )

    @api.depends('name', 'product_sku')
    @api.one
    def _description_without_sku_compute(self):
        if self.product_sku and self.name:
            sku_prefix = '[%s] ' % (self.product_sku,)
            self.description_without_sku = self.name.replace(sku_prefix, '')
        else:
            self.description_without_sku = self.name
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
