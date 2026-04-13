# Secrets Telegram Bot

Ваш быстрый, безопасный и удобный менеджер паролей в Telegram.

[![Lint and test](https://github.com/everysoftware/secrets-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/everysoftware/secrets-bot/actions/workflows/ci.yml)
[![Deploy to server](https://github.com/everysoftware/secrets-bot/actions/workflows/cd.yml/badge.svg)](https://github.com/everysoftware/secrets-bot/actions/workflows/cd.yml)

<img src="https://raw.githubusercontent.com/everysoftware/secrets-telegram-bot/master/assets/promo.png" width="300" />  
<img src="https://raw.githubusercontent.com/everysoftware/secrets-telegram-bot/master/assets/password_view.png" width="300" />  
<img src="https://raw.githubusercontent.com/everysoftware/secrets-telegram-bot/master/assets/password_gen.png" width="300" />  

## Начало работы

1. Запустите бота и зарегистрируйтесь
2. Добавяйте свои пароли и управляйте ими быстро и безопасно
3. Создавайте надёжные пароли с помощью функции "Предложить пароль"
4. Готово!

## Больше скриншотов

<details>

<summary>Посмотреть</summary> 
<img src="https://raw.githubusercontent.com/everysoftware/secrets-telegram-bot/master/assets/welcome.png" width="300" />  
<img src="https://raw.githubusercontent.com/everysoftware/secrets-telegram-bot/master/assets/password_change.png" width="300" />  
<img src="https://raw.githubusercontent.com/everysoftware/secrets-telegram-bot/master/assets/password_list.png" width="300" />  

</details>

## Стек технологий

Продукт: Python3 • Aiogram3 • PostgreSQL • SQLAlchemy • Alembic • Redis • arq • cryptography • Aiottp • Docker  
Инструменты: PyCharm • Black • Isort • Ruff • Mypy • Pytest

## Сборка

1. Создайте файл окружения ```.env``` на основании ```.dist.env```.
2. Соберите и запустите контейнеры Docker: ```docker-compose up -d --build```
3. Готово!

**Made with ❤️ by @everysoftware**
