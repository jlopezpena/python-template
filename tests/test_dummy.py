from ra.python_template.hello import say_hi


def test_dummy() -> None:
    """Dummy test for checking that CI works"""
    greet = say_hi("world")
    assert greet == "Hi, world"
