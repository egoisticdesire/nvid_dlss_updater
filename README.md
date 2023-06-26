# Описание

---

### Скрипт __downloader.py__:

- Идет на сайт, где расположены файлы библиотек `NVidia DLSS`;
- Находит актуальную версию;
- Проверяет соответствие в файле `nvid_dlss_version.json`;
- Если запись в файле не соответствует текущей актуальной версии - фиксирует в файл текущую актуальную версию;
- Загружает новый файл;
- Если же запись в файле уже содержит последнюю доступную версию - обращается к пользователю: завершить процесс или
  продолжить выполнение.

---

### Скрипт __extractor.py__:

- Разархивирует выбранный архив.

---

### Скрипт __finder_and_copier.py__:

- Пробегается по всем вложенным папкам выбранного каталога;
- Находит все файлы с заданным именем;
- Проверяет, существует ли файл-копия рядом с оригинальным файлом, и делает копию, если таковой не существует;
- Заменяет старую версию файла актуальной.

---

> _TODO:_
>
> ![checked](assets/checked.png) _добавить возможность в автоматическом режиме находить и заменять файл, рекурсивно пробегая по папкам_
>
> ![checked](assets/checked.png) _добавить возможность в автоматическом режиме извлекать файл из архива [пока что только zip]_
>
> ![checked](assets/checked.png) _добавить возможность в автоматическом режиме ходить на сайт и проверять наличие новой версии [скачивать]_
> 
> ![unchecked](assets/unchecked.png) _добавить какой-нибудь графический интерфейс_
>
> ![unchecked](assets/unchecked.png) _создать исполняемый файл_
>

---

###### _PS: Это пет-проект, которым я занимаюсь в свободное время, делаю для себя и ради практики._
