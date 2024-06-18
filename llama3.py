import transformers
import torch

model_id = "bosonai/Higgs-Llama-3-70B"

pipeline = transformers.pipeline(
  "text-generation",
  model=model_id,
  model_kwargs={"torch_dtype": torch.bfloat16},
  device_map="auto",
)

messages = [
  {"role": "system", "content": "You are an AI assistant that speaks in the style of Sheldon Cooper. You are arguing with the user and is trying to prove the opposite of what the user said."},
  {"role": "user", "content": "The earth is round."},
]

prompt = pipeline.tokenizer.apply_chat_template(
  messages,
  tokenize=False,
  add_generation_prompt=True
)

outputs = pipeline(
  prompt,
  max_new_tokens=256,
  eos_token_id=[
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
    pipeline.tokenizer.eos_token_id,
  ],
  do_sample=True,
  temperature=1.0,
  top_p=0.95,
)
print(outputs[0]["generated_text"][len(prompt):])
