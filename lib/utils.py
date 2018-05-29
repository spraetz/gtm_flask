import datetime


def days_later(days=0):
    return datetime.date.today() + datetime.timedelta(days=days)