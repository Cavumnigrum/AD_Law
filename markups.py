from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os
import csv


def ff(path):
    with open(path, encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        for x in reader:
            yield x


def inline(buttons):
    if len(buttons) > 10:
        width = (len(buttons) // 3 + 1)
    elif len(buttons) <= 3:
        width = 3
    else:
        width = (len(buttons) // 2 + 1)
    keyboard = InlineKeyboardMarkup(row_width=width)
    for i, button in enumerate(buttons):
        if (i + 1) % width == 0:
            keyboard.row()
        btn = InlineKeyboardButton(text=button, callback_data=button)
        keyboard.insert(btn)
    return keyboard


path_1 = './pics/1) Реклама алкогольной продукции/'
path_2 = './pics/2) Реклама фармацевтической продукции/'
path_3 = './pics/3) Реклама, побуждающая к совершению противоправных действий, и реклама на транспорте/'
path_4 = './pics/4) Использование образа несовершеннолетнего в рекламе/'
path_5 = './pics/5) Неэтичная реклама/'
path_6 = './pics/6) Реклама, содержащая некорректное сравнение/'

notice_1, true_why_1, false_why_1, answer_1 = [x['Оспариваемое рекламное объявление'] for x in
                                               ff(path_1 + 'table.csv')], \
    [x['Варианты ответа верное'] for x in ff(path_1 + 'table.csv')], \
    [x['Варианты ответа неверное'] for x in ff(path_1 + 'table.csv')], \
    [x['Итоговый ответ'] for x in ff(path_1 + 'table.csv')]

notice_2, true_why_2, false_why_2, answer_2 = [x['Оспариваемое рекламное объявление'] for x in
                                               ff(path_2 + 'table.csv')], \
    [x['Варианты ответа верное'] for x in ff(path_2 + 'table.csv')], \
    [x['Варианты ответа неверное'] for x in ff(path_2 + 'table.csv')], \
    [x['Итоговый ответ'] for x in ff(path_2 + 'table.csv')]

notice_3, true_why_3, false_why_3, answer_3 = [x['Оспариваемое рекламное объявление'] for x in
                                               ff(path_3 + 'table.csv')], \
    [x['Варианты ответа верное'] for x in ff(path_3 + 'table.csv')], \
    [x['Варианты ответа неверное'] for x in ff(path_3 + 'table.csv')], \
    [x['Итоговый ответ'] for x in ff(path_3 + 'table.csv')]

notice_4, true_why_4, false_why_4, answer_4 = [x['Оспариваемое рекламное объявление'] for x in
                                               ff(path_4 + 'table.csv')], \
    [x['Варианты ответа верное'] for x in ff(path_4 + 'table.csv')], \
    [x['Варианты ответа неверное'] for x in ff(path_4 + 'table.csv')], \
    [x['Итоговый ответ'] for x in ff(path_4 + 'table.csv')]

notice_5, true_why_5, false_why_5, answer_5 = [x['Оспариваемое рекламное объявление'] for x in
                                               ff(path_5 + 'table.csv')], \
    [x['Варианты ответа верное'] for x in ff(path_5 + 'table.csv')], \
    [x['Варианты ответа неверное'] for x in ff(path_5 + 'table.csv')], \
    [x['Итоговый ответ'] for x in ff(path_5 + 'table.csv')]

notice_6, true_why_6, false_why_6, answer_6 = [x['Оспариваемое рекламное объявление'] for x in
                                               ff(path_6 + 'table.csv')], \
    [x['Варианты ответа верное'] for x in ff(path_6 + 'table.csv')], \
    [x['Варианты ответа неверное'] for x in ff(path_6 + 'table.csv')], \
    [x['Итоговый ответ'] for x in ff(path_6 + 'table.csv')]

why_list_1 = [[x.replace('Верное: ', '').replace('Верное- ', '').replace('Верно: ', '').replace('Верный: ', '').replace(
    'Верное. ', '').replace('Верное:', '') for x in true_why_1],
              [y.replace('Неверное: ', '').replace('Неверное- ', '').replace('Неверно: ', '').replace('Неверный: ','')
               .replace('Неверное. ', '').replace('Неверное:', '') for y in false_why_1]]

why_list_2 = [[x.replace('Верное: ', '').replace('Верное- ', '').replace('Верно: ', '').replace('Верный: ', '').replace(
    'Верное. ', '').replace('Верное:', '') for x in true_why_2],
              [y.replace('Неверное: ', '').replace('Неверное- ', '').replace('Неверно: ', '').replace('Неверный: ','')
               .replace('Неверное. ', '').replace('Неверное:', '') for y in false_why_2]]

why_list_3 = [[x.replace('Верное: ', '').replace('Верное- ', '').replace('Верно: ', '').replace('Верный: ', '').replace(
    'Верное. ', '').replace('Верное:', '') for x in true_why_3],
              [y.replace('Неверное: ', '').replace('Неверное- ', '').replace('Неверно: ', '').replace('Неверный: ','')
               .replace('Неверное. ', '').replace('Неверное:', '') for y in false_why_3]]

why_list_4 = [[x.replace('Верное: ', '').replace('Верное- ', '').replace('Верно: ', '').replace('Верный: ', '').replace(
    'Верное. ', '').replace('Верное:', '') for x in true_why_4],
              [y.replace('Неверное: ', '').replace('Неверное- ', '').replace('Неверно: ', '').replace('Неверный: ','')
               .replace('Неверное. ', '').replace('Неверное:', '') for y in false_why_4]]

why_list_5 = [[x.replace('Верное: ', '').replace('Верное- ', '').replace('Верно: ', '').replace('Верный: ', '').replace(
    'Верное. ', '').replace('Верное:', '') for x in true_why_5],
              [y.replace('Неверное: ', '').replace('Неверное- ', '').replace('Неверно: ', '').replace('Неверный: ','')
               .replace('Неверное. ', '').replace('Неверное:', '') for y in false_why_5]]

why_list_6 = [[x.replace('Верное: ', '').replace('Верное- ', '').replace('Верно: ', '').replace('Верный: ', '').replace(
    'Верное. ', '').replace('Верное:', '') for x in true_why_6],
              [y.replace('Неверное: ', '').replace('Неверное- ', '').replace('Неверно: ', '').replace('Неверный: ','')
               .replace('Неверное. ', '').replace('Неверное:', '') for y in false_why_6]]

start = '''
Здравствуйте! Это бот для проекта <b>Рекламное право</b>.

Для того чтобы начать квиз, необходимо воспользоваться командой Начать:
<b>/quiz - Начать квиз</b>
После введите имя для сохранения результата в базе данных.
Далее на выбор будут представлены 6 категорий для тренировки, с помощью кнопок выберете необходимую.
После выбора категории нажмите на кнопку "Начать!" для старта тренировки.
Вам предложат вопросы и краткие ответы к ним (да или нет).
В случае выбора правильного краткого ответа, будет предложено выбрать обоснование.
Затем бот покажет правильный ответ с пояснениями.

За правильный краткий ответ счёт будет увеличен на 0.5, за правильное обоснование счёт увеличится еще на 0.5.
За неправильный краткий ответ количество очков не изменится.

Для досрочного завершения тренировки и оценки прохождения воспользуйтесь кнопкой "Результаты".
Или для выхода в любой момент воспользуйтесь командой <i>Выход:</i><b>
/cancel - Отмена
</b>
'''

# start
name = '''
Введите ваше имя:
'''

user_choice = '''
Пожалуйста, выберите одно из доступных направлений тренировки:\n
'''

lst = list(os.listdir('./pics'))
lst.sort()
for i in range(len(lst)):
    user_choice += f'{lst[i]}\n'
yn = ['Да', 'Нет']
choose_dir = inline([x for x in range(1, 7)])
dn = inline(yn)

true_1 = ['Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Нет', 'Нет']

true_2 = ['Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да', 'Да']

true_3 = ['Да', "Да", "Нет", "Да", "Да", "Да", "Нет", "Да", "Да"]

true_4 = ["Да", "Да", "Да", "Да", "Да", "Да", "Да", "Нет", "Нет", "Нет"]

true_5 = ["Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да",
          "Да", "Да", "Нет", "Нет", "Нет", "Нет", "Нет", "Да", "Да", "Да", "Да", "Нет", "Нет", "Нет", "Нет", "Нет"]

true_6 = ["Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да",
          "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Да", "Нет", "Нет", "Нет",
          "Нет"]


false_1 = ['Нет' if x == 'Да' else 'Да' for x in true_1]
false_2 = ['Нет' if x == 'Да' else 'Да' for x in true_2]
false_3 = ['Нет' if x == 'Да' else 'Да' for x in true_3]
false_4 = ['Нет' if x == 'Да' else 'Да' for x in true_4]
false_5 = ['Нет' if x == 'Да' else 'Да' for x in true_5]
false_6 = ['Нет' if x == 'Да' else 'Да' for x in true_6]


done_1 = [False for x in true_1]
done_2 = [False for x in true_2]
done_3 = [False for x in true_3]
done_4 = [False for x in true_4]
done_5 = [False for x in true_5]
done_6 = [False for x in true_6]

rightwrong_1 = [False for x in true_1]
rightwrong_2 = [False for x in true_2]
rightwrong_3 = [False for x in true_3]
rightwrong_4 = [False for x in true_4]
rightwrong_5 = [False for x in true_5]
rightwrong_6 = [False for x in true_6]

statements = inline(['Обоснование №1', 'Обоснование №2'])
end = inline(['Следующий вопрос', 'Результаты'])
na4at = inline(['Начать!', 'Назад'])
back = inline(['Вернуться к выбору категорий'])

