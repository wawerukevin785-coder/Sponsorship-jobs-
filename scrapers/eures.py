import requests
from bs4 import BeautifulSoup
from config import SKILL_KEYWORDS

BASE_URL = "https://europa.eu/eures/portal/jv-se/search"

COUNTRY_CODES = {
    "germany": "DE",
    "netherlands": "NL",
    "romania": "RO",
}


def fetch_jobs():
    jobs = []
    for country_name, country_code in COUNTRY_CODES.items():
        for keyword in SKILL_KEYWORDS:
            params = {
                "page": 1,
                "keywordType": "essential",
                "keyword": keyword,
                "countryCode": country_code,
            }
            try:
                resp = requests.get(BASE_URL, params=params, timeout=15,
                                     headers={"User-Agent": "Mozilla/5.0"})
                resp.raise_for_status()
            except requests.RequestException as e:
                print(f"[eures] request failed for {country_name}/{keyword}: {e}")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            listings = soup.select("div.jv-result-item")

            for item in listings:
                title_el = item.select_one("a.jv-title")
                company_el = item.select_one("span.jv-employer")

                if not title_el:
                    continue

                job_url = title_el.get("href", "")
                jobs.append({
                    "job_id": f"eures:{country_code}:{job_url}",
                    "title": title_el.get_text(strip=True),
                    "company": company_el.get_text(strip=True) if company_el else "Unknown",
                    "country": country_name.capitalize(),
                    "url": job_url if job_url.startswith("http") else f"https://europa.eu{job_url}",
                    "description": item.get_text(" ", strip=True),
                })

    return jobs
