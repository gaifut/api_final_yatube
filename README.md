# api_final
api final
### Краткое описание проекта:
Данный проект является учебным и представляет из себя макет социальной сети. Пользователи могут:
- Создавать, редактировать и удалять свои посты.
- Комментировать посты.
- Редактировать и удалять свои комментарии.
- Подписываться на других пользователей.

Основная цель проекта - применить теоретичесие знания на практике, используя принцип API First.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/gaifut/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3.9 -m venv venv
```

```
. venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3.9 manage.py migrate
```

Запустить проект:

```
python3.9 manage.py runserver
```
