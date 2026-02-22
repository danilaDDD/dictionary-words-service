import pytest

from settings.settings import Settings, load_settings


@pytest.mark.unit
def test_env():
    import os
    assert os.getenv('ENV') == 'test'

@pytest.mark.unit
def test_load_settings_with_test_env():
    settings = load_settings()
    assert settings is not None
    assert "test" in settings.get_database_url()