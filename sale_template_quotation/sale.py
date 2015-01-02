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

from openerp import models, fields, api, exceptions

class TemplateQuotation(models.Model):
    _inherit = "sale.order"

    is_template = fields.Boolean(default=False)
    quotation_ref = fields.Char()

    @api.one
    def convert_to_template(self):
        self.is_template = True


    #@api.one
    #def write(self, data):
    #    if self.is_template and ('state' not in data or data['state'] != 'cancelled'):
    #        raise exceptions.Warning('You cannot edit or change state of a quotation template')
    #    return super(TemplateQuotation, self).write(self, data)

    @api.one
    def copy(self, default=None):
        new_default = default or {'is_template': False}
        return super(TemplateQuotation, self).copy(default=new_default)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
