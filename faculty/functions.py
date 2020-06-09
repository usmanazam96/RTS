from datetime import datetime, date


def get_time_diff(end_time, start_time):
    delta = datetime.combine(date.today(), end_time) - datetime.combine(date.today(), start_time)
    delta_minutes = (delta.days * 24 * 60 + delta.seconds) / 60
    if delta.days < 0:
        delta_minutes *= -1
    return delta_minutes
