import telebot
import model

API_KEY = "6562576439:AAH5_OO2hBHvPyDOvMeyB43QQnNZ5lMwzIg" # TODO: заменить токен
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Отправьте изображение")
    bot.register_next_step_handler(message, handle_photo)
    print(1)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = "received_image.jpg"
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    
    latex_code = model.process_image(src) # TODO: Заменить на функцию обработки
    bot.send_message(message.chat.id, latex_code)
    bot.register_next_step_handler(message, handle_photo)



@bot.message_handler(content_types=['text'])
def send_tex(message, latex_code):
    
    bot.register_next_step_handler(message, handle_photo)


bot.polling(non_stop=True)