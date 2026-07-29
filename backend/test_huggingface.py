from app.llm.huggingface_client import HuggingFaceClient

client = HuggingFaceClient()

response = client.generate(
    "Say Hello in exactly one sentence."
)

print(response)