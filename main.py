import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from config_reader import config
data = pd.read_excel(config.dstTable, sheet_name = config.shtName)
datesColumn = config.datesColumn

def send_msg(text):
   import requests
   url_req = "https://api.telegram.org/bot" + config.BOT_TOKEN + "/sendMessage?chat_id=" + config.tgId + "&text=" + text
   results = requests.get(url_req)
   print(results.json())

for idx, x in enumerate(data[datesColumn]):
    deadline = x - datetime.now()
    if deadline <= timedelta(days=config.daysLeft):
        deadKeyName = data[config.namesColumn].loc[idx]
        deadTime = deadline.days
        # Если дней осталось 0, то высчитываем сколько осталось часов
        if deadTime == 0:
            deadTime = str(deadline.seconds/3600).partition('.')[0]
            send_msg("🔥 ВНИМАНИЕ\nВыходит срок: %s\nОсталось: %s ч.\nСрок: %s" % (str(deadKeyName), str(deadTime), str(x.strftime("%d.%m.%Y"))))
        else:
            send_msg("🔥 ВНИМАНИЕ\nВыходит срок: %s\nОсталось: %s дн.\nСрок: %s" % (str(deadKeyName), str(deadTime), str(x.strftime("%d.%m.%Y"))))