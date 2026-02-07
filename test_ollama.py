from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import json

llm = Ollama(
    model="qwen2.5:3b",
    temperature=0.1,
    timeout=30
)

prompt = PromptTemplate.from_template(
    "Return valid JSON only: {{\"number\": {num}}}"
)




raw = llm.invoke("Return valid JSON only: {\"status\": \"ok\"}")
parsed = json.loads(raw)

print(parsed["status"])
