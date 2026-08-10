from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_FROM,
    MY_WHATSAPP_NUMBER,
)


def send_digest(jobs: list):
    if not jobs:
        print("No new jobs today - nothing sent.")
        return

    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN):
        print("Twilio credentials missing - printing digest instead:")
        _print_digest(jobs)
        return

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    chunk_size = 5
    for i in range(0, len(jobs), chunk_size):
        chunk = jobs[i:i + chunk_size]
        body = _format_message(chunk, batch_number=i // chunk_size + 1)
        client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=MY_WHATSAPP_NUMBER,
            body=body,
        )
        print(f"Sent batch {i // chunk_size + 1} ({len(chunk)} jobs)")


def _format_message(jobs: list, batch_number: int) -> str:
    lines = [f"*New sponsorship jobs - batch {batch_number}*\n"]
    for j in jobs:
        lines.append(
            f"*{j['title']}* - {j['company']} ({j['country']})\n{j['url']}\n"
        )
    return "\n".join(lines)


def _print_digest(jobs: list):
    for j in jobs:
        print(f"- {j['title']} | {j['company']} | {j['country']} | {j['url']}")
