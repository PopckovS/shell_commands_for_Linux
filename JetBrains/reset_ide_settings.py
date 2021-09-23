import os
import re
import shutil

"""
Переопределите параметр IDE указав вашу IDE для удаления всех
временных ключей именно для нее.

И да, знаю что формировать пути хардкодок через слеши, не правильно,
ибо разделитель директорий в разных операционных системах разный,
но я использую Linux, и программу эту писал для Linux.
"""

# Путь к месту хранения лок настроек продукции JetBrains
path_key = '~/.config/JetBrains/'

# Путь домашней директории текущего пользователя
path_home = os.path.expanduser('~')

# Имя текущего пользователя
current_user = os.path.basename(path_home)

# Получаем список все IDE от JetBrains из которых позже отсеем только
# те IDE настройки для которой нам требуется удалить.
dir_list = os.listdir('{0}/.config/JetBrains'.format(path_home))

# Название IDE настройки для которой будем удалять, замените на название
# другой IDE (с учетом регистра) по своему желанию:
# 'CLion' 'PyCharm' 'Phpstorm' или другая которую используете.
IDE = 'PyCharm'


# TODO Что если вабще нету установленных IDE
def get_list_of_ide_version(dir_list, IDE):
    """Получает список всех версий указанной IDE"""
    find_dir = []
    for elem in dir_list:
        result = re.match(IDE, elem)
        if result is not None:
            find_dir.append(elem)

    return find_dir


def delete_all_ide_settings(find_ide, IDE):
    """
    Удаление происходит из 3 мест.
    1) из директории .java - настройки java для IDE
    2) из /eval/...evaluation.key - временный ключ активации
    3) из /options/other.xml - записи о сессиях работы с IDE
    """

    # TODO Тут сразу 3 удаления, их можно разбить на 3 разные функции

    # TODO 1
    # удаляем директорию с настройками для IDE из ~.java/.userPrefs/jetbrains/{указанная_IDE}
    java_settings_IDE = '{path}/.java/.userPrefs/jetbrains/{IDE}'.format(path=path_home, IDE=IDE.lower())
    if os.path.isdir(java_settings_IDE):
        shutil.rmtree(java_settings_IDE)

    # TODO 2
    # для каждой из найденных IDE
    for elem in find_ide:
        path = '{0}/.config/JetBrains/{1}/'.format(path_home, elem)
        list_eval = os.listdir('{0}/eval'.format(path))
        # находим содержимое их eval директорий, и если там что то есть удаялем это
        for eval in list_eval:
            file_in_eval = '{0}/eval/{1}'.format(path, eval)
            if os.path.isfile(file_in_eval) or os.path.isdir(file_in_eval):
                os.unlink(file_in_eval)

        # TODO 3
        # Для каждой из версий pycharm удаляем .xml записи о сеансах работы с IDE
        file_xml = '{0}/options/other.xml'.format(path)
        if os.path.isfile(file_xml):
            os.unlink(file_xml)


# TODO вывод о очистке версий даже если они и были пустые, пофиксить
def deleteIDE():
    # Получаем список всех версий IDE если они есть
    find_ide = get_list_of_ide_version(dir_list, IDE)

    # Если нашли хотя бы одну установленную версию указанной IDE то удаляем все ее настройки
    if len(find_ide) >= 1:
        delete_all_ide_settings(find_ide, IDE)
        print('Удалены настройки пользователя {user} для для {IDE} версий : {versions}'.
              format(user=current_user, IDE=IDE, versions=', '.join(find_ide))
              )
    else:
        # Если ни одной из установленных версий указанной IDE не нашлось
        print("Настроек для {0} у пользователя '{1}' не обнаружено.".format(IDE, current_user))


# запуск удаления всех настроек указанной IDE
deleteIDE()
