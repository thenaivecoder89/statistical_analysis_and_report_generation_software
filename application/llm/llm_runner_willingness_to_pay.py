from openai import OpenAI
from application.analytics_engines.willingness_to_pay_cleanser_analysis import scatter_plot_willingness_to_pay as spw
from application.analytics_engines.willingness_to_pay_cleanser_analysis import box_plot_willingness_to_pay as bpw
import os
from dotenv import load_dotenv
import json
import io

# Initialize environment
load_dotenv()
key = os.getenv('key')

# Initialize LLM
client = OpenAI(api_key=key)

# Scatterplot dataset for llm
wtp_sp_desc, wtp_sp_correl, wtp_sp_fig = spw(show_plot=False)

# Boxplot dataset for llm
wtp_bp_desc, wtp_bp_fig = bpw(show_plot=False)

# Call LLM for scatterplot analysis
def llm_willingness_scatterplot():
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
                            data_set: {wtp_sp_desc}
                            data_correlation: {wtp_sp_correl}

                            Review the above and generate key insights that can help DP World plan, design, and structure the Bharat Mart facility being developed in Jebel Ali.

                            Output JSON with the following structure:
                            {{
                                "summary:": "three paragraph overview with paragraph 1 focussed on insights on the data correlation, paragraph 2 focussed on insights from the data set and paragraph 3 focussed on recommendations for Bharat Mart.",
                                "insights": "bullet point based insights for each area of evaluation in the following format:
                                            {"statistical_insights":"bullet point based insights on the statistical significance provided in paragraph 1 above."}
                                            {"core_data_set_insights":"bullet point based insights on the content generated in paragraph 2 above."}
                                            {"recommendations_for_bharat_mart":"bullet point based insights on the content generated in paragraph 3 above."}"
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
    wtp_sp_fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return output, buf

# Call LLM for boxplot analysis
def llm_willingness_boxplot():
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
                            data_set: {wtp_bp_desc}

                            Review the above and generate key insights that can help DP World plan, design, and structure the Bharat Mart facility being developed in Jebel Ali.

                            Output JSON with the following structure:
                            {{
                                "summary:": "three paragraph overview with paragraph 1 focussed on insights on the data correlation, paragraph 2 focussed on insights from the data set and paragraph 3 focussed on recommendations for Bharat Mart.",
                                "insights": "bullet point based insights for each area of evaluation in the following format:
                                            {"statistical_insights":"bullet point based insights on the statistical significance provided in paragraph 1 above."}
                                            {"core_data_set_insights":"bullet point based insights on the content generated in paragraph 2 above."}
                                            {"recommendations_for_bharat_mart":"bullet point based insights on the content generated in paragraph 3 above."}"
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
    wtp_bp_fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return output, buf