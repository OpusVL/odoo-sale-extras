# -*- coding: utf-8 -*-

##############################################################################
#
# Customer-specific products
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

from openerp import models, fields, api, exceptions
from openerp.tools.translate import _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
    uom=False, qty_uos=0, uos=False, name='', partner_id=False,
    lang=False, update_tax=True, date_order=False, packaging=False,
    fiscal_position=False, flag=False, context=None):
        res = super(SaleOrderLine, self).product_id_change(cr, uid, ids,
            pricelist, product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag, context=context
        )
        if not (partner_id and product):
            return res
        partner = self.pool['res.partner'].browse(cr, uid, partner_id, context=context)
        prod = self.pool['product.product'].browse(cr, uid, product, context=context)
        self._error_if_not_allowed_to_buy(cr, uid, partner, prod, context=context)
        return res

    @api.model
    def _error_if_not_allowed_to_buy(self, partner, product):
        if not (product and partner):
            return
        if not product.may_be_sold_to_customer(partner):
            raise exceptions.ValidationError(_("Product {prod_name} can't be sold to customer {cust_name}").format(
                prod_name=product.display_name,
                cust_name=partner.display_name,
            ))
        
    @api.constrains('product_id', 'order_partner_id')
    def _check_product_id(self):
        self._error_if_not_allowed_to_buy(product=self.product_id, partner=self.order_partner_id)
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
