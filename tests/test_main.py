import pytest
from src.main import ArchitectureBot


def test_add_standard():
    bot = ArchitectureBot("Bridge Project")
    bot.add_standard("ISO 9001")
    assert "ISO 9001" in bot.standards


def test_check_compliance_returns_dict():
    bot = ArchitectureBot("Road Project")
    bot.add_standard("Local Road Safety Standard")
    design = {"road_width": "7m"}
    results = bot.check_compliance(design)
    assert isinstance(results, dict)
    assert "Local Road Safety Standard" in results


class TestReportGeneration:
    def test_generate_report_contains_project_name(self):
        bot = ArchitectureBot("Airport Project")
        bot.add_standard("ISO 14001")
        results = bot.check_compliance({"runway_length": "3km"})
        report = bot.generate_report(results)
        assert "Airport Project" in report
        assert "ISO 14001" in report
