# Verify that our module can be installed...


def test_import():
    try:
        import python_template

        assert True
    except ImportError:
        assert False
