import csv
from django.shortcuts import render
from django.core.cache import cache
from django.shortcuts import redirect
from . import terms_work
from .terms_work import delete_term_from_csv



def terms_list_del(request):
    """показ формы удаления выделенных терминов"""
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list_del.html", context={"terms": terms})


def terms_list_del_del(request):
    """подтверждение удаления выделенных терминов"""

    if request.method == 'POST':
        delete_rows = request.POST.getlist('delete_rows')

        # Читаем данные из файла
        data = terms_work.get_terms_for_table()

        # Удаляем помеченные строки
        for i in sorted(delete_rows, reverse=True):
            del data[int(i)]

        # Записываем обновленные данные в файл
        with open('./data/terms.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    # Перенаправляем пользователя на страницу со списком терминов
    return redirect('/term-list')

def terms_list_del_look(request):
    """просмотр терминов на удаление"""
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





def term_delete(request):
    """удаление терминов"""
    #terms = terms_work.get_terms_for_table()
    updated_data = delete_term_from_csv()
    #return render(request, "term_list.html", context={"terms": terms})
    if updated_data:
        print(updated_data)
    return redirect('term_list')



def index(request):
    """показ главной страницы"""
    return render(request, "index.html")


def terms_list(request):
    """показ окна списка терминов"""
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    """ отображение формы добавления терминов"""
    return render(request, "term_add.html")


def add_translate(request):
    """ отображение формы переводов терминов"""
    return render(request, "translate_add.html")


def send_term(request):
    """ функция записи терминов в файл CSV"""
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term(new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def send_translate(request):
    """ функция записи переводов в файл CSV"""
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term1", "")
        new_definition = request.POST.get("new_definition1", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_translate(new_term1, new_definition1)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def show_stats(request):
    """ функция показа статистики"""
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)
