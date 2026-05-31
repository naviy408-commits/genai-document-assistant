import re
import json
from langchain_community.llms import Ollama


OLLAMA_MODEL = "tinyllama"

FINANCIAL_PATTERNS = {
    "Revenue":          r"(?:total\s+)?(?:net\s+)?revenue[s]?\s*[\$:]?\s*([\$\d,\.]+\s*(?:billion|million|B|M)?)",
    "Net Income":       r"net\s+income\s*[\$:]?\s*([\$\d,\.]+\s*(?:billion|million|B|M)?)",
    "EPS":              r"(?:diluted\s+)?(?:earnings|EPS)\s+per\s+share\s*[\$:]?\s*([\$\d,\.]+)",
    "Total Assets":     r"total\s+assets\s*[\$:]?\s*([\$\d,\.]+\s*(?:billion|trillion|B|T)?)",
    "Operating Margin": r"operating\s+(?:income\s+)?margin\s*:?\s*([\d,\.]+\s*%)",
    "Return on Equity": r"(?:return\s+on\s+equity|ROE)\s*:?\s*([\d,\.]+\s*%)",
}

HEALTHCARE_PATTERNS = {
    "Readmission Rate":     r"(?:30-day\s+)?readmission\s+rate\s*:?\s*([\d,\.]+\s*%)",
    "Mortality Rate":       r"mortality\s+rate\s*:?\s*([\d,\.]+\s*%)",
    "Patient Satisfaction": r"(?:patient\s+)?satisfaction\s+(?:score\s+)?:?\s*([\d,\.]+\s*(?:%|out of \d+)?)",
    "Compliance Rate":      r"compliance\s+rate\s*:?\s*([\d,\.]+\s*%)",
    "Infection Rate":       r"(?:hospital-acquired\s+)?infection\s+rate\s*:?\s*([\d,\.]+\s*%)",
    "Vaccination Rate":     r"vaccination\s+(?:coverage\s+)?rate\s*:?\s*([\d,\.]+\s*%)",
}

FINANCIAL_KPI_PROMPT = """Extract KPIs from the text. Return ONLY a JSON object, nothing else.
Use this exact format:
{{"revenue": "value or null", "net_income": "value or null", "eps": "value or null", "total_assets": "value or null", "operating_margin": "value or null", "return_on_equity": "value or null", "year": "value or null"}}

Text: {text}

JSON:"""

HEALTHCARE_KPI_PROMPT = """Extract KPIs from the text. Return ONLY a JSON object, nothing else.
Use this exact format:
{{"readmission_rate": "value or null", "mortality_rate": "value or null", "patient_satisfaction": "value or null", "compliance_rate": "value or null", "infection_rate": "value or null", "vaccination_rate": "value or null"}}

Text: {text}

JSON:"""


def extract_with_regex(text, patterns):
    results = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        results[key] = match.group(1).strip() if match else None
    return results


def extract_with_llm(text, prompt_template):
    llm = Ollama(model=OLLAMA_MODEL, temperature=0)
    prompt = prompt_template.format(text=text[:2000])
    try:
        response = llm.invoke(prompt)
        # Clean response — remove markdown, extra text
        clean = re.sub(r"```(?:json)?|```", "", response).strip()
        # Find JSON object in response
        match = re.search(r'\{.*\}', clean, re.DOTALL)
        if match:
            parsed = json.loads(match.group())
            # Make sure it's a dict not a list
            if isinstance(parsed, dict):
                return parsed
        return {}
    except Exception as e:
        print(f"LLM extraction error: {e}")
        return {}


def extract_financial_kpis(full_text):
    # First try regex — fast and reliable
    results = extract_with_regex(full_text, FINANCIAL_PATTERNS)
    missing = sum(1 for v in results.values() if v is None)

    # Only call LLM if regex missed most fields
    if missing >= 3:
        llm_results = extract_with_llm(full_text, FINANCIAL_KPI_PROMPT)
        if isinstance(llm_results, dict):
            for key, val in llm_results.items():
                display_key = key.replace("_", " ").title()
                if display_key not in results or results[display_key] is None:
                    results[display_key] = val if val != "null" else None
    return results


def extract_healthcare_kpis(full_text):
    results = extract_with_regex(full_text, HEALTHCARE_PATTERNS)
    missing = sum(1 for v in results.values() if v is None)

    if missing >= 3:
        llm_results = extract_with_llm(full_text, HEALTHCARE_KPI_PROMPT)
        if isinstance(llm_results, dict):
            for key, val in llm_results.items():
                display_key = key.replace("_", " ").title()
                if display_key not in results or results[display_key] is None:
                    results[display_key] = val if val != "null" else None
    return results


def generate_summary(full_text):
    llm = Ollama(model=OLLAMA_MODEL, temperature=0.3)
    prompt = f"""Write a 3-paragraph executive summary:
Paragraph 1: What is this document and who published it?
Paragraph 2: Key findings and data points?
Paragraph 3: Important conclusions or recommendations?

Document:
{full_text[:2000]}

Summary:"""
    return llm.invoke(prompt)