from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from apiRequests import getUser
from classes import User
from config import TELEGRAM_API_KEY


# Стартовая функция для всех пользователей
def start(update: Update, context: CallbackContext):
    user = update.message.from_user.username
    
    me = getUser(username=user.username)

    if me.isOrg:
        # Сообщение для организаторов
        keyboard = [
            [InlineKeyboardButton('Налоги', callback_data='taxes'),
             InlineKeyboardButton('Перевод', callback_data='transfer_admin'),
             InlineKeyboardButton('Просмотр баланса участника', callback_data='check_balance_participant')],
            [InlineKeyboardButton('Список должников', callback_data='debtors_list'),
             InlineKeyboardButton('История', callback_data='history_admin'),
             InlineKeyboardButton('Поиск транзакции', callback_data='search_transaction')],
            [InlineKeyboardButton('Кредиты', callback_data='credits')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'Привет, биоробот! Успехов тебе на день<3',
            reply_markup=reply_markup
        )
    else:
        # Сообщение для обычных пользователей
        keyboard = [
            [InlineKeyboardButton('Перевод', callback_data='transfer'),
             InlineKeyboardButton('История', callback_data='history'),
             InlineKeyboardButton('Оформить кредит', callback_data='credit')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'Вас приветствует банк планеты завтра.\nСледующий налог будет {{date, time, sum}}\nВаш баланс: {{balance}}',
            reply_markup=reply_markup
        )

# Обработка нажатия на кнопки для участников
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user = update.effective_user.username
    
    if data == 'transfer':
        query.edit_message_text(text="Введите username того, кому вы хотите перевести")
        context.user_data['action'] = 'transfer_username'
    elif data == 'history':
        query.edit_message_text(text="Ваша история")
        # Здесь нужно добавить логику для чтения истории из базы данных
    elif data == 'credit':
        query.edit_message_text(text="На какую сумму хотите оформить кредит?")
        context.user_data['action'] = 'apply_credit_amount'

# Обработка сообщений от участников
def message_handler(update: Update, context: CallbackContext):
    user = update.effective_user.username
    text = update.message.text
    
    action = context.user_data.get('action')
    
    if action == 'transfer_username':
        recipient = text
        if not check_role(recipient):
            update.message.reply_text("Ошибка: такого пользователя нет.")
        else:
            update.message.reply_text("Введите сумму перевода")
            context.user_data['recipient'] = recipient
            context.user_data['action'] = 'transfer_amount'
    elif action == 'transfer_amount':
        amount = float(text)
        balance = get_balance(user)  # Здесь должна быть логика получения текущего баланса
        if amount > balance:
            update.message.reply_text("У вас недостаточно средств.")
        else:
            transfer_money(user, context.user_data['recipient'], amount)  # Логика перевода денег
            update.message.reply_text("Перевод выполнен.")
    elif action == 'apply_credit_amount':
        credit_amount = float(text)
        update.message.reply_text("Для чего вам нужен кредит?")
        context.user_data['action'] = 'apply_credit_reason'
        context.user_data['credit_amount'] = credit_amount
    elif action == 'apply_credit_reason':
        reason = text
        apply_for_credit(user, context.user_data['credit_amount'], reason)  # Логика оформления кредита
        update.message.reply_text("Ожидайте рассмотрения вашей заявки.")

# Логика для организатора
def admin_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    
    if data == 'taxes':
        query.edit_message_text(text="test_я в рот ебла пока не ебу как все подключить")
    elif data == 'transfer_admin':
        query.edit_message_text(text="test_я в рот ебла пока не ебу как все подключить")
    elif data == 'check_balance_participant':
        query.edit_message_text(text="test_я в рот ебла пока не ебу как все подключить")
    elif data == 'debtors_list':
        query.edit_message_text(text="test_я в рот ебла пока не ебу как все подключить")
    elif data == 'history_admin':
        query.edit_message_text(text="test_я в рот ебла пока не ебу как все подключить")
    elif data == 'search_transaction':
        query.edit_message_text(text="test_я в рот ебла пока не ебу как все подключить")
    elif data == 'credits':
        query.edit_message_text(text="test_я в рот ебла пока не ебу как все подключить")

def main():
    updater = Updater(token=TELEGRAM_API_KEY, use_context=True)
    
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))
    dp.add_handler(CallbackQueryHandler(admin_button_handler, pattern='^taxes$|^transfer_admin$|^check_balance_participant$|^debtors_list$|^history_admin$|^search_transaction$|^credits$'))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()