import json
from yookassa import Configuration, Payment

from data.config import SHOP_ID, SECRET_KEY
from loader import dp
from utils.db_api.db_commands import update_payment, get_payments, get_rate_by_id, get_client_by_id, start_subscribe, \
    update_notify_sub, delete_payments, update_amount_req

Configuration.account_id = SHOP_ID
Configuration.secret_key = SECRET_KEY


async def create_payment(amount, telegram_id, rate_id):
    payment = Payment.create({
        "amount": {
            "value": int(amount),
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/TGstat_parsing_bot"
        },
        "capture": True,
        "description": 'Приобретение подписки'
    })

    payment_data = json.loads(payment.json())
    payment_id = payment_data['id']
    payment_url = (payment_data['confirmation'])['confirmation_url']
    await update_payment(rate_id=rate_id, telegram_id=telegram_id, payment_id=payment_id)
    return payment_url


async def check_payment():
    payments = await get_payments()

    for i in range(len(payments)):
        payment = json.loads((Payment.find_one(payments[i].payment_id)).json())
        if payment['status'] == 'succeeded':
            if payments[i].amount is None:
                client = await get_client_by_id(payments[i].client)
                rate = await get_rate_by_id(payments[i].rate)

                await start_subscribe(telegram_id=client.telegram_id, amount=rate.amount)
                await update_notify_sub(telegram_id=client.telegram_id)

                await dp.bot.send_message(
                    chat_id=client.telegram_id,
                    text=f'✅ Подписка на {rate.title} успешно приобретена!\n'
                         f'Количество запросов обновлено до {rate.amount}\n\n'
                         f'Я напомню вам об окончании вашей подписки за два дня.')
                await delete_payments(client.id)
            else:
                client = await get_client_by_id(payments[i].client)

                old_amount = await update_amount_req(payments[i].client)

                await dp.bot.send_message(
                    chat_id=client.telegram_id,
                    text=f'✅ Оплата успешно проведена!\n'
                         f'К вашему количеству запросов прибавилось {payments[i].amount}\n'
                         f'Итоговое количество запросов: {old_amount + payments[i].amount}')

                await delete_payments(client.id)
        else:
            pass
