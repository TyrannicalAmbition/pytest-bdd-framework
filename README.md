# Pytest-BDD Framework

### Ключевые особенности:

- **BDD подход** - тесты написаны на языке Gherkin для лучшего понимания бизнес-логики
- **Page Object Pattern** - инкапсуляция взаимодействия с UI элементами
- **Модульная архитектура** - четкое разделение ответственности между компонентами
- **Автоматическая регистрация шагов** - шаги регистрируются как pytest плагины
- **Гибкая конфигурация** - поддержка разных браузеров и режимов запуска
- **Pre-commit** - чистый и стандартизированный код.

## Структура проекта

```
pytest_bdd_frame/
├── components/              # Page Objects и компоненты
│   ├── base/                # Базовые классы
│   │   ├── base_page.py     # Базовый класс для страниц
│   │   └── base_wait.py     # Класс для ожиданий
│   ├── config/              # Конфигурация
│   │   └── urls.py          # URL адреса
│   ├── locators/            # Локаторы элементов
│   │   ├── base_element.py  # Базовый класс для элементов
│   │   ├── buttons.py       # Специализированные кнопки
│   │   ├── links.py         # Специализированные ссылки
│   │   └── text_inputs.py   # Специализированные поля ввода
│   └── pages/               # Page Objects
│       └── login_page/      # Страница логина
│           └── login_page.py
├── tests/                   # Тесты и шаги
│   ├── conftest.py          # Фикстуры pytest
│   ├── features/            # Gherkin feature файлы
│   │   └── login_form.feature
│   ├── steps/               # Определения шагов
│   │   ├── common_steps.py  # Общие шаги
│   │   └── login_steps.py   # Шаги логина
│   └── test_login_form.py   # Тестовые файлы
├── pyproject.toml          # Конфигурация проекта
└── README.md               # Документация
```

## Основные зависимости

### Основные библиотеки:

- **pytest** (^8.0) - основной фреймворк для тестирования
- **pytest-bdd** (^8.1.0) - поддержка BDD сценариев
- **selenium** (^4.34.0) - автоматизация браузера
- **webdriver-manager** (^4.0.0) - автоматическое управление драйверами

### Инструменты разработки:

- **poetry** - управление зависимостями
- **ruff** (^0.4) - линтер и форматтер
- **black** (^24.4) - форматирование кода
- **mypy** (^1.10) - статическая типизация
- **pre-commit** (^4.2) - pre-commit хуки

## Быстрый старт

### Установка зависимостей

```bash
poetry install
```

### Запуск тестов

```bash
# Все тесты
poetry run python -m pytest tests/ -v

# Конкретный тест
poetry run python -m pytest tests/test_login_form.py::test_login_form_visibility -v

# UI тесты с определенным браузером
poetry run python -m pytest -m ui --browser=firefox -v

# Headless режим
poetry run python -m pytest --headless -v
```

## Пример использования

### Feature файл (Gherkin)

```gherkin
Feature: Login Form

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I fill in the email field with "user@example.com"
    And I fill in the password field with "password123"
    And I click the login button
    Then I should be logged in successfully
```

### Шаги (регистрируются как плагины)

```python
@when(parsers.parse('I fill in the email field with "{email}"'))
def fill_email_field(driver: WebDriver, email: str):
    login_page = LoginPage(driver)
    login_page.fill_email(email)
```

### Тестовый файл

```python
@pytest.mark.ui
@scenario("features/login_form.feature", "Successful login with valid credentials")
def test_successful_login():
    pass
```

## FYI - Ответы на вопросы

### Почему использованы такие селекторы?

В проекте используются CSS селекторы и XPath для поиска элементов. Хорошим тоном является добавление в DOM специальных
`data-qa` атрибутов для тестирования. Однако, если это невозможно, наиболее стабильными являются:

1. **Семантические селекторы** - `button[type="submit"]`, `input[type="email"]`
2. **CSS селекторы по атрибутам** - `ion-label[color="danger"]`
3. **XPath с семантическими условиями** - `//ion-label[contains(@class, "ion-color-danger")]`

**Рекомендации:**

- Используйте `data-qa="login-button"` атрибуты в DOM
- Предпочитайте CSS селекторы XPath для производительности

### Что еще можно добавить?

#### 1. Лучшая обработка исключений

```python
class ElementNotFoundException(Exception):
    pass


class BaseElement:
    def find(self) -> WebElement:
        try:
            return self.wait.safe_until(
                ex_con.presence_of_element_located((self.by, self.locator))
            )
        except TimeoutException:
            raise ElementNotFoundException(f"Element not found: {self.locator}")
```

#### 2. Параметризация тестов

```python
@pytest.mark.parametrize("email,password,expected", [
    ("valid@email.com", "password", "success"),
    ("invalid@email", "password", "validation_error"),
])
def test_login_scenarios(driver, email, password, expected):
# тест с параметрами
```

#### 3. Отчеты Allure

```python
import allure


@allure.step("Login with credentials")
def login(self, email: str, password: str) -> 'LoginPage':
    with allure.step(f"Fill email: {email}"):
        self.fill_email(email)
    with allure.step(f"Fill password: {password}"):
        self.fill_password(password)
    return self
```

#### 4. Дополнительные улучшения:

- **Retry механизм** для нестабильных элементов
- **Video recording** для отладки
- **Parallel execution** для ускорения тестов
- **Docker контейнеры** для CI/CD
- Сокрытие чувствительной информации в secret файлах

### Почему структура страниц разбита по директориям?

Структура разбита по директориям для лучшей организации кода, особенно для крупных веб-сервисов:

#### Преимущества:

1. **Модульность** - каждая страница в отдельной директории
2. **Масштабируемость** - легко добавлять новые страницы
3. **Изоляция** - компоненты страницы не конфликтуют
4. **Читаемость** - понятная структура проекта

#### Пример для сложной страницы:

```
pages/
├── dashboard/
│   ├── dashboard_page.py
│   ├── widgets/
│   │   ├── chart_widget.py
│   │   └── stats_widget.py
│   └── forms/
│       ├── settings_form.py
│       └── profile_form.py
└── login/
    └── login_page.py
```

Это позволяет:

- Разделить сложную логику на модули
- Переиспользовать компоненты между страницами
- Упростить поддержку и тестирование
- Следовать принципу единственной ответственности
