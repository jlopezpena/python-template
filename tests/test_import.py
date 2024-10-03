# Verify that our module can be installed...


def test_import() -> None:
    try:
        import python_template

        assert python_template is not None

    except ImportError:
        assert False
