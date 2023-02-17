import asyncio
from pyrogram import Client, filters

api_id = 0000000000
api_hash = "xxxxxxxxxxxxxxxx"
bot_token = "00000000:xxxxxxxxxxxxxxxxxxxxxxxxx"

menu = 0
phone_number = ""
sc = None

bot = Client("cp_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

app = Client("test_auth", api_id=api_id, api_hash=api_hash, phone_number=phone_number)

async def auth(number):
    global api_id
    global api_hash
    global phone_number
    global sc
    global menu
    global app
    print(phone_number)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print(number)
    if menu == 1:
        await app.connect()
        print("trying send code")
        sc = await app.send_code(phone_number=number)
        print("OK")
    elif menu == 2:
        code = number
        ch = sc.phone_code_hash
        print(ch)
        await app.sign_in(phone_number=phone_number, phone_code_hash=ch, phone_code=str(code))
        await app.disconnect()
        loop.close()

@bot.on_message(filters.command(["start"]) & filters.text)
async def command_start(client, message):
    global menu
    await message.reply_text("Старт аутентификации! Отправь номер телефона в международном формате (+1234567890)")
    menu = 1

@bot.on_message(filters.text)
async def command_start(client, message):
    global menu
    global phone_number
    global code
    if menu == 1:
        phone = message.text
        phone = phone.replace("+", "")
        if phone.isdigit():
            print(phone)
            phone_number = phone
            await auth(phone_number)
            menu = 2
            print("is ok")
            await message.reply_text("DONE!\nТеперь отправь код авторизации, с цифрами через пробел (прим. \"1 2 266\" и подобное)")
        else:
            await message.reply_text("Phone incorrect! try again")
    elif menu == 2:
        v_dig = message.text
        v_dig = v_dig.replace(" ", "") # если в бота или личку ТГ с которого производится авторизация, пересылается
# чистый код авторизации - он аннулируется, потому я использую лайфхак с вводом кода через пробел и он работает
        print(v_dig)
        if v_dig.isdigit():
            code = v_dig
            print(code)
            await auth(code)
            await message.reply_text("DONE!\nАвторизация прошла успешно!")
        else:
            await message.reply_text("CODE incorrect! try again")
bot.run()
