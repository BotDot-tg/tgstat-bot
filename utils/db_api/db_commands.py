import datetime

from asgiref.sync import sync_to_async

from admin_panel.telebot.models import Clients, ClientRequest, Rate, Payments


@sync_to_async()
def create_client(telegram_id, username):
    return Clients.objects.get_or_create(telegram_id=telegram_id, username=username)


@sync_to_async()
def get_client(telegram_id):
    return Clients.objects.filter(telegram_id=telegram_id).first()


@sync_to_async()
def get_client_by_id(client_id):
    return Clients.objects.filter(id=client_id).first()


@sync_to_async()
def update_is_trial(telegram_id):
    Clients.objects.filter(telegram_id=telegram_id).update(is_trial=True)


@sync_to_async()
def create_row(telegram_id, channel_name, count, link):
    client = Clients.objects.filter(telegram_id=telegram_id).first()

    ClientRequest.objects.get_or_create(client=client, channel_name=channel_name, count=count, link=link)


@sync_to_async()
def get_links(telegram_id):
    client = Clients.objects.filter(telegram_id=telegram_id).first()

    return ClientRequest.objects.filter(client=client).values_list('link', flat=True)


@sync_to_async()
def add_err(telegram_id, link, err, err_24):
    client = Clients.objects.filter(telegram_id=telegram_id).first()

    ClientRequest.objects.filter(client=client, link=link).update(ERR=err, ERR24=err_24)


@sync_to_async()
def add_citate(citate_amount, citate_percent, link, telegram_id):
    client = Clients.objects.filter(telegram_id=telegram_id).first()

    ClientRequest.objects.filter(client=client, link=link).update(citate_amount=citate_amount,
                                                                  citate_percent=citate_percent)


@sync_to_async()
def get_info(telegram_id):
    client = Clients.objects.filter(telegram_id=telegram_id).first()

    names = ClientRequest.objects.filter(client=client).values_list('channel_name', flat=True)
    count = ClientRequest.objects.filter(client=client).values_list('count', flat=True)
    links = ClientRequest.objects.filter(client=client).values_list('link', flat=True)
    ERR = ClientRequest.objects.filter(client=client).values_list('ERR', flat=True)
    ERR_24 = ClientRequest.objects.filter(client=client).values_list('ERR24', flat=True)
    citate_amount = ClientRequest.objects.filter(client=client).values_list('citate_amount', flat=True)
    citate_percent = ClientRequest.objects.filter(client=client).values_list('citate_percent', flat=True)

    return [names, count, links, ERR, ERR_24, citate_amount, citate_percent]


@sync_to_async()
def delete_info(telegram_id):
    client = Clients.objects.filter(telegram_id=telegram_id).first()

    ClientRequest.objects.filter(client=client).delete()


@sync_to_async()
def get_rate():
    return Rate.objects.all()


@sync_to_async()
def get_rate_by_id(rate_id):
    return Rate.objects.filter(pk=int(rate_id)).first()


@sync_to_async()
def get_client_request(telegram_id):
    return ClientRequest.objects.filter(client__telegram_id=telegram_id).values_list('client', flat=True)


@sync_to_async()
def start_subscribe(telegram_id, amount):
    start_time = datetime.datetime.now(datetime.timezone.utc)

    end_time = start_time + datetime.timedelta(days=30)

    Clients.objects.filter(telegram_id=telegram_id).update(subscribe=True, start_subscribe=start_time,
                                                           end_subscribe=end_time, amount=amount)


@sync_to_async()
def get_subscribers():
    return Clients.objects.filter(subscribe=True).all()


@sync_to_async()
def update_notify(telegram_id):
    Clients.objects.filter(telegram_id=telegram_id).update(is_notificated=True)


@sync_to_async()
def update_notify_sub(telegram_id):
    Clients.objects.filter(telegram_id=telegram_id).update(is_notificated=False)


@sync_to_async()
def get_count_subscribers():
    return Clients.objects.filter(subscribe=True).count()


@sync_to_async()
def update_amount_client(telegram_id):
    old_amount = Clients.objects.filter(telegram_id=telegram_id).first().amount

    Clients.objects.filter(telegram_id=telegram_id).update(amount=old_amount - 1)


@sync_to_async()
def bought_amount(telegram_id, amount):
    old_amount = Clients.objects.filter(telegram_id=telegram_id).first().amount

    Clients.objects.filter(telegram_id=telegram_id).update(amount=old_amount + amount)

    return Clients.objects.filter(telegram_id=telegram_id).first().amount


@sync_to_async()
def get_admins():
    return Clients.objects.filter(is_admin=True).values_list('telegram_id', flat=True)


@sync_to_async()
def search_by_username(username):
    return Clients.objects.filter(username=username).first()


@sync_to_async()
def add_del_admin(username, state):
    Clients.objects.filter(username=username).update(is_admin=state)


@sync_to_async()
def update_sub_god(username, state):
    start_time = datetime.datetime.now(datetime.timezone.utc)

    end_time = start_time + datetime.timedelta(days=9000)
    if state is True:
        Clients.objects.filter(username=username).update(subscribe=state, start_subscribe=start_time,
                                                         end_subscribe=end_time)
    else:
        Clients.objects.filter(username=username).update(subscribe=state)


@sync_to_async()
def update_rate(item, text, rate_id):
    if item == 'title':
        Rate.objects.filter(id=rate_id).update(title=text)
    elif item == 'desc':
        Rate.objects.filter(id=rate_id).update(description=text)
    elif item == 'req':
        Rate.objects.filter(id=rate_id).update(amount=int(text))
    elif item == 'price':
        Rate.objects.filter(id=rate_id).update(price=int(text))


@sync_to_async()
def update_payment(telegram_id, rate_id, payment_id):
    client = Clients.objects.filter(telegram_id=telegram_id).first().id
    Payments.objects.filter(client=client).update(rate=rate_id, payment_id=payment_id)


@sync_to_async()
def get_payments():
    return Payments.objects.all()


@sync_to_async()
def delete_payments(client):
    Payments.objects.filter(client=client).delete()


@sync_to_async()
def update_amount_req(client, amount):
    old_amount = Clients.objects.filter(id=client).first().amount
    Clients.objects.filter(id=client).update(amount=old_amount + amount)

    return old_amount


@sync_to_async()
def create_req_payment(telegram_id, amount):
    client = Clients.objects.filter(telegram_id=telegram_id).first().id
    Payments.objects.get_or_create(client=client, amount=amount)

@sync_to_async()
def create_payment_db(telegram_id):
    client = Clients.objects.filter(telegram_id=telegram_id).first().id
    Payments.objects.get_or_create(client=client)
