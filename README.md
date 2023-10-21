# Описание

> ###### _Это пет-проект, которым я занимаюсь в свободное время, делаю для себя и ради практики._

---

### Варианты использования:
1) Загрузить исполняемый файл со страницы [Releases](https://github.com/egoisticdesire/nvid_dlss_updater/releases/tag/1.0):

2) Запустить команды (Windows):
```python
git clone https://github.com/egoisticdesire/nvid_dlss_updater.git;
cd nvid_dlss_updater;
python -m venv venv;
.\venv\Scripts\activate;
pip install -r requirements.txt;
python .\main.py;
```

---

### Скрипт __downloader.py__:

- Идет на сайт, где расположены файлы библиотек `NVIDIA DLSS`;
- Находит актуальную версию;
- Проверяет соответствие версии в файле `meta.json`;
- Если запись в файле не соответствует текущей актуальной версии - фиксирует в файл текущую актуальную версию;
- Загружает новый файл;
- Если же запись в файле уже содержит последнюю доступную версию - обращается к пользователю: завершить процесс или
  продолжить выполнение.


### Скрипт __extractor.py__:

- Разархивирует выбранный архив.


### Скрипт __file_finder.py__:

- Пробегается по всем вложенным папкам выбранного каталога;
- Находит все файлы с заданным именем;
- Проверяет, существует ли файл-копия рядом с оригинальным файлом и делает копию, если таковой не существует;
- Заменяет старую версию файла актуальной.


### Скрипт __utility.py__:

- Проверяет, существует ли файл `meta.json`;
- Создает, если файл отсутствует или не содержит никаких данных;
- Заполняет по шаблону конфигурационные данные;
- Читает файл и возвращает данные для дальнейшей работы с ними;
- Также после выполнения всей программы могут оставаться временные файлы или, если загрузка была прервана, файлы незагруженных файлов. Они удаляются.
