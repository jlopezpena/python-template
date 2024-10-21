# Verify that our module can be installed...

import jlp.python_template as pt


def test_import() -> None:
    assert pt is not None
