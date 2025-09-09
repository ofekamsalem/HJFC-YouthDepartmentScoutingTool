from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse, parse_qs, urljoin
from selenium import webdriver
from utils.helper import load_config

    
def get_games_list(team_id):
    config = load_config()
    base_games_list_url = config['base team games url']
    games_list_url = base_games_list_url.format(team_id=team_id)
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver,20)
    driver.get(games_list_url)
    games_links = driver.find_elements(By.CSS_SELECTOR, "div.table_row_group a.table_row.link_url")
    games_id = []
    games_date = []
    games = {}
    for game in games_links:
        href = game.get_attribute('href')
        href = urljoin(games_list_url, href)
        q = parse_qs(urlparse(href).query)
        game_id = q.get("game_id", [""])[0]
        games_id.append(game_id)
        date_str = ""
        cells = game.find_elements(By.CSS_SELECTOR, "div.table_col.align_content")
        for cell in cells:
            spans = cell.find_elements(By.CSS_SELECTOR, "span.sr-only")
            if spans and spans[0].text.strip() == "תאריך":
                date_str = cell.text.replace(spans[0].text, "").strip().strip('"')
                games_date.append(date_str)
                break
        games[game_id] = date_str
    driver.quit()
    return games

