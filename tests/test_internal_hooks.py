from hookery import Hook, InstanceHook, Hookable


def test_handler_registered_hook_on_simple_hook():
    handlers_seen = []

    hook = Hook()

    @hook.handler_registered
    def on_handler_registered(handler):
        assert callable(handler)
        handlers_seen.append(handler)

    hook(lambda: 1)
    hook(lambda: 2)

    assert hook.trigger() == [1, 2]
    assert len(handlers_seen) == 2
    assert [h() for h in handlers_seen] == [1, 2]


def test_handler_registered_hook_on_instance_hook():
    handlers_seen = []

    class Base(Hookable):
        before = InstanceHook()

        # TODO This handler gets registered twice!

        @before.handler_registered
        def on_handler_registered(handler):
            assert callable(handler)
            handlers_seen.append(handler)

        before(lambda: 1)

    assert len(handlers_seen) == 1

    Base.before(lambda: 2)
    assert len(handlers_seen) == 2

    b = Base()
    b.before(lambda: 3)
    assert len(handlers_seen) == 3

    assert b.before.trigger() == [1, 2, 3]
    assert [h() for h in handlers_seen] == [1, 2, 3]
