from typer.testing import CliRunner
from ygo_ultime_deck.main import app

runner = CliRunner()

def test_app_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Moteur d'optimisation de deck Yu-Gi-Oh!" in result.stdout
