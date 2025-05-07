from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.llm.text_correction import TextCorrection

app = FastAPI()
pf = TextCorrection()
corrected = pf("私たちのチームでは、テレワークの普及は今後も加速すると思います。特に、大都市に拠点を置く企業ほど出社率はさらに低下すると思う。これにより、コミュニケーションの質が下がるのではないかと思いますが、同時に移動時間が削減されるメリットは大きいという気がします。リーダーが意識的に雑談の場を設けることが不可欠なのではないでしょうか。また、情報共有の仕組みを見直すべき時期なのではないか。今のままではナレッジが属人化するかもしれませんし、新人が孤立するかもしれない。そこで、定例ミーティングの後に5分間の雑談タイムを設けた方がいいですし、週報を自動で集計するツールを導入した方がいい。さらに、目標設定のプロセスをシンプルにしてほしいですし、ガイドラインもアップデートしてほしい。長時間労働は良くないと思いますし、多様性を尊重するカルチャーが大切だと思います。こうした取り組みが奏功すれば、生産性は着実に向上するようになり、組織全体がよりアジャイルになると思います。")
print(corrected)
# result = pf(sample)
# print(result)

# CORS設定（Reactとローカル開発するため）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProofreadRequest(BaseModel):
    text: str


@app.post("/proofread")
async def proofread(request: ProofreadRequest):
    corrected = pf(request.text)
    # corrected = f"校正済みのテキストです: {request.text}"
    return {"corrected_text": corrected}
