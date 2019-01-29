"""Tests for helper."""
from typing import List, Sized, cast  # noqa: F401

import homeassistant_cli.helper as helper


def test_to_attributes_multiples():
    """Basic assertions on to_attributes."""
    data = helper.to_attributes("entity_id=entityone,attr1=val1")
    assert len(cast(Sized, data)) == 2

    assert data["entity_id"] == "entityone"
    assert data["attr1"] == "val1"


def test_to_attributes_none():
    """Basic assertions on to_attributes."""
    data = helper.to_attributes("")
    assert data == {}


def test_to_tuples():
    """Basic title test on to_tuples."""
    data = helper.to_tuples("a=entity_id,b=state")
    assert len(data) == 2
    assert data[0] == ("a", "entity_id")
    assert data[1] == ("b", "state")


def test_to_tuples_no_header():
    """Test to_tuples without header."""
    data = helper.to_tuples("entity_id,state")
    assert len(data) == 2
    assert data[0] == ("entity_id",)
    assert data[1] == ("state",)


def test_sorting_by_jsonpath():
    """Test sorting function by jsonpath works."""
    result = [
        {'id': 'Uno', 'no': 3},
        {'id': 'Duo', 'no': 2},
        {'id': 'Trio', 'no': 1},
        {'id': None, 'no': 0},
    ]  # type: List
    helper._sort_table(result, 'id')  # pylint: disable=W0212

    assert result[0].get('id') == 'Duo'
    assert result[1].get('id') == 'Trio'
    assert result[2].get('id') == 'Uno'
    assert result[3].get('id') is None

    helper._sort_table(result, 'no')  # pylint: disable=W0212

    assert result[0].get('id') is None
    assert result[1].get('id') == 'Trio'
    assert result[2].get('id') == 'Duo'
    assert result[3].get('id') == 'Uno'
