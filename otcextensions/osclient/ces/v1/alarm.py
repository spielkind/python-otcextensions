#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''CES Alarm v1 action implementations'''
import argparse
import logging

from osc_lib import utils
from osc_lib.command import command

from otcextensions.i18n import _
from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)

"""
ZONE_TYPES = ['private', 'public']


_formatters = {
    # 'traffic_limited_list': sdk_utils.ListOfDictColumn,
    # 'http_limited_list': sdk_utils.ListOfDictColumn,
    # 'connection_limited_list': sdk_utils.ListOfDictColumn,
}



"""

def _get_columns(item):
    column_map = {
    }
    hidden = ['location', 'links']
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


class ListAlarm(command.Lister):
    _description = _('List CES alarms')
    columns = (
        'id', 'name', 'alarm_enabled', 'alarm_action_enabled', 'alarm_state', 'alarm_level'
    )

    def get_parser(self, prog_name):
        parser = super(ListAlarm, self).get_parser(prog_name)
      
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.ces

        data = client.alarms()

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns
                 ) for s in data))
        return table


class ShowAlarm(command.ShowOne):
    _description = _('Show the alarm details')

    def get_parser(self, prog_name):
        parser = super(ShowAlarm, self).get_parser(prog_name)

        parser.add_argument(
            'alarm',
            metavar='<alarm>',
            help=_('UUID or name of the alarm.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.ces

        obj = client.find_alarm(
            parsed_args.alarm,
            ignore_missing=False
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteAlarm(command.Command):
    _description = _('Delete CES alarm')

    def get_parser(self, prog_name):
        parser = super(DeleteAlarm, self).get_parser(prog_name)

        parser.add_argument(
            'alarm',
            metavar='<alarm>',
            nargs='+',
            help=_('UUID or name of the alarm.')
        )

        return parser

    def take_action(self, parsed_args):
        if parsed_args.alarm:
            client = self.app.client_manager.ces
            for alarm in parsed_args.alarm:
                alarm = client.find_alarm(alarm, ignore_missing=False)
                client.delete_alarm(alarm=alarm)


class SetAlarm(command.ShowOne):
    _description = _('Change alarm_status_enabled to the opposite value of true / false.')

    def get_parser(self, prog_name):
        parser = super(ShowAlarm, self).get_parser(prog_name)

        parser.add_argument(
            'alarm',
            metavar='<alarm>',
            help=_('UUID or name of the alarm.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.ces

        alarm = client.find_alarm(parsed_args.alarm, ignore_missing=False)

        if alarm:
            obj = client.update_alarm_enabled(
                alarm=alarm
            )

            display_columns, columns = _get_columns(obj)
            data = utils.get_item_properties(obj, columns)

            return (display_columns, data)

"""

class CreateZone(command.ShowOne):
    _description = _('Create zone')

    def get_parser(self, prog_name):
        parser = super(CreateZone, self).get_parser(prog_name)

        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('DNS Name for the zone.')
        )
        parser.add_argument(
            '--email',
            metavar='<email>',
            help=_('E-mail for the zone. Used in SOA records for the zone.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description for this zone.')
        )
        parser.add_argument(
            '--type',
            metavar='{' + ','.join(ZONE_TYPES) + '}',
            type=lambda s: s.lower(),
            choices=ZONE_TYPES,
            help=_('Domain name type, the value of which can be '
                   '`public` or `private` .')
        )
        parser.add_argument(
            '--ttl',
            metavar='<300-2147483647>',
            type=int,
            # NOTE: py2 does not support such big int, skip unless py3-only
            # choices=range(300, 2147483647),
            help=_('TTL (Time to Live) for the zone.')
        )
        parser.add_argument(
            '--router_id',
            metavar='<router_id>',
            help=_('Router ID (VPC ID) for the private zone.')
        )
        parser.add_argument(
            '--router_region',
            metavar='<router_region>',
            help=_('Router region for the private zone.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dns

        attrs = {}

        if parsed_args.name:
            attrs['name'] = parsed_args.name
        if parsed_args.email:
            attrs['email'] = parsed_args.email
        if parsed_args.description:
            attrs['description'] = parsed_args.description
        if parsed_args.type:
            attrs['zone_type'] = parsed_args.type
        if parsed_args.ttl:
            attrs['ttl'] = parsed_args.ttl
        if parsed_args.type and parsed_args.type == 'private':
            if not parsed_args.router_id:
                msg = _('router_id is required for a private zone')
                raise argparse.ArgumentTypeError(msg)
            router = {
                'router_id': parsed_args.router_id
            }
            if parsed_args.router_region:
                router['router_region'] = parsed_args.router_region
            attrs['router'] = router

        obj = client.create_zone(
            **attrs
        )

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)





class AssociateRouterToZone(command.ShowOne):
    _description = _('Associate router with a private zone')

    def get_parser(self, prog_name):
        parser = super(AssociateRouterToZone, self).get_parser(prog_name)

        parser.add_argument(
            'zone',
            metavar='<zone>',
            help=_('UUID or name of the zone.')
        )
        parser.add_argument(
            '--router_id',
            metavar='<router_id>',
            help=_('Router ID (VPC ID) for the private zone.')
        )
        parser.add_argument(
            '--router_region',
            metavar='<router_region>',
            help=_('Router region for the private zone.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dns

        router = {
            'router_id': parsed_args.router_id
        }
        if parsed_args.router_region:
            router['router_region'] = parsed_args.router_region

        zone = client.find_zone(parsed_args.zone, ignore_missing=False)

        if zone:
            obj = client.add_router_to_zone(
                zone=zone,
                **router
            )

            display_columns, columns = _get_columns(obj)
            data = utils.get_item_properties(obj, columns)

            return (display_columns, data)


class DisassociateRouterToZone(command.ShowOne):
    _description = _('Disassociate router with a private zone')

    def get_parser(self, prog_name):
        parser = super(DisassociateRouterToZone, self).get_parser(prog_name)

        parser.add_argument(
            'zone',
            metavar='<zone>',
            help=_('UUID or name of the zone.')
        )
        parser.add_argument(
            '--router_id',
            metavar='<router_id>',
            help=_('Router ID (VPC ID) for the private zone.')
        )
        parser.add_argument(
            '--router_region',
            metavar='<router_region>',
            help=_('Router region for the private zone.')
        )

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.dns

        router = {
            'router_id': parsed_args.router_id
        }
        if parsed_args.router_region:
            router['router_region'] = parsed_args.router_region

        zone = client.find_zone(parsed_args.zone, ignore_missing=False)

        if zone:
            obj = client.remove_router_from_zone(
                zone=zone,
                **router
            )

            display_columns, columns = _get_columns(obj)
            data = utils.get_item_properties(obj, columns)

            return (display_columns, data)


class ListNameserver(command.Lister):
    _description = _('List DNS zone nameservers')
    columns = (
        'address', 'hostname', 'priority'
    )

    def get_parser(self, prog_name):
        parser = super(ListNameserver, self).get_parser(prog_name)

        parser.add_argument(
            'zone',
            metavar='<zone>',
            help=_('UUID or name of the zone.')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        zone = client.find_zone(parsed_args.zone, ignore_missing=False)

        if zone:
            data = client.nameservers(zone=zone)

            table = (self.columns,
                     (utils.get_item_properties(
                         s, self.columns, formatters=_formatters
                     ) for s in data))
            return table
"""