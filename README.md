# Система аутентификации и авторизации (Django + DRF + PostgreSQL)

## Описание проекта

Данный проект представляет собой backend-приложение с собственной системой:

* регистрации пользователей;
* авторизации;
* аутентификации;
* разграничения прав доступа.

Проект реализован на:

* Django
* Django REST Framework
* PostgreSQL
* JWT authentication

Главная задача проекта — реализовать собственную систему управления доступом к ресурсам приложения, не используя полностью встроенную систему permissions Django.

---

# Что реализовано

В проекте реализованы:

### Пользовательская система

* Регистрация пользователя
* Login
* Logout
* Обновление профиля
* Soft delete пользователя
* JWT authentication

### Система ролей

Реализованы роли:

* Admin
* Employee

### Система авторизации

Реализованы:

* роли;
* ресурсы системы;
* правила доступа.

### Mock бизнес-объекты

Реализован тестовый бизнес-ресурс:

* Products

---

# Архитектура проекта

Проект состоит из нескольких приложений.

## 1. users

Отвечает за:

* регистрацию;
* login;
* logout;
* обновление профиля;
* удаление пользователя.

---

## 2. access_control

Отвечает за:

* роли;
* права доступа;
* бизнес-ресурсы;
* проверку доступа пользователя.

---

## 3. business

Содержит mock-ресурсы бизнес-приложения.

Для демонстрации реализован ресурс:

```text
products
```

---

# Схема базы данных

## Таблица User

Содержит пользователей системы.

### Поля

| Поле        | Описание                |
| ----------- | ----------------------- |
| id          | ID пользователя         |
| email       | Email                   |
| password    | Хэшированный пароль     |
| first_name  | Имя                     |
| last_name   | Фамилия                 |
| middle_name | Отчество                |
| is_active   | Активен ли пользователь |
| role        | Роль пользователя       |
| created_at  | Дата создания           |
| updated_at  | Дата обновления         |

### Логика

Пользователь может:

* зарегистрироваться;
* войти в систему;
* обновить профиль;
* удалить аккаунт (soft delete).

Soft delete означает:

Пользователь не удаляется из БД, а:

```python
is_active = False
```

После этого login становится невозможным.

---

## Таблица Role

Содержит роли пользователей.

### Примеры ролей

### Admin

Имеет доступ к:

* products
* permissions

Может изменять права доступа.

### Employee

Имеет ограниченные права.

Например:

* читать products;
* не управлять permissions.

---

## Таблица BusinessElement

Описывает ресурсы приложения.

### Примеры

```text
products
permissions
```

---

## Таблица AccessRule

Основная таблица авторизации.

Содержит правила:

> какая роль имеет доступ к какому ресурсу и что она может делать.

### Поля

| Поле              | Описание  |
| ----------------- | --------- |
| role              | Роль      |
| element           | Ресурс    |
| read_permission   | Читать    |
| create_permission | Создавать |
| update_permission | Изменять  |
| delete_permission | Удалять   |

---

# Как работает система доступа

Система работает следующим образом.

### Шаг 1

Пользователь логинится.

### Шаг 2

После login система создаёт JWT-token.

Пример:

```text
eyJhbGc...
```

---

### Шаг 3

При следующих запросах token передаётся:

```text
?token=jwt_token
```

или через:

```http
Authorization: Bearer jwt_token
```

---

### Шаг 4

Middleware определяет пользователя.

Система находит:

```python
request.user
```

---

### Шаг 5

Проверяется право доступа.

Например:

Employee запрашивает:

```text
/api/business/products/
```

Система проверяет:

1. Кто пользователь?
2. Какая у него роль?
3. Есть ли AccessRule?
4. Разрешён ли read_permission?

Если да:

```http
200 OK
```

Если нет:

```http
403 Forbidden
```

---

# Разница между Authentication и Authorization

## Authentication

Отвечает на вопрос:

> Кто ты?

Пример:

Login + JWT token.

---

## Authorization

Отвечает на вопрос:

> Что тебе можно делать?

Пример:

Employee нельзя менять permissions.

---

# Реализованные API

## Регистрация

### Endpoint

```http
POST /api/users/register/
```

### Body

```json
{
    "email": "user@test.com",
    "password": "12345678",
    "password_repeat": "12345678",
    "first_name": "Denis",
    "last_name": "Test",
    "middle_name": "Testovich"
}
```

---

## Login

### Endpoint

```http
POST /api/users/login/
```

### Body

```json
{
    "email": "user@test.com",
    "password": "12345678"
}
```

### Response

```json
{
    "token": "jwt_token"
}
```

---

## Logout

### Endpoint

```http
POST /api/users/logout/
```

---

## Update profile

### Endpoint

```http
PATCH /api/users/profile/
```

---

## Delete account (soft delete)

### Endpoint

```http
DELETE /api/users/profile/
```

Результат:

```python
is_active = False
```

---

## Products

Mock business resource.

### Endpoint

```http
GET /api/business/products/
```

---

## Access rules

### Получение правил

```http
GET /api/access-control/rules/
```

Только для Admin.

---

### Изменение правил

```http
PATCH /api/access-control/rules/<id>/
```

Пример:

```json
{
    "read_permission": false
}
```

---

# Ошибки системы

## 401 Unauthorized

Возвращается если:

* пользователь не найден;
* token отсутствует;
* token невалидный.

Пример:

```json
{
    "error": "Unauthorized"
}
```

---

## 403 Forbidden

Возвращается если:

* пользователь найден;
* но прав недостаточно.

Пример:

```json
{
    "error": "Forbidden"
}
```

---

# Демонстрация работы системы

Была выполнена проверка:

### Шаг 1

Admin изменил право доступа через API.

Запрос:

```http
PATCH /api/access-control/rules/3/
```

Body:

```json
{
    "read_permission": false
}
```

---

### Шаг 2

Employee попытался открыть:

```http
/api/business/products/
```

---

### Результат

Система вернула:

```http
403 Forbidden
```

Это подтверждает корректную работу системы авторизации.

---

# Как запустить проект

## 1. Установить зависимости

```bash
pip install -r requirements.txt
```

---

## 2. Выполнить миграции

```bash
python manage.py migrate
```

---

## 3. Запустить сервер

```bash
python manage.py runserver
```

---

## 4. Открыть API

```text
http://127.0.0.1:8000/
```

---

# Как проверить проект

## Проверка login

1. Зарегистрировать пользователя.
2. Выполнить login.
3. Получить token.

---

## Проверка permissions

1. Залогиниться как Admin.
2. Изменить AccessRule.
3. Залогиниться как Employee.
4. Проверить доступ к products.

Ожидаемый результат:

```http
403 Forbidden
```

---

# Вывод

В рамках проекта была реализована собственная backend-система аутентификации и авторизации.

Были реализованы:

* JWT authentication;
* role-based access control;
* разграничение прав доступа;
* soft delete;
* mock business resources;
* API управления правами доступа.

Система успешно различает:

* неавторизованного пользователя (401);
* пользователя без доступа (403).
