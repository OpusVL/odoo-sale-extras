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

from decimal import Decimal
import re

from openerp import models, fields, api
from openerp.osv import osv
from openerp.osv import fields as OF
from openerp.tools.translate import _

import logging

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def _packaging_compatibility_warning(self, qty, uom_obj, pack):
        """Return the warning that requested quantity is incompatible with the packaging.

        qty: The quantity the user asked for
        uom_obj: The unit of measure browse object asked for
        pack: The packaging browse object
        """
        return _("You selected a quantity of %s %s.\n"
                 "But it's not compatible with the selected packaging.\n"
                 "Here is a proposition of quantities according to the packaging:\n"
                 "EAN: %s Quantity: %s Type of ul: %s") % \
                 (uom_obj.format_float(qty),
                  uom_obj.name,
                  (pack.ean or _('(n/a)')),
                  uom_obj.format_float(pack.qty),
                  pack.ul.name)

    @api.model
    def _stock_warning_info(self, requested_quantity, uom_record, product_obj):
        """Return the extra information for the out of stock warning.
        """
        def fmt_qty(qty):
            return uom_record.format_float(qty)
        return _('You plan to sell %s %s but you only have %s %s available !\nThe real stock is %s %s. (without reservations)') % \
                    (fmt_qty(requested_quantity), uom_record.name,
                     fmt_qty(max(0,product_obj.virtual_available)), uom_record.name,
                     fmt_qty(max(0,product_obj.qty_available)), uom_record.name)

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    def product_id_change_with_wh(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, warehouse_id=False, context=None):
        res = super(sale_order_line, self)\
          .product_id_change_with_wh(cr, uid, ids, pricelist, product, qty, uom,
                                     qty_uos, uos, name, partner_id, lang,
                                     update_tax, date_order, packaging,
                                     fiscal_position, flag, warehouse_id,
                                     context=context)
        if res:
            res = res.copy()   # avoid leaking changes
        else:
            return res
        warning = res.get('warning')
        if not warning:
            return res

        warning = warning.copy()  # avoid leaking changes
        not_enough_stock = _("Not enough stock ! : ")
        if not_enough_stock in warning['message']:

            product_obj = self.pool['product.product'].browse(cr, uid, product, context=context)
            uom_record = False
            if uom:
                product_uom_obj = self.pool['product.uom']
                uom_record = product_uom_obj.browse(cr, uid, uom, context=context)
                if product_obj.uom_id.category_id.id != uom_record.category_id.id:
                    uom_record = False
            if not uom_record:
                uom_record = product_obj.uom_id
            warn_msg = self._stock_warning_info(cr, uid, qty, uom_record, product_obj, context=context)
            # TODO is it really likely we'll need to replace in the middle of multiple messages?
            #      and do we care?
            #      for now I'm just replacing the entire message.
            warning['message'] = not_enough_stock + warn_msg + "\n\n"

        res['warning'] = warning
        return res
    
    def product_packaging_change(self, cr, uid, ids, pricelist, product, qty=0, uom=False,
        partner_id=False, packaging=False, flag=False, context=None):
        res = super(sale_order_line, self).\
          product_packaging_change(cr, uid, ids, pricelist, product, qty, uom,
                                   partner_id, packaging, flag, context=context)

        if res:
            res = res.copy()   # avoid leaking changes
        else:
            return res
        warning = res.get('warning')
        if not warning:
            return res

        warning = warning.copy()  # avoid leaking changes
        picking_information = _("Picking Information ! : ")
        if picking_information in warning['message']:
            product_obj = self.pool['product.product'].browse(
                cr, uid, product, context=context)

            pack = self.pool['product.packaging'].browse(
                cr, uid, packaging, context=context)
            uom_obj = self.pool['product.uom'].browse(cr, uid, uom, context=context)
            warn_msg = self._packaging_compatibility_warning(
                cr, uid, qty, uom_obj, pack, context=context)
            warning['message'] = picking_information + warn_msg + "\n\n"
        res['warning'] = warning
        return res


    
class ProductUOM(models.Model):
    _inherit = 'product.uom'

    def format_float(self, quantity):
        """Format a quantity to the given precision
        """
        self.ensure_one()
        dp = self._decimal_places()
        if dp is None:
            return str(quantity)
        
        fmt = "{:." + "{:d}".format(dp) + "f}"
        return fmt.format(quantity)


    def _decimal_places(self):
        """Return the number of decimal places to round to"""
        self.ensure_one()
        exponent = Decimal(str(self.rounding)).as_tuple().exponent
        return abs(exponent) if exponent <= 0 else None
        
        



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
