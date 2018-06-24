import os, time, datetime, re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

token = os.environ['TELEGRAM_TOKEN']

def start(bot, update):
    update.message.reply_text("Hey! Got action items? Send them my way! Add me to a group with @ActionItemBot or send me your own personal list!\n\nUse _/ai [your action items, separated with periods]_\nTry _/ai@ActionItemBot [action items, separated with periods]_ when in groups.\n\nExamples:\n_\"/ai Get new action items. Do action items. Get more action items.\"\n\"/ai@ActionItemBot Buy twelve action items. Use nine action items. Sell 1 action item.\"_\n\nAction items remain until they're marked done. P.S. Check out my brother @AcknowledgedBot!",parse_mode=ParseMode.MARKDOWN) 

def new(bot, update):
    user = update.effective_user
    firstname = user['first_name']
    lastname = user['last_name']
    if firstname is None:
        name = lastname
    elif lastname is None:
        name = firstname
    else:
        name= firstname + ' ' + lastname[0]

    now=datetime.datetime.now()
    strnow = now.strftime("%A, %m/%d/%y")

    initialItems = ""
    itemCount = 0

    if ' ' not in update.message.text:
        return
    for idx, i in enumerate((update.message.text.split(" ",1)[1].split("."))):
        newItem = ""
        if(len(i) != 0):
            if(i[0].isspace()):
                if(len(i) > 1):
                    newItem = i[1:]
            else:
                newItem = i
            initialItems += '*(' + (str(idx+1)) + ') ' + newItem + '* by ' + name + '\n'
            itemCount+=1

    keyboard =[]
    for i in range(0,itemCount):
        keyboard.append([InlineKeyboardButton("Mark (" + (str(i+1))+") completed!" , callback_data=i+1)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(update.message.chat_id, "\nAction Items for " + strnow + "\n\n" + initialItems, reply_markup = reply_markup, parse_mode= ParseMode.MARKDOWN)

def button(bot, update):
    query = update.callback_query
    oglist = query.message.text_markdown
    user = query.from_user
    firstname = user['first_name']
    lastname = user['last_name']
    if firstname is None:
        name = lastname
    elif lastname is None:
        name = firstname
    else:
        name= firstname + ' ' + lastname[0]
    
    now=datetime.datetime.now()
    strnow = now.strftime("%I:%M%p")

    front = oglist.split('\n',2)
    firstpart = ''.join(front[0:2])

    numItems = 3
    indToDel = int(query.data)
    secondlist = front[2].split('\n')
    finishedTask = "-" +re.sub('\s?\(.*?\)', '', secondlist.pop(indToDel - 1)).replace(' ','',1)
    newCurrentList = []
    for idx, i in enumerate(secondlist):
        newind = '('+str(idx+1)+')'
        newCurrentList.append(re.sub('\s?\(.*?\)', newind ,i))
    newEnd = "\n".join(newCurrentList).rstrip() + "\n"
    finalText = newEnd.split('-----------------')[0]
    if(len(finalText.split('\n')) ==1):
        finalText = "Everything's done! Yay!\n"
    if(len(oglist.split('-----------------'))>1):
        finishedList = "\n" + (oglist.split('-----------------')[-1]).replace('\n','',1) + "\n"
    else:
        finishedList = "\n"

    new_text = firstpart + "\n\n" + finalText + '-----------------' + finishedList + finishedTask + '\nCompleted! ' + name + ' at ' + strnow

    itemCount = len(finalText.split('\n'))-1
    keyboard =[]
    if(finalText[0] != 'E'):
        for i in range(0,itemCount):
            keyboard.append([InlineKeyboardButton("Mark (" + (str(i+1))+") completed!" , callback_data=i+1)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.answer_callback_query(update.callback_query.id)
    bot.edit_message_text(reply_markup = reply_markup,chat_id=query.message.chat_id, message_id=query.message.message_id, text = new_text, parse_mode=ParseMode.MARKDOWN)

    
def error(bot, update, error):
    print(error)
    """Log Errors caused by Updates."""

def main():
    updater = Updater(token=token)

    updater.dispatcher.add_handler(CommandHandler('ai', new))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('new', start))
    updater.dispatcher.add_handler(CommandHandler('help', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
