from aiogram import Bot, Dispatcher, executor, types
import requests
from uuid import uuid4

TOKEN = "YOUR TOKEN" # Your token from the bot
API_KEY = "YOUR_API_KEY" # Get it here: http://www.omdbapi.com/apikey.aspx # More details can be found on google.


bot = Bot(TOKEN)
dp = Dispatcher(bot)



def get_json(name):
    r = requests.get(url=f"http://www.omdbapi.com/?i=tt3896198&apikey={API_KEY}&t={name}")

    return r.json()


@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    await message.answer(f"\
    \n👋 Hello, {message.from_user.full_name}\
    \n🤖 This is a bot that can send you information about any movie.\
    \n🔎 To find the movie you need write:\
    \n🎥 @ytsearchintg_bot movie title\
\n🧑 Bot developer: @moylub")


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    __name = query.query

    json = get_json(__name)

    if json["Response"] == "False":

        article_not_found = [types.InlineQueryResultArticle(
            id=uuid4(),
            title="Oops... No such movie found.",
            thumb_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDuQWraS91oUVYEqAbA9XY3xX0S59oBaSRbQ&usqp=CAU",
            input_message_content=types.InputTextMessageContent(message_text="No such movie was found. Here are the possible reasons:\
                \nMake a spelling mistake in a word\
                \nThere is no such movie in the database(("))]
        await query.answer(article_not_found, cache_time=60, is_personal=True)
    
    else:
        atricle_found = [types.InlineQueryResultArticle(
            id=uuid4(),
            title=json["Title"],
            thumb_url=json["Poster"],
            description=json['Plot'][:64] + "...",
            input_message_content=types.InputTextMessageContent(message_text=
            f"""Title: {json["Title"]}
                \nReleased: {json["Released"]}
                \nGenre: {json["Genre"]}
                \nWriters: {json["Writer"]}
                \nActors: {json["Actors"]}
                \nPlot: {json["Plot"]}
                \nLanguage: {json["Language"]}
                \nCountry: {json["Country"]}
                \nRating: {json["imdbRating"]}
                \nType: {json["Type"]}"""))
            
        ]


        await query.answer(atricle_found, cache_time=60, is_personal=True)
    



    


executor.start_polling(dp, skip_updates=True)