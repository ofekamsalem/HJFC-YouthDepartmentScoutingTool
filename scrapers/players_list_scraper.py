from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse, parse_qs, urljoin
from selenium import webdriver
from utils.helper import load_config

""""
it works! we have dict of players with names and their IDS
"""


from selenium.webdriver.support import expected_conditions as EC

def get_players_names_and_ID(team_id) -> dict:
    config = load_config()
    base_team_url = config['base team url']
    team_url = base_team_url.format(team_id=team_id)
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver,20)
    driver.get(team_url)
    # wait for container and scroll into view
    container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.players-statistics-container")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)

    # collect rows
    rows = wait.until(EC.presence_of_all_elements_located((
        By.CSS_SELECTOR,
        "section.players-statistics-container a.table_row.link_url, "
        "section.players-statistics-container .table_row.link_url"
    )))

    players = {}

    for row in rows:
        href = row.get_attribute("href")
        href = urljoin(driver.current_url, href)
        qs = parse_qs(urlparse(href).query)
        player_id = qs.get("player_id", [""])[0]
        # extract player name
        name = None
        for col in row.find_elements(By.CSS_SELECTOR, "div.table_col"):
            labels = [el.text.strip() for el in col.find_elements(By.CSS_SELECTOR, "span.sr-only")]
            if any(lbl in ("שם השחקן", "שם שחקן") for lbl in labels):
                txt = col.text.strip()
                for lbl in ("שם השחקן", "שם שחקן"):
                    txt = txt.replace(lbl, "")
                name = txt.strip().strip('"')
                break
        if name:
            players[player_id] = name
    driver.quit()
    return players


