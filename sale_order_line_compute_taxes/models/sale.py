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

    @api.depends('tax_id', 'price_subtotal')
    def _compute_subtotal_taxes(self):
        # Based on sale.order/_amount_all method
        for order in self:
            cur = order.order_id.pricelist_id.currency_id
            order.tax_on_subtotal = \
                cur.round(self.env['sale.order']._amount_line_tax(order))
            order.subtotal_untaxed = cur.round(order.price_subtotal)
            order.subtotal_taxed = \
                cur.round(order.subtotal_untaxed + order.tax_on_subtotal)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
