"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    started_at = time.perf_counter()
    response_text: list[str] = []
    first_token_at: float | None = None
    usage = None

    for chunk in client.models.generate_content_stream(
        model=MODEL, contents=question
    ):
        text = chunk.text
        if text:
            if first_token_at is None:
                first_token_at = time.perf_counter()
            response_text.append(text)
            print(text, end="", flush=True)

        if chunk.usage_metadata is not None:
            usage = chunk.usage_metadata

    finished_at = time.perf_counter()
    total_time = finished_at - started_at
    ttft = first_token_at - started_at if first_token_at is not None else None
    generation_time = total_time - ttft if ttft is not None else None
    output_tokens = usage.candidates_token_count if usage is not None else None
    input_tokens = usage.prompt_token_count if usage is not None else None

    print("\n\n[計測結果]")
    print(f"モデル: {MODEL}")
    print(f"TTFT: {ttft:.3f} 秒" if ttft is not None else "TTFT: 計測不可")
    print(f"全体の応答時間: {total_time:.3f} 秒")
    if (
        output_tokens is not None
        and generation_time is not None
        and generation_time > 0
    ):
        print(f"生成速度: {output_tokens / generation_time:.2f} tokens/sec")
    else:
        print("生成速度: 計測不可")
    displayed_input_tokens = input_tokens if input_tokens is not None else "不明"
    displayed_output_tokens = output_tokens if output_tokens is not None else "不明"
    print(f"入力トークン数: {displayed_input_tokens}")
    print(f"出力トークン数: {displayed_output_tokens}")

    return "".join(response_text)


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[質問] {args.question}\n")
    try:
        ask(args.question)
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
