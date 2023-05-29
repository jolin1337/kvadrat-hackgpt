import random
from gpt4all import GPT4All


gptj = GPT4All("ggml-gpt4all-j-v1.3-groovy")

print(gptj.model.thread_count())
gptj.model.set_thread_count(1)

messages = [{"role": "user", "content": "Hi, how are you today?"}]
messages = [{"role": "user", "content": "Hi, how are you today? Could you please tell me more about the second world war? What really happened back then with Anne Frank who wrote in her dirary?"}]
messages = [{"role": "user", "content": "Hej, har du något tips på en bra fil som är likt filmen \"en nyckel till frihet\""}]
for i in range(1):
    print("Iteration", i + 1)
    choices = gptj.chat_completion(messages, verbose=True, streaming=True)['choices']
    content = choices[int(random.random() * len(choices))]['message']['content']
    role = 'assistant' if i % 2 == 0 else 'user'
    messages.append({'role': role, 'content': content})
    #print(messages)
    print()

print(messages)
