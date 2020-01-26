# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import wbbot.handlers.actions as actions
import wbbot.handlers.commands as commands
import wbbot.handlers.messages as messages
import common.env as env
import wbbot.misc.jobs as jobs
import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

updater = Updater(env.BOT_TOKEN, use_context=True)
job_queue = updater.job_queue
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('ping', commands.command_ping))
dispatcher.add_handler(CommandHandler(['start', 'help'], commands.command_start))
dispatcher.add_handler(CommandHandler('list', commands.command_list))
dispatcher.add_handler(CommandHandler('search', commands.command_search))
dispatcher.add_handler(CommandHandler('brands', commands.command_brands))

dispatcher.add_handler(MessageHandler(Filters.reply, messages.message_search))
dispatcher.add_handler(MessageHandler(Filters.regex(env.PRODUCT_REGEXP), messages.message_add_product))

dispatcher.add_handler(CallbackQueryHandler(actions.inline_callback))

job_queue.run_repeating(jobs.check_prices, env.NOTIFY_INTERVAL, 1)

updater.start_polling()
updater.idle()
