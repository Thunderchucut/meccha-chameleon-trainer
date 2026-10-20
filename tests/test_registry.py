from meccha_trainer.core.contracts import PluginManifest, TrainerContext
from meccha_trainer.core.registry import PluginRegistry


class _Dummy:
    PLUGIN_MANIFEST = PluginManifest(
        name="dummy", version="0.1.0", author="test", api=1,
    )

    def on_load(self, ctx: TrainerContext) -> None: ...
    def on_tick(self, ctx: TrainerContext) -> None: ...
    def on_unload(self) -> None: ...


def test_register_and_lookup():
    reg = PluginRegistry()
    reg.register(_Dummy())
    assert reg.get("dummy") is not None
    assert [m.name for m in reg.manifests()] == ["dummy"]


def test_api_mismatch_rejected():
    class Bad(_Dummy):
        PLUGIN_MANIFEST = PluginManifest(name="bad", version="0", author="t", api=99)

    reg = PluginRegistry()
    try:
        reg.register(Bad())
    except RuntimeError:
        return
    raise AssertionError("expected RuntimeError for api mismatch")