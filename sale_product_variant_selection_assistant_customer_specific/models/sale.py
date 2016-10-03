# -*- coding: utf-8 -*-

##############################################################################
#
# Link variant assistant with customer-specific products
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

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('variant_assistant_product_template_id')
    def _onchange_variant_assistant_product_template_id_order_partner_id(self):
        template = self.variant_assistant_product_template_id
        partner = self.order_id.partner_id
        self._error_if_not_allowed_to_buy(partner=partner, product=template)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
