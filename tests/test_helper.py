"""Tests for helper."""
import homeassistant_cli.helper as helper


def test_to_attributes_multiples():
    """Basic assertions on to_attributes."""
    data = helper.to_attributes("entity_id=entityone,attr1=val1")
    assert len(data) == 2

    assert data["entity_id"] == "entityone"
    assert data["attr1"] == "val1"


def test_to_attributes_none():
    """Basic assertions on to_attributes."""
    data = helper.to_attributes("")
    assert data is None
