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

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    subtotal_taxed = fields.Float(
        digits_compute=dp.get_precision('Product Price'),
        compute='_compute_subtotal_taxes',
    )

    subtotal_untaxed = fields.Float(
        digits_compute=dp.get_precision('Product Price'),
        compute='_compute_subtotal_taxes',
    )

    tax_on_subtotal = fields.Float(
        digits_compute=dp.get_precision('Product Price'),
        compute='_compute_subtotal_taxes',
    )

    @api.depends('price_subtotal', 'price_tax', 'price_total')
    def _compute_subtotal_taxes(self):
        for order in self:
            order.subtotal_taxed = order.price_total
            order.subtotal_untaxed = order.price_subtotal
            order.tax_on_subtotal = order.price_tax


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
