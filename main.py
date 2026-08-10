from scrapers import canada, eures
from filters import is_relevant
from storage import init_db, is_new, mark_seen
from notifier import send_digest


def run():
    init_db()

    all_jobs = []
    print("Fetching Canada listings...")
    all_jobs += canada.fetch_jobs()

    print("Fetching Germany/Netherlands/Romania listings (EURES)...")
    all_jobs += eures.fetch_jobs()

    print(f"Total raw listings pulled: {len(all_jobs)}")

    relevant = [
        job for job in all_jobs
        if is_relevant(job["title"], job.get("description", ""))
    ]
    print(f"Relevant after keyword filter: {len(relevant)}")

    new_jobs = [job for job in relevant if is_new(job["job_id"])]
    print(f"New (not sent before): {len(new_jobs)}")

    for job in new_jobs:
        mark_seen(job)

    send_digest(new_jobs)


if __name__ == "__main__":
    run()
