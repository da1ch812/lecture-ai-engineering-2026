import importlib
from types import SimpleNamespace


def test_ask_streams_text_and_reports_performance(monkeypatch, capsys):
    ask_module = importlib.import_module("app.ask")
    usage = SimpleNamespace(prompt_token_count=3, candidates_token_count=8)
    chunks = [
        SimpleNamespace(text="Hel", usage_metadata=None),
        SimpleNamespace(text="lo", usage_metadata=usage),
    ]
    times = iter([10.0, 10.25, 11.25])

    class FakeModels:
        def generate_content_stream(self, *, model, contents):
            assert model == ask_module.MODEL
            assert contents == "question"
            return iter(chunks)

    class FakeClient:
        models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", lambda **kwargs: FakeClient())
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(times))

    assert ask_module.ask("question") == "Hello"

    output = capsys.readouterr().out
    assert output.startswith("Hello\n\n[計測結果]")
    assert f"モデル: {ask_module.MODEL}" in output
    assert "TTFT: 0.250 秒" in output
    assert "全体の応答時間: 1.250 秒" in output
    assert "生成速度: 8.00 tokens/sec" in output
    assert "入力トークン数: 3" in output
    assert "出力トークン数: 8" in output


def test_ask_reports_unavailable_metrics_without_text(monkeypatch, capsys):
    ask_module = importlib.import_module("app.ask")
    chunks = [SimpleNamespace(text=None, usage_metadata=None)]
    times = iter([1.0, 2.0])

    class FakeModels:
        def generate_content_stream(self, *, model, contents):
            return iter(chunks)

    class FakeClient:
        models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", lambda **kwargs: FakeClient())
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(times))

    assert ask_module.ask("question") == ""

    output = capsys.readouterr().out
    assert "TTFT: 計測不可" in output
    assert "全体の応答時間: 1.000 秒" in output
    assert "生成速度: 計測不可" in output
    assert "入力トークン数: 不明" in output
    assert "出力トークン数: 不明" in output