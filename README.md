# openwall
Простая общественная стена на Flask для примера работы Timeweb Cloud Apps. [Ссылка на статью](https://habr.com/ru/companies/timeweb/articles/812413/)

## Установка на Timeweb Cloud Apps
Вам нужно будет зарегистрироваться на [Timeweb Cloud](https://timeweb.cloud/services/vds-vps).

После перейдите в раздел приложения и выберите бекенд на Python, фреймворк flask.

Измените команду сборки на:

```bash
bash deploy.sh
```

А команду запуска на:

```bash
gunicorn main:app --timeout 60
```

После начните деплой. Если возникли вопросы - откройте issue к данному репозиторию с темой "Проблема при деплое на Cloud Apps".
