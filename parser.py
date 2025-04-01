from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def find_by_nickname():
    nickname = "RailNur"
    region = "EU"
    leaderboard = "battlegrounds"
    max_pages = 600
    found = False
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Передаём service, а не строку

    driver.get(
        f"https://hearthstone.blizzard.com/en-us/community/leaderboards/?region={region}&leaderboardId={leaderboard}")

    try:
        for page in range(2, max_pages-1):
            print(f"Проверяем страницу {page-1}...")

            # Ждём загрузки таблицы
            r = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#leaderBoardsTable > div.LeaderboardsTable-Rendered"))
            )

            # Получаем все строки таблицы
            lines = r.text.split('\n')


            try:
                index = lines.index(nickname)  # Пытаемся найти индекс
                found = True  # Если не было исключения, значит, строка найдена
            except ValueError:
                found = False  # Если строка не найдена

            if found:
                line_before = lines[index - 1]
                line_after = lines[index + 1]
                print(f"Место в рейтинге: {line_before}")
                print(f"ММР: {line_after}")
                break
            else:
                try:
                    driver.get(
                        f"https://hearthstone.blizzard.com/en-us/community/leaderboards/?region={region}&leaderboardId={leaderboard}&page={page}")
                except Exception as er:
                    print(f"Ошибка переходе на страницу {page}: {str(er)}")
        if not found:
            print('Не нашли')

    finally:
        driver.quit()


if __name__ == "__main__":
    find_by_nickname()
