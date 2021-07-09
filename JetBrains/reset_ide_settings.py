import os
import re
import shutil

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
    # Удаляем директорию с настройками для IDE из java
    shutil.rmtree('{path}/.java/.userPrefs/jetbrains/{IDE}'.format(path=path_home, IDE=IDE.lower()))

    # Удаляем все настройки и все временные ключи для каждой из версий IDE
    for elem in find_ide:
        path = '{0}/.config/JetBrains/{1}/'.format(path_home, elem)
        list_eval = os.listdir('{0}/eval'.format(path))
        for eval in list_eval:
            os.unlink('{0}/eval/{1}'.format(path, eval))

        # Для каждой из версий pycharm удаляем .xml записи о сеансах работы с IDE
        os.unlink('{0}/options/other.xml'.format(path))


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
