from jlp.python_template.hello import say_hi  # TEMPLATE: optional module


def test_dummy() -> None:
    greet = say_hi("world")
    assert greet == "Hi, world"
