from selenium import webdriver
from selenium.webdriver.common.by import By
from spellchecker import SpellChecker
import time

# Инициализация веб-драйвера
driver = webdriver.Chrome()  # Убедитесь, что ChromeDriver находится в PATH или укажите путь к нему

# Инициализация проверщика орфографии
spell = SpellChecker(language='ru')

def check_spelling(text):
    """Проверяет текст на орфографические ошибки."""
    words = text.split()
    misspelled = spell.unknown(words)
    return misspelled

try:
    # Открытие главной страницы
    driver.get("https://nexign.com/ru")
    time.sleep(2)  # Ждем загрузки страницы

    # Список для хранения URL всех страниц
    visited_urls = set()
    urls_to_check = ["https://nexign.com/ru"]

    while urls_to_check:
        current_url = urls_to_check.pop(0)
        if current_url in visited_urls:
            continue  # Пропускаем уже проверенные страницы

        print(f"Проверка страницы: {current_url}")
        visited_urls.add(current_url)

        # Переход на страницу
        driver.get(current_url)
        time.sleep(2)

        # Получение текстового контента страницы
        page_content = driver.find_element(By.TAG_NAME, "body").text

        # Проверка орфографии
        misspelled_words = check_spelling(page_content)
        if misspelled_words:
            print(f"Орфографические ошибки на странице {current_url}: {misspelled_words}")
        else:
            print(f"На странице {current_url} ошибок не обнаружено.")

        # Сбор ссылок со страницы
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and "https://nexign.com/ru" in href and href not in visited_urls:
                urls_to_check.append(href)

        # Ограничение на количество проверяемых страниц (например, первые 5)
        if len(visited_urls) >= 5:
            break

finally:
    # Закрытие браузера
    driver.quit()