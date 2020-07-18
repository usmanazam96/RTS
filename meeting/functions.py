from datetime import datetime, date, timedelta


def get_today():
    return datetime.today().weekday() + 1


def get_weekday_from_date(t_date):
    return t_date.weekday() + 1


def add_time(t_time, t_min):
    r_time = datetime.combine(date.today(), t_time)
    r_time = r_time + timedelta(0, t_min * 60)
    return r_time.time()


def is_future_date(t_date, t_days):
    f_date = datetime.now() + timedelta(days=t_days)
    if t_date < f_date.date():
        return False
    return True
