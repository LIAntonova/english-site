"""Модуль работы с терминами"""


# views.py
import csv
from django.shortcuts import render
def terms_list_del_del(request):
    if request.method == 'POST':
        delete_rows = request.POST.getlist('delete_rows')

        # Читаем данные из файла
        with open('./data/terms.csv', 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Удаляем помеченные строки
        for i in sorted(delete_rows, reverse=True):
            del data[int(i)]

        # Записываем обновленные данные в файл
        with open('./data/terms.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    # Перенаправляем пользователя на страницу со списком терминов
    return redirect('/term-list')




def delete_term_from_csv(term):
    try:
        # Открываем файл и читаем его содержимое
        with open("./data/terms.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            data = list(reader)

        # Находим строку, которую нужно удалить
        for i, row in enumerate(data):
            if row[0] == term:
                deleted_term = row
                del data[i]
                print(f"Deleted term: {', '.join(deleted_term)}")
                break
        else:
            print(f"Term '{term}' not found.")
            return

        # Записываем обновленные данные обратно в файл
        with open('./data/terms.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        print("Data updated successfully.")
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def terms_list_del_look(request):
    if request.method == 'POST':
        rows_to_delete = request.POST.getlist('delete_rows')
        # Теперь у вас есть список значений, которые были выбраны для удаления
        # Вы можете выполнить нужные действия здесь, например, удалить соответствующие записи из базы данных
        # или из файла.
        print(rows_to_delete)
        for row_id in rows_to_delete:
            print()
            # Здесь вы можете выполнить нужные действия для удаления строки с идентификатором row_id
            pass
        # После выполнения действий перенаправьте пользователя на нужную страницу,
        # например:
        # return HttpResponseRedirect('/desired-page/')
    # Если метод запроса не POST, просто перенаправьте пользователя на нужную страницу
    # с помощью HttpResponseRedirect, если это необходимо.


def get_terms_for_table():
    """Функция возвращает список терминов"""
    terms = []
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        cnt = 1
        for line in f.readlines()[1:]:
            term, definition, source = line.split(";")
            terms.append([cnt, term, definition])
            cnt += 1
    return terms









def write_term(new_term, new_definition):
    """Функция записи новых терминов"""
    new_term_line = f"{new_term};{new_definition};user"
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        existing_terms = [l.strip("\n") for l in f.readlines()]
        title = existing_terms[0]
        old_terms = existing_terms[1:]
    terms_sorted = old_terms + [new_term_line]
    terms_sorted.sort()
    new_terms = [title] + terms_sorted
    with open("./data/terms.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_terms))




def get_terms_stats():
    """Функция расчета статистики терминов,
    имеющихся в базе данных
    """
    db_terms = 0
    user_terms = 0
    defin_len = []
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            term, defin, added_by = line.split(";")
            words = defin.split()
            defin_len.append(len(words))
            if "user" in added_by:
                user_terms += 1
            elif "db" in added_by:
                db_terms += 1
    stats = {
        "terms_all": db_terms + user_terms,
        "terms_own": db_terms,
        "terms_added": user_terms,
        "words_avg": sum(defin_len)/len(defin_len),
        "words_max": max(defin_len),
        "words_min": min(defin_len)
    }
    return stats


