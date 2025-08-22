from llama_cpp import Llama
from application.analytics_engines.industry_cleanser_analysis import cross_tabulation_industry_sector as ctis
import os
from dotenv import load_dotenv

# Initialize environment
load_dotenv()
MODEL_PATH = os.getenv('MODEL_PATH')

# Initialize LLM
model = Llama(
    model_path=MODEL_PATH,
    verbose=False,
    n_gpu_layers=40,
    n_ctx=32768
)

# Call LLM
response = model.create_chat_completion(
    messages=[
        {
            'role':'system',
            'content':'You are a statistician with over 20 years of experience. Your role will be to interpret incoming data and explain key insights from the same.'
         },
        {
            'role':'user',
            'content':f'Review the data from {ctis()} and generate key insights that can help DP World plan, design and structure the Bharat Mart Facility that they are planning to build in Jebel Ali.'
        }
    ],
    stream=True,
    temperature=0.2,
    top_p=0.2,
    max_tokens=2048
)

# Display LLM output
for chunk in response:
    if 'choices' in chunk and 'delta' in chunk['choices'][0]:
        output = chunk['choices'][0]['delta'].get('content', ' ')
        print(output, flush=True, end='')