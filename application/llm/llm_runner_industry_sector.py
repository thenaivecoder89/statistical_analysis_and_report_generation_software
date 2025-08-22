from openai import OpenAI
from application.analytics_engines.industry_cleanser_analysis import cross_tabulation_industry_sector as ctis
from application.analytics_engines.industry_cleanser_analysis import cross_tabulation_industry_hs_code as ctihs
import os
from dotenv import load_dotenv
import json

# Initialize environment
load_dotenv()
key = os.getenv('key')

# Initialize LLM
client = OpenAI(api_key=key)

# Call LLM for industry and sector analysis - cross tabulation
def llm_industry_sector_cross_tabulation():
    response = client.chat.completions.create(
        model='chatgpt-4o-latest',
        messages=[
            {
                'role':'system',
                'content':'You are a statistician with over 20 years of experience. Your role will be to interpret incoming data and explain key insights from the same.'
                          'You MUST respond as a valid JSON object only (no prose outside JSON).'
             },
            {
                'role':'user',
                'content':f'Review the data from {ctis(show_plot=False)} and generate key insights that can help DP World plan, design and structure the Bharat Mart Facility that they are planning to build in Jebel Ali. '
                          'Output JSON with the following structure:'
                          '{'
                            '"summary:": "three paragraph overview with paragraphs 1 and 2 focussed on insights from the data and paragraph 3 focussed on recommendations for Bharat Mart.",'
                            '"insights": "bullet point based insights for each area of evaluation"'
                          '}'
                          'Do not include any tables in your response.'
            }
        ],
        temperature=0.2,
        top_p=0.2,
        max_tokens=2048,
        response_format={'type':'json_object'}
    )

    # Display LLM output
    content = response.choices[0].message.content
    j_load = json.loads(content)
    output = json.dumps(j_load, indent=2, ensure_ascii=False)
    print(output)
    ctis(show_plot=True)


# Call LLM for industry and hs codes analysis - cross tabulation
def llm_industry_hs_codes_cross_tabulation():
    response = client.chat.completions.create(
        model='chatgpt-4o-latest',
        messages=[
            {
                'role': 'system',
                'content': 'You are a statistician with over 20 years of experience. Your role will be to interpret incoming data and explain key insights from the same.'
                           'You MUST respond as a valid JSON object only (no prose outside JSON).'
            },
            {
                'role': 'user',
                'content': f'Review the data from {ctihs(show_plot=False)} and generate key insights that can help DP World plan, design and structure the Bharat Mart Facility that they are planning to build in Jebel Ali. '
                           'Output JSON with the following structure:'
                           '{'
                           '"summary:": "three paragraph overview with paragraphs 1 and 2 focussed on insights from the data and paragraph 3 focussed on recommendations for Bharat Mart.",'
                           '"insights": "bullet point based insights for each area of evaluation"'
                           '}'
                           'Do not include any tables in your response.'
            }
        ],
        temperature=0.2,
        top_p=0.2,
        max_tokens=2048,
        response_format={'type': 'json_object'}
    )

    # Display LLM output
    content = response.choices[0].message.content
    j_load = json.loads(content)
    output = json.dumps(j_load, indent=2, ensure_ascii=False)
    print(output)
    ctihs(show_plot=True)

print(f'Industry and sector analysis:\n{llm_industry_sector_cross_tabulation()}')
print(f'Industry and product analysis:\n{llm_industry_hs_codes_cross_tabulation()}')