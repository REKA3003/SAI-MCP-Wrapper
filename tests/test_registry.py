from basesmcp import ToolRegistry


def test_bare_and_parameterized_registration():
    reg = ToolRegistry()

    @reg.register
    def alpha():
        return "a"

    @reg.register(name="bravo", tags={"x"})
    def beta():
        return "b"

    names = [spec.options.get("name", spec.fn.__name__) for spec in reg.specs]
    assert names == ["alpha", "bravo"]


def test_apply_registers_onto_server():
    reg = ToolRegistry()

    @reg.register(name="hello")
    def hello():
        return "hi"

    calls = []

    class FakeServer:
        def tool(self, **options):
            def decorator(fn):
                calls.append((options.get("name", fn.__name__), fn))
                return fn

            return decorator

    names = reg.apply(FakeServer())
    assert names == ["hello"]
    assert calls[0][0] == "hello"


def test_decorated_function_is_unchanged():
    reg = ToolRegistry()

    @reg.register
    def double(x):
        return x * 2

    assert double(4) == 8
