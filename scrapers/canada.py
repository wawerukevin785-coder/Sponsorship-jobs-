import requests
from bs4 import BeautifulSoup
from config import SKILL_KEYWORDS

BASE_URL = "https://www.jobbank.gc.ca/jobsearch/jobsearch"


def fetch_jobs():
    jobs = []
    for keyword in SKILL_KEYWORDS:
        params = {
            "searchstring": keyword,
            "locationstring": "Canada",
            "sort": "M",
        }
        try:
            resp = requests.get(BASE_URL, params=params, timeout=15,
                                 headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[canada] request failed for '{keyword}': {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        listings = soup.select("article.resultJobItem")

        for item in listings:
            title_el = item.select_one("span.noctitle")
            company_el = item.select_one("li.business")
            link_el = item.select_one("a")

            if not (title_el and link_el):
                continue

            job_url = "https://www.jobbank.gc.ca" + link_el.get("href", "")
            job_id = link_el.get("href", "")

            jobs.append({
                "job_id": f"canada:{job_id}",
                "title": title_el.get_text(strip=True),
                "company": company_el.get_text(strip=True) if company_el else "Unknown",
                "country": "Canada",
                "url": job_url,
                "description": item.get_text(" ", strip=True),
            })

    return jobs
