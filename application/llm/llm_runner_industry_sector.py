from openai import OpenAI
from application.analytics_engines.industry_cleanser_analysis import cross_tabulation_industry_sector as ctis
from application.analytics_engines.industry_cleanser_analysis import dendogram_industry_sector as dis
from application.analytics_engines.industry_cleanser_analysis import cross_tabulation_industry_hs_code as ctihs
from application.analytics_engines.industry_cleanser_analysis import dendogram_industry_product as dip
import os
from dotenv import load_dotenv
import json

# Initialize environment
load_dotenv()
key = os.getenv('key')

# Initialize LLM
client = OpenAI(api_key=key)

# Cross-Tab dataset development - for llm
heat_industry_sector, p_industry_sector = ctis(show_plot=False)
heat_industry_product, p_industry_product = ctihs(show_plot=False)
data_ctis_dataset = json.dumps(heat_industry_sector.to_dict(), indent=2)
data_ctihs_dataset = json.dumps(heat_industry_product.to_dict(), indent=2)

# Dendo dataset development - for llm
dendo_industry_sector, p_dendo_industry_sector = dis(show_plot=False)
dendo_industry_product, p_dendo_industry_product = dip(show_plot=False)
data_dis_dataset = json.dumps(dendo_industry_sector.to_dict(), indent=2)
data_dip_dataset = json.dumps(dendo_industry_product.to_dict(), indent=2)

# Call LLM for industry and sector analysis - cross tabulation
# print(f'Industry and sector analysis:\n') # Comment this out before exposing on API
def llm_industry_sector_cross_tabulation():
    response = client.chat.completions.create(
        model='chatgpt-4o-latest',
        messages=[
            {
                'role': 'system',
                'content': """ You are a senior infrastructure planning and trade zone strategist with over 20 years of experience
                                in conceptualizing, designing, and scaling commercial trading hubs such as Bharat Mart (in Jebel Ali)
                                and Dragon Mart (in Dubai). Your expertise spans logistics, multi-sector tenant enablement,
                                warehousing, customs facilitation, and global trade compliance infrastructure.
                                You MUST respond as a valid JSON object only (no prose outside JSON)."""
            },
            {
                'role': 'user',
                'content': f"""
                            p_value: {p_industry_sector}
                            data_set: {data_ctis_dataset}

                            Review the above and generate key insights that can help DP World plan, design, and structure the Bharat Mart facility being developed in Jebel Ali.

                            Output JSON with the following structure:
                            {{
                                "summary:": "three paragraph overview with paragraph 1 focussed on insights on the statistical significance, paragraph 2 focussed on insights from the core data set and paragraph 3 focussed on recommendations for Bharat Mart.",
                                "insights": "bullet point based insights for each area of evaluation"
                            }}

                            Do not include any tables in your response.
                            """
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
    return output, ctis(show_plot=True)
    # print(output) #Comment this out before exposing on API.
    # ctis(show_plot=True) #Comment this out before exposing on API.
# print(llm_industry_sector_cross_tabulation()) #Comment this out before exposing on API.

# Call LLM for industry and hs codes analysis - cross tabulation
# print(f'Industry and product analysis:\n') #Comment this out before exposing on API.
def llm_industry_hs_codes_cross_tabulation():
    response = client.chat.completions.create(
        model='chatgpt-4o-latest',
        messages=[
            {
                'role':'system',
                'content':  """ You are a senior infrastructure planning and trade zone strategist with over 20 years of experience
                                in conceptualizing, designing, and scaling commercial trading hubs such as Bharat Mart (in Jebel Ali)
                                and Dragon Mart (in Dubai). Your expertise spans logistics, multi-sector tenant enablement,
                                warehousing, customs facilitation, and global trade compliance infrastructure.
                                You MUST respond as a valid JSON object only (no prose outside JSON)."""
             },
            {
                'role':'user',
                'content':f"""
                            p_value: {p_industry_product}
                            data_set: {data_ctihs_dataset}

                            Review the above and generate key insights that can help DP World plan, design, and structure the Bharat Mart facility being developed in Jebel Ali.

                            Output JSON with the following structure:
                            {{
                                "summary:": "three paragraph overview with paragraph 1 focussed on insights on the statistical significance, paragraph 2 focussed on insights from the core data set and paragraph 3 focussed on recommendations for Bharat Mart.",
                                "insights": "bullet point based insights for each area of evaluation"
                            }}

                            Do not include any tables in your response.
                            """
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
    return output, ctihs(show_plot=True)
    # print(output) #Comment this out before exposing on API.
    # ctihs(show_plot=True) #Comment this out before exposing on API.
# print(llm_industry_hs_codes_cross_tabulation()) #Comment this out before exposing on API.

# Call LLM for industry and sector analysis - dendogram
# print(f'Industry and sector analysis:\n')  # Comment this out before exposing on API
def llm_industry_sector_dendogram():
    response = client.chat.completions.create(
        model='chatgpt-4o-latest',
        messages=[
            {
                'role': 'system',
                'content': """ You are a senior infrastructure planning and trade zone strategist with over 20 years of experience 
                                in conceptualizing, designing, and scaling commercial trading hubs such as Bharat Mart (in Jebel Ali) 
                                and Dragon Mart (in Dubai). Your expertise spans logistics, multi-sector tenant enablement, 
                                warehousing, customs facilitation, and global trade compliance infrastructure.
                                You MUST respond as a valid JSON object only (no prose outside JSON)."""
            },
            {
                'role': 'user',
                'content': f"""
                            p_value: {p_dendo_industry_sector}
                            data_set: {data_dis_dataset}

                            Review the above and generate key insights that can help DP World plan, design, and structure the Bharat Mart facility being developed in Jebel Ali.

                            Output JSON with the following structure:
                            {{
                                "summary:": "three paragraph overview with paragraph 1 focussed on insights on the statistical significance; paragraph 2 focussed on insights from the core data set identifying dominant relationships, clusters, and outliers; and paragraph 3 focussed on recommendations for Bharat Mart.",
                                "insights": "bullet point based insights for each area of evaluation"
                            }}

                            Do not include any tables in your response.
                            """
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
    return output, dis(show_plot=True)
    # print(output) #Comment this out before exposing on API.
    # dis(show_plot=True) #Comment this out before exposing on API.
# print(llm_industry_sector_dendogram())  # Comment this out before exposing on API.

# Call LLM for industry and product analysis - dendogram
# print(f'Industry and product analysis:\n')  # Comment this out before exposing on API
def llm_industry_product_dendogram():
    response = client.chat.completions.create(
        model='chatgpt-4o-latest',
        messages=[
            {
                'role': 'system',
                'content': """ You are a senior infrastructure planning and trade zone strategist with over 20 years of experience 
                                in conceptualizing, designing, and scaling commercial trading hubs such as Bharat Mart (in Jebel Ali) 
                                and Dragon Mart (in Dubai). Your expertise spans logistics, multi-sector tenant enablement, 
                                warehousing, customs facilitation, and global trade compliance infrastructure.
                                You MUST respond as a valid JSON object only (no prose outside JSON)."""
            },
            {
                'role': 'user',
                'content': f"""
                            p_value: {p_dendo_industry_product}
                            data_set: {data_dip_dataset}

                            Review the above and generate key insights that can help DP World plan, design, and structure the Bharat Mart facility being developed in Jebel Ali.

                            Output JSON with the following structure:
                            {{
                                "summary:": "three paragraph overview with paragraph 1 focussed on insights on the statistical significance; paragraph 2 focussed on insights from the core data set identifying dominant relationships, clusters, and outliers; and paragraph 3 focussed on recommendations for Bharat Mart.",
                                "insights": "bullet point based insights for each area of evaluation"
                            }}

                            Do not include any tables in your response.
                            """
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
    return output, dip(show_plot=True)
    # print(output) #Comment this out before exposing on API.
    # dip(show_plot=True) #Comment this out before exposing on API.
# print(llm_industry_product_dendogram())  # Comment this out before exposing on API.