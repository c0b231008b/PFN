import yaml
from openai import OpenAI
from typing import List
import anthropic


with open("src/config/config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)

def llm_call(messages: List, 
             model: str = "gpt-4o-mini",
             temperature: int = 0,
             max_tokens: int = 2048,
             system_prompt: str = "you are assistant",
             mode: str = "openai"
               ) -> str:
    """
    モデル名を指定して、LLMを呼び出す

    Parameters:
    - messages (List): モデルに送信するメッセージのリスト
    - model (str): 使用するモデル名を指定。"gpt-4o-mini"や"gpt-4o-2024-08-06"などのopenaiのモデルと、
    "claude-3-5-sonnet-20241022"などのanthropicのモデルが選択可能
    - temperature (int): モデルの応答のランダム性を制御するパラメータ
    - max_tokens (int): モデル応答の最大トークン数
    - system_prompt (str): システムプロンプト
    - mode (str): 使用するLLMのモデルを指定。"openai"または"anthropic"

    Returns:
    - str: モデルからの応答
    """
    res = ""
    if mode == "openai":
        OPENAI_KEY = configs["OPENAI_API_KEY"]
        client = OpenAI(api_key=OPENAI_KEY)

        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=messages,
            stream=False,
        )
        res = response.choices[0].message.content
    
    elif mode == "anthropic":
        client = anthropic.Anthropic(
            api_key=configs["ANTHROPIC_API_KEY"]
        )
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt, 
            messages=messages
        )
        res = message.content[0].text
    
    return res


if __name__ == "__main__":
    # テスト用のメッセージ
    messages = [
        {
            "role": "user",
            "content": "hi"
        }
    ]

    res = llm_call(messages=messages, 
                 model="o1",
                 mode="openai"
                 )
    print(res)