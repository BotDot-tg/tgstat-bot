from datetime import datetime, timezone, timedelta

from loader import dp
from utils.db_api.db_commands import get_subscribers


async def check():
    clients = await get_subscribers()
    now_time = datetime.now(timezone.utc)
    for i in range(len(clients) - 1):
        client_telegram_id = clients[i].telegram_id

        alarm_date = clients[i].start_subscribe + timedelta(days=28)
        if alarm_date < now_time:
            await dp.bot.send_message(
                chat_id=client_telegram_id,
                text='До окончания вашей подписки осталось 2 дня.\n'
                     'Чтобы её обновить, перейдите в меню подписки.'
            )

        if clients[i].start_subscribe == clients[i].end_subscribe and clients[i].is_notificated:
            await dp.bot.send_message(
                chat_id=client_telegram_id,
                text='К сожалению, ваша подписка истекла.\n'
                     'Возобновить ее вы можете в меню подписки.'
            )
