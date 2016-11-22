# -*- coding: utf-8 -*-

##############################################################################
#
# Notifications for rentals
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
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from itertools import groupby

import datetime

class SaleRentalNotifications(models.Model):
    _name = 'sale.rental.notifications'

    @api.model
    def send_start_notifications(self):
        """Intended to be run once, daily, as early as possible."""
        ignore_states = 'draft sent cancel'.split()   # TODO are waiting_date, invoice_except and shipping_except also to be ignored
        today = datetime.datetime.utcnow()
        def group_key(line):
            return line.order_partner_id
        rental_lines = self.env['sale.order.line'].search([
            ('rental', '=', True),
            ('start_date', '=', today.strftime(DEFAULT_SERVER_DATE_FORMAT)),   # Comparing in UTC
            ('order_id.state', 'not in', ignore_states)
        ]).sorted(group_key)
        if not rental_lines:
            return False
        template = self.env.ref('sale_rental_notifications.start_notification_email_template')
        for partner, rental_lines in groupby(rental_lines, group_key):
            template.with_context(
                rental_lines=list(rental_lines),
                rental_date=today.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            ).send_mail(partner.id)
        return False
        
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
