from shop.models import Shoot, Message
from datetime import datetime, timedelta

def shoot_data():
    start_date = datetime.now()
    end_date = start_date - timedelta(days=7)
    week_shoots = len(list(Shoot.objects.filter(date__range=[start_date, end_date], booked=True, complete=True)))
    end_date = start_date - timedelta(days=30)
    month_shoots = len(list(Shoot.objects.filter(date__range=[start_date, end_date], booked=True, complete=True)))
    pending_shoots = len(list(Shoot.objects.filter(booked=True, complete=False)))
    all_shoots = len(list(Shoot.objects.all()))

    return {
        'week_shoots': week_shoots,
        'month_shoots': month_shoots,
        'pending_shoots': pending_shoots,
        'all_shoots': all_shoots
    }

    
def message_data():
    unread_messages = len(list(Message.objects.filter(read=False)))
    all_messages = len(list(Message.objects.all()))

    return {
        'unread_messages': unread_messages,
        'all_messages': all_messages
    }