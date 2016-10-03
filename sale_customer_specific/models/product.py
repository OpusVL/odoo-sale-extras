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

from openerp import models, fields, api


class CustomerSpecificCommonMixin(object):
    def may_be_sold_to_customer(self, customer):
        """Return whether this product should be sold to the given customer.
        """
        self.ensure_one()
        if not self.is_customer_specific:
            return True
        if isinstance(customer, (int, long)):
            customer = self.browse(customer)
        return customer in self.specific_customer_ids
    

class ProductTemplate(models.Model, CustomerSpecificCommonMixin):
    _inherit = 'product.template'

    is_customer_specific = fields.Boolean()
    
    specific_customer_ids = fields.Many2many(
        string='Allowed customers',
        comodel_name='res.partner',
        domain=[('customer', '=', True)],
    )


class ProductProduct(models.Model, CustomerSpecificCommonMixin):
    _inherit = 'product.product'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
