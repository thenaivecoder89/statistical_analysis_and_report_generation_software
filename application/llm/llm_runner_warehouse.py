from openai import OpenAI
from application.analytics_engines.warehouse_cleanser_analysis import histogram_warehouse_cbm as hs_cbm
from application.analytics_engines.warehouse_cleanser_analysis import histogram_warehouse_mt as hs_mt
from application.analytics_engines.warehouse_cleanser_analysis import kde_warehouse_cbm as ks_cbm
from application.analytics_engines.warehouse_cleanser_analysis import kde_warehouse_mt as ks_mt
import os
from dotenv import load_dotenv
import json
import io

# Initialize environment
load_dotenv()
key = os.getenv('key')

# Initialize LLM
client = OpenAI(api_key=key)

# Histogram dataset for llm - cbm
warehouse_hist_describe_cbm, hist_warehouse_cbm, fig_warehouse_cbm = hs_cbm(show_plot=False)
data_desc_dataset_cbm = warehouse_hist_describe_cbm
data_hist_dataset_cbm = hist_warehouse_cbm

# Histogram dataset for llm - mt
warehouse_hist_describe_mt, hist_warehouse_mt, fig_warehouse_mt = hs_mt(show_plot=False)
data_desc_dataset_mt = warehouse_hist_describe_mt
data_hist_dataset_mt = hist_warehouse_mt

# KDE dataset for llm - cbm
data_kde_warehouse_cbm, fig_kde_warehouse_cbm = ks_cbm(show_plot=False)
data_kde_dataset_cbm = data_kde_warehouse_cbm

# KDE dataset for llm - mt
data_kde_warehouse_mt, fig_kde_warehouse_mt = ks_mt(show_plot=False)
data_kde_dataset_mt = data_kde_warehouse_mt

# Call LLM for warehouse analysis for CBM - histogram
def llm_warehouse_histogram_cbm():
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
                            data_description: {data_desc_dataset_cbm}
                            data_set: {data_hist_dataset_cbm}

                            The dataset above contains monthly trade volume data (in cbm) that needs to be analyzed to determine warehouse sizing for the Bharat Mart facility being developed in Jebel Ali. 
                            Review the above and generate key insights that can help DP World plan, design, and structure the Bharat Mart facility (with specific focus on warehouse sizes) being developed in Jebel Ali.

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
    fig_warehouse_cbm.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return output, buf

# Call LLM for warehouse analysis for MT - histogram
def llm_warehouse_histogram_mt():
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
                            data_description: {data_desc_dataset_mt}
                            data_set: {data_hist_dataset_mt}

                            The dataset above contains monthly trade volume data (in mt) that needs to be analyzed to determine warehouse sizing for the Bharat Mart facility being developed in Jebel Ali. 
                            Review the above and generate key insights that can help DP World plan, design, and structure the Bharat Mart facility (with specific focus on warehouse sizes) being developed in Jebel Ali.

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
    fig_warehouse_mt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return output, buf

# Call LLM for warehouse analysis for CBM - KDE
def llm_warehouse_kde_cbm():
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
                            data_set: {data_kde_dataset_cbm}

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
    fig_kde_warehouse_cbm.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return output, buf

# Call LLM for warehouse analysis for MT - KDE
def llm_warehouse_kde_mt():
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
                            data_set: {data_kde_dataset_mt}

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
    fig_kde_warehouse_mt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return output, buf