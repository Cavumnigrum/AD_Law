import random
from background import keep_alive

from loguru import logger
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaPhoto
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import markups as btn
from db import Database
import config

import asyncio

db = Database("quiz.db")

db.create_table()
TOKEN = config.TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Fsm(StatesGroup):
    name = State()
    path = State()
    user_naber = State()


async def result(data, id):
    points = data["points"]
    points = int(points) if points == int(points) else points
    text = f'Ваши баллы: {points}/{data["state"]}'
    await asyncio.sleep(0.5)
    await bot.send_message(id, text)
    txt = 'Спасибо за участие в квизе!\n<i>Вы можете вернуться к выбору категорий с помощью кнопки ниже</i>'
    await asyncio.sleep(0.5)
    await bot.send_message(id, txt, parse_mode='html', reply_markup=btn.back)
    db.post_result(id, data['name'], points, data['points'], data['state'])
    logger.info(data)


@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message, state: FSMContext):
    await asyncio.sleep(0.5)
    await bot.send_message(message.from_user.id, "Выход.\n")
    await state.finish()
    return False


@dp.message_handler(commands=['start'])
async def admin(message: types.Message, state: FSMContext):
    await asyncio.sleep(0.5)
    await bot.send_message(message.chat.id, btn.start, parse_mode='html')


@dp.message_handler(commands=['quiz'])
async def addmin(message: types.Message, state: FSMContext):
    await asyncio.sleep(0.5)
    await bot.send_message(message.chat.id, btn.name)
    await Fsm.name.set()


@dp.message_handler(state=Fsm.name)
async def name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await asyncio.sleep(0.5)
    await bot.send_message(message.from_user.id,
                           btn.user_choice,
                           reply_markup=btn.choose_dir)
    await Fsm.next()
    await state.update_data(state=0)


@dp.callback_query_handler(state=Fsm.path)
async def choose_path(callback: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=callback.id)
    await state.update_data({'path': callback.data})
    lsl = (random.sample(range(0, len(btn.__dict__[f'answer_{callback.data}'])),
                         len(btn.__dict__[f'answer_{callback.data}'])))
    lst = ([(x // (len(btn.__dict__[f'answer_{callback.data}']) // 2 + 1))
            for x in range(len(btn.__dict__[f'answer_{callback.data}']))])
    random.shuffle(lst)
    points = 0
    done = btn.__dict__[f'done_{callback.data}']
    rightwrong = btn.__dict__[f'rightwrong_{callback.data}']

    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await state.update_data({'done': done})
    await state.update_data({'lsl': lsl})
    await state.update_data({'lst': lst})
    await state.update_data({'points': points})
    await state.update_data({'rightwrong': rightwrong})

    await asyncio.sleep(0.5)
    await bot.send_message(
        callback.from_user.id,
        f'Ваша выбранная категория: {btn.lst[int(callback.data) - 1]}',
        reply_markup=btn.na4at)
    await Fsm.next()


@dp.callback_query_handler(state=Fsm.user_naber)
async def user_naber(callback: types.CallbackQuery, state: FSMContext):
     
    data = await state.get_data(state)
    done_data = data['done']
    state_user = data["state"]
    path_data = data['path']
    lsl = data['lsl']
    lst = data['lst']
    points = data['points']
    rightwrong_data = data['rightwrong']
    try:
        await bot.edit_message_reply_markup(chat_id = callback.from_user.id,
                                 message_id=callback.message.message_id,
                                            reply_markup=None)
    except:
        logger.info('Failure')
    if callback.data == btn.__dict__[f'true_{path_data}'][lsl[state_user - 1]] and done_data[state_user-1]:

        if callback.data == 'Да':

            txtt = f'''Какое из обоснований верное?
Обоснование №1. {btn.__dict__[f'why_list_{path_data}'][lst[state_user - 1]][lsl[state_user - 1]]}
\nОбоснование №2. {btn.__dict__[f'why_list_{path_data}'][1 - lst[state_user - 1]][lsl[state_user - 1]]}'''
        else:
            txtt = f"По какому поводу могли быть претензии к этой рекламе?\
Обоснование №1. {btn.__dict__[f'why_list_{path_data}'][lst[state_user - 1]][lsl[state_user - 1]]}\
\n\nОбоснование №2. {btn.__dict__[f'why_list_{path_data}'][1 - lst[state_user - 1]][lsl[state_user - 1]]}"
        try:
            t = f"{callback.message.text}\n\n<i>Ваш вариант ответа: {callback.data}</i>"
            await bot.edit_message_text(t, callback.from_user.id, callback.message.message_id, parse_mode='html', disable_web_page_preview=True)
        except:
            try:
                t = f"{callback.message.caption}\n\n<i>Ваш вариант ответа: {callback.data}</i>"
                await bot.edit_message_caption(callback.from_user.id, callback.message.message_id,caption = t, parse_mode='html')
            except Exception as E:
                logger.info(E)
        await asyncio.sleep(0.5)
        await bot.send_message(callback.from_user.id,
                                   txtt,
                                   reply_markup=btn.statements, disable_web_page_preview=True)
    elif callback.data == btn.__dict__[f'false_{path_data}'][lsl[state_user - 1]] and done_data[state_user-1]:
        text = 'К сожалению, Вы ответили неправильно'
        try:
            t = f"{callback.message.text}\n\n<i>Ваш вариант ответа: {callback.data}</i>"
            await bot.edit_message_text(t, callback.from_user.id, callback.message.message_id, parse_mode='html', disable_web_page_preview=True)
        except:
            try:
                t = f"{callback.message.caption}\n\n<i>Ваш вариант ответа: {callback.data}</i>"
                await bot.edit_message_caption(callback.from_user.id, callback.message.message_id,caption = t, parse_mode='html')
            except Exception as E:
                logger.info(E)
        await asyncio.sleep(0.5)
        await bot.send_message(callback.from_user.id, text, disable_web_page_preview=True)
        final = f'''<b>Правильный ответ:</b>\n{btn.__dict__[f'answer_{path_data}'][lsl[state_user - 1]]}'''
         
        await asyncio.sleep(0.5)
        await bot.send_message(callback.from_user.id, final, parse_mode='html', disable_web_page_preview=True)
        end_of_q = 'Можно перейти к следующему вопросу или закончить квиз и узнать результаты!'
         
        await asyncio.sleep(0.5)
        await bot.send_message(callback.from_user.id,
                               end_of_q,
                               reply_markup=btn.end, disable_web_page_preview=True)

    elif len(callback.data) >= 13 and len(callback.data) < 16 and done_data[state_user-1]:
        if int(callback.data.replace('Обоснование №', '')) == 1:
            tt = f"Вы выбрали Обоснование №1.\n{btn.__dict__[f'why_list_{path_data}'][lst[state_user - 1]][lsl[state_user - 1]]}"
            await bot.edit_message_text(tt,callback.from_user.id,callback.message.message_id, disable_web_page_preview=True,parse_mode='html')
            if btn.__dict__[f'why_list_{path_data}'][lst[state_user - 1]][lsl[state_user - 1]] \
                    == btn.__dict__[f'true_why_{path_data}'][lsl[state_user - 1]] \
                    .replace('Верное: ', '').replace('Верное- ', '').replace('Верно: ', '').replace('Верный: ', '') \
                    .replace('Верное. ', '').replace('Верное:', ''):
                ttxt = 'Вы ответили правильно!'
                rightwrong_data[state_user - 1] = True
                await asyncio.sleep(0.5)
                await bot.send_message(callback.from_user.id, ttxt, disable_web_page_preview=True)
                points += 1
            else:
                ttxt = 'К сожалению, Вы ответили неправильно'
                points += 0.5
                 
                await asyncio.sleep(0.5)
                await bot.send_message(callback.from_user.id, ttxt, disable_web_page_preview=True)
        elif int(callback.data.replace('Обоснование №', '')) == 2:
            tt = f"Вы выбрали Обоснование №2.\n{btn.__dict__[f'why_list_{path_data}'][1 - lst[state_user - 1]][lsl[state_user - 1]]}"
            await bot.edit_message_text(tt, callback.from_user.id, callback.message.message_id,parse_mode='html', disable_web_page_preview=True)
            if btn.__dict__[f'why_list_{path_data}'][1 - lst[state_user - 1]][lsl[state_user - 1]] \
                    == btn.__dict__[f'true_why_{path_data}'][lsl[state_user - 1]] \
                    .replace('Верное: ', '').replace('Верное- ', '').replace('Верно: ', '').replace('Верный: ', '') \
                    .replace('Верное. ', '').replace('Верное:', ''):
                ttxt = 'Вы ответили правильно!'
                rightwrong_data[state_user - 1] = True
                await asyncio.sleep(0.5)
                await bot.send_message(callback.from_user.id, ttxt, disable_web_page_preview=True)
                points += 1
            else:
                ttxt = 'К сожалению, Вы ответили неправильно'
                points += 0.5
                 
                await asyncio.sleep(0.5)
                await bot.send_message(callback.from_user.id, ttxt, disable_web_page_preview=True)
        expl = btn.__dict__[f'answer_{path_data}'][lsl[state_user - 1]]
        final = f'''<b>Правильный ответ:</b>\n{expl}'''
         
        await asyncio.sleep(0.5)
        await bot.send_message(callback.from_user.id, final, parse_mode='html', disable_web_page_preview=True)
        end_of_q = 'Можно перейти к следующему вопросу или закончить квиз и узнать результаты!'
         
        await asyncio.sleep(0.5)
        await bot.send_message(callback.from_user.id,
                               end_of_q,
                               reply_markup=btn.end, disable_web_page_preview=True)

    elif callback.data == 'Назад' or callback.data == 'Вернуться к выбору категорий':
        await bot.delete_message(callback.from_user.id,
                                 callback.message.message_id)
        state_user = 0
        points = 0
         
        await asyncio.sleep(0.5)
        await bot.send_message(callback.from_user.id,
                               btn.user_choice,
                               reply_markup=btn.choose_dir, disable_web_page_preview=True)
        await state.update_data({'points': points})
        await state.update_data({'state': state_user})
    elif callback.data == 'Результаты' or state_user == len(
            btn.__dict__[f'answer_{path_data}']):
        await result(data, callback.from_user.id)
        return
    elif callback.data in '123456':
        path_data = callback.data
        lsl = (random.sample(
            range(0, len(btn.__dict__[f'answer_{callback.data}'])),
            len(btn.__dict__[f'answer_{callback.data}'])))
        lst = ([(x // (len(btn.__dict__[f'answer_{callback.data}']) // 2 + 1))
                for x in range(len(btn.__dict__[f'answer_{callback.data}']))])
        random.shuffle(lst)
        await state.update_data({'lsl': lsl})
        await state.update_data({'lst': lst})
        await bot.delete_message(callback.from_user.id,
                                 callback.message.message_id)
         
        await asyncio.sleep(0.5)
        await bot.send_message(
            callback.from_user.id,
            f'Ваша выбранная категория: {btn.lst[int(callback.data) - 1]}',
            reply_markup=btn.na4at, disable_web_page_preview=True)
        state_user = 0
        points = 0
        done_data = btn.__dict__[f'done_{path_data}']
        rightwrong_data = btn.__dict__[f'rightwrong_{callback.data}']
        await state.update_data({'rightwrong': rightwrong_data})
        await state.update_data({'done': done_data})
        await state.update_data({'path': path_data})
    elif callback.data == 'Начать!' or callback.data == 'Следующий вопрос':
        state_user += 1
        done_data[state_user-1] = True
        txt = '''<b>Есть ли нарушение ФЗ “О рекламе” в данном материале?</b>\n'''
        if btn.__dict__[f'notice_{path_data}'][lsl[state_user - 1]]:
            txt += str(btn.__dict__[f'notice_{path_data}'][lsl[state_user - 1]])
             
            await asyncio.sleep(0.5)
            await bot.send_message(callback.from_user.id,
                                   txt,
                                   reply_markup=btn.dn,
                                   parse_mode='html', disable_web_page_preview=True)
        else:
            if not (path_data == '6' and lsl[state_user - 1] == 35):
                if path_data == '1' and lsl[state_user - 1] == 8:
                    txt += '''\n<i> источник изображения: группа Вконтакте</i>'''
                try:
                     
                    await asyncio.sleep(0.5)
                    await bot.send_photo(
                        callback.from_user.id,
                        types.InputFile(btn.__dict__[f'path_{path_data}'] +
                                        f'{lsl[state_user - 1] + 1}.png'),
                        reply_markup=btn.dn,
                        caption=txt,
                        parse_mode='html')
                except Exception as e:
                    try:
                         
                        await asyncio.sleep(0.5)
                        await bot.send_photo(
                            callback.from_user.id,
                            types.InputFile(btn.__dict__[f'path_{path_data}'] +
                                            f'{lsl[state_user - 1] + 1}.jpg'),
                            reply_markup=btn.dn,
                            caption=txt,
                            parse_mode='html')
                    except Exception as ee:
                        try:
                             
                            await asyncio.sleep(0.5)
                            await bot.send_video(
                                callback.from_user.id,
                                types.InputFile(btn.__dict__[f'path_{path_data}'] +
                                                f'{lsl[state_user - 1] + 1}.mp4'),
                                reply_markup=btn.dn,
                                caption=txt,
                                parse_mode='html')
                        except Exception as eee:
                            logger.info(e)
                            logger.info(ee)
                            logger.info(eee)
            else:
                try:
                    media = [
                        InputMediaPhoto(types.InputFile(btn.__dict__['path_6'] + f'{lsl[state_user - 1] + 1}_1.jpg')),
                        InputMediaPhoto(types.InputFile(btn.__dict__['path_6'] + f'{lsl[state_user - 1] + 1}_2.jpg'))]
                     
                    await asyncio.sleep(0.5)
                    await bot.send_media_group(callback.from_user.id, media)
                    teext = '''<b>Есть ли нарушение ФЗ “О рекламе” в матерале выше??</b>\n'''
                    await bot.send_message(callback.from_user.id,teext,reply_markup=btn.dn,parse_mode='html')
                except Exception as E:
                    logger.info(E)
    else:
        logger.info(callback.data)
    await state.update_data({'done': done_data})
    await state.update_data({'rightwrong': rightwrong_data})

    await state.update_data({'points': points})
    await state.update_data({'state': state_user})


if __name__ == "__main__":
    keep_alive()
    executor.start_polling(dp, skip_updates=True)
