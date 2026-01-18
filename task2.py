def count_valid_emails(emails):
    count = 0

    for email in emails:
        if "@" in email:
            count += 1

    return count


emails = [
    "getinet@gmail.com",
    "bosena@gmail.com",
    "asbakdbkbs@kbfkdbv@sds.com"
]

print(count_valid_emails(emails))