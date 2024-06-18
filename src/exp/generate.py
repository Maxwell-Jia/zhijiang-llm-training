from transformers import AutoTokenizer, AutoModelForCausalLM
import json
from tqdm import tqdm

model_path = "/mnt/geogpt-gpfs/llm-course/public/models/command-r-v01"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cuda:7", load_in_8bit=True)

with open("./datasets/question_astro.txt", 'r') as f:
    questions = f.read().splitlines()
messages = []

for question in questions:
    message = [{"role": "user", "content": question}]
    messages.append(message)

batch_size = 8

for i in tqdm(range(0, len(messages), batch_size)):
    batch = messages[i:i+batch_size]
    input_ids = tokenizer.apply_chat_template(batch, tokenize=True, add_generation_prompt=True, return_tensors="pt", padding=True)

    input_ids = input_ids.to("cuda:7")
    
    gen_tokens = model.generate(
        input_ids, 
        max_new_tokens=512, 
        do_sample=True, 
        temperature=0.3,
    )
    
    with open("./datasets/question_astro_response.jsonl", 'a') as f:
        for response_id, gen_token in enumerate(gen_tokens):
            response = tokenizer.decode(gen_token, skip_special_tokens=True)

            data = json.dumps({
                "question": batch[response_id][0]["content"],
                "response": response.split('<|CHATBOT_TOKEN|>')[1]
            })

            f.write(data + "\n")