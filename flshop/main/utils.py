import os
from telegram import Bot
from django.conf import settings


def send_order_notification_to_telegram(orders):
    token = os.environ.get('TELEGRAM_BOT_TOKEN')  # Убедитесь, что у вас есть токен бота
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')  # Убедитесь, что у вас есть идентификатор чата
    bot = Bot(token=token)

    message_text = ""
    total_price = 0
    for order in orders:
        message_text += f"{order.flower.name} - {order.quantity}\n"
        total_price += order.flower.price * order.quantity

    message_text += f"\nTotal Price: {total_price:.2f}"
    message_text += f"\nDelivery Date & Time: {order.delivery_date_time}"
    message_text += f"\nAddress: {order.address}"
    message_text += f"\nComment: {order.comment}"

    bot.send_message(chat_id=chat_id, text=message_text)