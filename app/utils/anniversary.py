from datetime import timedelta

def generate_anniversary_dates(wedding_date):
    return [
        {"year": 1, "date": wedding_date + timedelta(days=365)},
        {"year": 5, "date": wedding_date + timedelta(days=365 * 5)},
        {"year": 10, "date": wedding_date + timedelta(days=365 * 10)},
    ]