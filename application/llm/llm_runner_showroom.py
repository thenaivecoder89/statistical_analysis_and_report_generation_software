from openai import OpenAI
from application.analytics_engines.showroom_cleanser_analysis import histogram_showroom as hs
from application.analytics_engines.showroom_cleanser_analysis import kde_showroom as ks
import os
from dotenv import load_dotenv
import json
import io

# Initialize environment
load_dotenv()
key = os.getenv('key')

# Initialize LLM
client = OpenAI(api_key=key)

# Histogram dataset for llm
showroom_hist_describe, hist_showroom, fig_showroom = hs(show_plot=False)
data_desc_dataset = showroom_hist_describe
data_hist_dataset = hist_showroom

# KDE dataset for llm
data_kde_showroom, fig_kde_showroom = ks(show_plot=False)
data_kde_dataset = data_kde_showroom

# Call LLM for showroom analysis - histogram
def llm_showroom_histogram():
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
                            data_description: {data_desc_dataset}
                            data_set: {data_hist_dataset}

                            Review the above and generate key insights that can help DP World plan, design, and structure the Bharat Mart facility being developed in Jebel Ali.

                            Output JSON with the following structure:
                            {{
                                "summary:": "three paragraph overview with paragraph 1 focussed on insights on the data statistics, paragraph 2 focussed on insights from the data set and paragraph 3 focussed on recommendations for Bharat Mart.",
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
    # Convert plot to BytesIO for API
    buf = io.BytesIO()
    fig_showroom.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return output, buf

# Call LLM for showroom analysis - histogram
def llm_showroom_kde():
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
                            data_set: {data_kde_dataset}

                            Review the above and generate key insights that can help DP World plan, design, and structure the Bharat Mart facility being developed in Jebel Ali.

                            Output JSON with the following structure:
                            {{
                                "summary:": "three paragraph overview with paragraph 1 focussed on insights on the data statistics, paragraph 2 focussed on insights from the data set and paragraph 3 focussed on recommendations for Bharat Mart.",
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
    # Convert plot to BytesIO for API
    buf = io.BytesIO()
    fig_showroom.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return output, buf