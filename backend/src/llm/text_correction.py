from typing import List
import re
import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)
from src.llm.llm_call import llm_call
from src.llm.prompt import get_prompt

class TextCorrection:
    """
    日本語テキストを校閲ルールに従って置換するユーティリティ。

    Parameters
    ----------
    model : str
        LLM のモデル名（既定: "gpt-4o"）
    mode : str
        "openai" | "anthropic" のいずれかを選択（既定: "openai"）
    max_input_chars : int
        入力文字数上限（既定: 800）
    chunk_chars : int
        チャンク分割時の最大文字数（既定: 300）
    """
    # プロンプトを取得
    _RULE_PROMPT, _ = get_prompt()

    _SENT_SPLIT_RE = re.compile(r"(?<=[。！？\?！])\s*|\n+")

    def __init__(
        self,
        model: str = "gpt-4o",
        mode: str = "openai",
        max_input_chars: int = 800,
        chunk_chars: int = 200,
    ) -> None:
        self.model = model
        self.mode = mode
        self.max_input_chars = max_input_chars
        self.chunk_chars = chunk_chars

    #  内部ユーティリティ #
    def _split_sentences(self, text: str) -> List[str]:
        """句点・改行で文を粗く切る"""
        return [
            s.strip() for s in self._SENT_SPLIT_RE.split(text) if s.strip()
        ]

    def _chunk(self, sentences: List[str]) -> List[str]:
        """指定長を超えないよう文をまとめる"""
        chunks, buf = [], ""
        for s in sentences:
            if len(buf) + len(s) > self.chunk_chars:
                chunks.append(buf)
                buf = s
            else:
                buf += s
        if buf:
            chunks.append(buf)
        return chunks

    # ---------- 公開 API ------------------------------------------------ #
    def proofread(self, text: str) -> str:
 
        sentences = self._split_sentences(text)
        chunks    = self._chunk(sentences)

        corrected_chunks: List[str] = []

        for ch in chunks:
            _, user_prompt = get_prompt(ch)
            # ---- Anthropic だけ system を messages から外す ----
            if self.mode == "anthropic":
                
                messages = [{"role": "user", "content": user_prompt}]
                system_prompt = self._RULE_PROMPT
            else:
                messages = [
                    {"role": "system", "content": self._RULE_PROMPT},
                    {"role": "user",   "content": user_prompt},
                ]
                system_prompt = self._RULE_PROMPT  

            out = llm_call(
                messages=messages,
                model=self.model,
                temperature=0, # o1シリーズでtempを渡すとエラー吐くかもしれないです
                system_prompt=system_prompt,
                mode=self.mode,
            )
            corrected_chunks.append(out)
            

        return "".join(corrected_chunks)


    # `obj(text)` で呼び出せるように
    __call__ = proofread


# test
if __name__ == "__main__":
    sample = """
私たちのチームでは、テレワークの普及は今後も加速すると思います。特に、大都市に拠点を置く企業ほど出社率はさらに低下すると思う。これにより、コミュニケーションの質が下がるのではないかと思いますが、同時に移動時間が削減されるメリットは大きいという気がします。リーダーが意識的に雑談の場を設けることが不可欠なのではないでしょうか。また、情報共有の仕組みを見直すべき時期なのではないか。今のままではナレッジが属人化するかもしれませんし、新人が孤立するかもしれない。そこで、定例ミーティングの後に5分間の雑談タイムを設けた方がいいですし、週報を自動で集計するツールを導入した方がいい。さらに、目標設定のプロセスをシンプルにしてほしいですし、ガイドラインもアップデートしてほしい。長時間労働は良くないと思いますし、多様性を尊重するカルチャーが大切だと思います。こうした取り組みが奏功すれば、生産性は着実に向上するようになり、組織全体がよりアジャイルになると思います。
"""

    pf = TextCorrection()  
    result = pf(sample)
    print(result)