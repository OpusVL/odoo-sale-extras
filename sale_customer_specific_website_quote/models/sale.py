# -*- coding: utf-8 -*-

##############################################################################
#
# Customer-specific products - suggested products integration
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

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('partner_id', 'options.product_id')
    def _check_options_buyable_by_customer(self):
        self._error_if_not_allowed_to_buy_any_of(self.partner_id, self.mapped('options.product_id'))



class SaleOrderOption(models.Model):
    _inherit = 'sale.order.option'

    order_partner_id = fields.Many2one(
        related=['order_id', 'partner_id'],
        comodel_name='res.partner',
    )

    @api.onchange('product_id', 'order_partner_id')
    def _check_option_buyable_by_customer(self):
        self.env['sale.order.line']._error_if_not_allowed_to_buy(self.order_partner_id, self.product_id)
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
