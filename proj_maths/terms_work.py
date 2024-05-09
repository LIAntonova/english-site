"""Модуль работы с терминами"""
import csv


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

def write_translate(new_term1, new_definition1):
    """Функция записи новых переводов - сделана как копия из функции записи, писала в файл terms. Попытка сделать второй файл базы данных не получилась"""
    new_term1_line = f"{new_term1};{new_definition1};user"
    with open("./data/translate.csv", "r", encoding="utf-8") as f:
        existing_terms = [l.strip("\n") for l in f.readlines()]
        title = existing_terms[0]
        old_terms = existing_terms[1:]
    terms_sorted = old_terms + [new_term1_line]
    terms_sorted.sort()
    new_terms = [title] + terms_sorted
    with open("./data/translate.csv", "w", encoding="utf-8") as f:
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


