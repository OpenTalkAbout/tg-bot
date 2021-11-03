import re


food_pizza = 0


def pizza(update, context):
    global food_pizza
    
    if ((update.message.text.lower().find("пицц") >= 0)
            and ((update.message.text.lower().find("хо") >= 0)
                 or (update.message.text.lower().find("дай") >= 0))):

        switcher = {
            0: 'Нет',
            1: 'Иди в магазин',
            2: 'Сходи в магазин',
            3: 'АЛЛО',
            4: 'СХОДИ В МАГАЗИН',
            5: 'Закажите уже ему пиццу',
            6: 'Ой все',
        }

        if (food_pizza == 6):
            food_pizza = 0
        else:
            food_pizza += 1

        update.message.reply_text(switcher.get(food_pizza, ""))


def press_f(update, context):
    if (update.message.text == 'F'):
        update.message.reply_text('F')


def weather(update, context, OWM):
    if (update.message.text.lower().find("погода") >= 0) and (update.message.text.lower().find("\"") >= 0):
        try:
            result = re.search(
                r'\"\w{2,}\"', str(update.message.text.lower()))
            city = str(result.group(0)[1:-1]).capitalize()
            sf = OWM.weather_at_place(city)
            weather = sf.get_weather()
            update.message.reply_text(
                'Погода в городе {}: {}°C'.format(city, str(round(float(weather.get_temperature('fahrenheit')['temp'])-32.00, 1))))
        except:
            pass


def init(update, context, OWM):
    pizza(update, context)
    press_f(update, context)
    weather(update, context, OWM)
