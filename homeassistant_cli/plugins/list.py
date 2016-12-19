"""List plugin for Home Assistant CLI (hass-cli)."""
import click
from homeassistant.core import State

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import json_output, timestamp

@click.command('list')
@click.option('--entry', '-e',
              type=click.Choice(['services', 'events', 'entities']),
              help='The entry to list.')
@click.option('--show-all',
              is_flag=True,
              help='Show all attributes')
@pass_context
def cli(ctx, entry, show_all):
    """List various entries of an instance."""
    import homeassistant.remote as remote

    ctx.log('Available %s', entry)
    if entry == 'services':
        services = remote.get_services(ctx.api)
        for service in services:
            ctx.log(json_output(service['services']))

    if entry == 'events':
        events = remote.get_event_listeners(ctx.api)
        for event in events:
            ctx.log(event)

    if entry == 'entities':
        entities = remote.get_states(ctx.api)
        for row in EntityFormatter(entities, show_all).get_rows():
            ctx.log(row)

    ctx.vlog('Details of %s, Created: %s', ctx.host, timestamp())


class EntityFormatter:
    def __init__(self, entities, show_all_attributes):
        self.rows = list(map(EntityFormatter._extract_fields, entities))
        self.entity_format = self._build_entity_format(show_all_attributes)
        self.field_widths = self._get_output_widths()

    @staticmethod
    def _build_entity_format(show_all_attributes):
        entity_format = "{name:<{name_length}}" \
                             "{entity_id:<{entity_id_length}}" \
                             "{state:<{state_length}}"
        if show_all_attributes:
            entity_format += "{attributes:<{attributes_length}}"
        return entity_format + "{last_changed:<{last_changed_length}}"

    @staticmethod
    def _extract_fields(entity: State):
        def format_attributes(attributes):
            formatted_attributes = ["%s=%s" % (key, item) for key, item in
                                    attributes.items() if key not in ['friendly_name']]
            return ", ".join(formatted_attributes)

        return {
            'name': entity.name,
            'entity_id': entity.entity_id,
            'state': entity.state,
            'last_changed': entity.last_changed.isoformat(),
            'attributes': format_attributes(entity.attributes)
        }

    def _get_output_widths(self):
        return {field + '_length': max_length + 3 for (field, max_length) in
                self._get_column_widths().items()}

    def _get_column_widths(self):
        longest = {}
        for row in self.rows:
            for (field, value) in (row.items()):
                longest[field] = max(longest.get(field, 0), len(value))
        return longest

    def _format_row(self, **kwargs):
        return self.entity_format.format(**kwargs, **self.field_widths)

    def get_rows(self):
        header = [self._format_row(
            name='Name',
            entity_id='Identifier',
            state='State',
            last_changed='Last change',
            attributes='Additional attributes')]
        return header + list(map(lambda row: self._format_row(**row), self.rows))
