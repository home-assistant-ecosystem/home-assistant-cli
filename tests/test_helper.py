"""Tests for helper."""
from typing import Sized, cast

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
