import json

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from common.models import ProductPrice
from common.session import session
from common.models import UserProduct


def get_product_card(product):
    card = f'🛍️ {product.header}\n\n'
    card += f'<b>{format_product_price(product)}</b>\n'

    if product.size_list:
        card += get_size_list(product)

    return card


def get_product_markup(user_id, product):
    user_product = session.query(UserProduct).filter_by(user_id=user_id, product_id=product.id).first()

    delete_button = InlineKeyboardButton(
        '❌ Удалить',
        callback_data=json.dumps({'action': 'delete_product', 'product_id': product.id})
    )
    price_button = InlineKeyboardButton(
        '📈 Цены',
        callback_data=json.dumps({'action': 'prices_history', 'product_id': product.id})
    )
    notify_button = InlineKeyboardButton(
        '🔕 Отключить уведомления' if user_product.settings.is_price_notify else '🔔 Включить уведомления',
        callback_data=json.dumps({'action': 'price_notify', 'product_id': product.id,
                                  'n': user_product.settings.is_price_notify})
    )

    return InlineKeyboardMarkup([[delete_button, price_button], [notify_button]])


def format_product_price(product):
    if not product.price or product.price.value is None:
        return '💰 нет данных'

    price_icon = get_price_icon(product.price.value, product.price.prev_value)
    price_value = ProductPrice.format_price_value(product.price.value, product.domain)

    return f'{price_icon} {price_value}'


def get_price_icon(current_value, prev_value):
    price_icon = '💰'

    if prev_value and current_value:
        if current_value < prev_value:
            price_icon = '🔻'
        if current_value > prev_value:
            price_icon = '🔺'

    return price_icon


def get_size_list(product):
    return '📏 <b>' + ', '.join(product.size_list) + '</b>\n' if product.size_list else ''

