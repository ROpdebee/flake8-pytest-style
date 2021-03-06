from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import IncorrectFixtureNameUnderscore
from flake8_pytest_style.visitors import FixturesVisitor


def test_ok_with_return():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture(mocker):
            return 0
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_with_yield():
    code = """
        import pytest

        @pytest.fixture()
        def activate_context():
            with get_context() as context:
                yield context
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_nested_function():
    code = """
        @pytest.fixture()
        def _any_fixture(mocker):
            def nested_function():
                return 1

            mocker.patch('...', nested_function)
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_error_with_return():
    code = """
        import pytest

        @pytest.fixture()
        def _my_fixture(mocker):
            return 0
    """
    assert_error(
        FixturesVisitor,
        code,
        IncorrectFixtureNameUnderscore,
        name='_my_fixture',
        config=DEFAULT_CONFIG,
    )


def test_error_with_yield():
    code = """
        import pytest

        @pytest.fixture()
        def _activate_context():
            with get_context() as context:
                yield context
    """
    assert_error(
        FixturesVisitor,
        code,
        IncorrectFixtureNameUnderscore,
        name='_activate_context',
        config=DEFAULT_CONFIG,
    )
