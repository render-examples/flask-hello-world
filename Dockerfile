# Базовый образ
FROM python:3.9

# Определяем рабочую директорию контейнера
WORKDIR /webapp

# Копируем файл с необходимыми компонентами в созданную директорию
COPY requirements.txt /webapp

# Обновляем pip и устанавливаем компоненты
RUN pip install --upgrade pip && python -m pip install -r requirements.txt

# Указываем Docker порт для прослушивание (tcp)
EXPOSE 5000

# Копируем наше приложение внутрь контейнера
COPY . /webapp

# Определяем команду для старта приложения
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
