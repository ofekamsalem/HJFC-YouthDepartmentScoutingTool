from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urljoin
from utils.helper import load_config

    
def get_details(club_id) -> str:
    driver = webdriver.Chrome()
    config = load_config()
    base_club_url = config['base club url']
    club_url = base_club_url.format(club_id=club_id)
    driver.get(club_url)
    club_name = driver.find_element(By.CSS_SELECTOR, "h1.page_main_title span.big").text
    # articles = driver.find_elements(By.CSS_SELECTOR, "article.field-item a")
    wait = WebDriverWait(driver, 20)

    # Wait until the active-teams section exists and at least 2 cards are rendered
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.active-teams")))
    wait.until(lambda drv: len(
        drv.find_elements(By.CSS_SELECTOR, "section.active-teams article.field-item")
    ) >= 2)

    # Pick the 2nd article directly, then its link
    second_article = driver.find_element(
        By.CSS_SELECTOR,
        "section.active-teams article.field-item:nth-of-type(2)"
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", second_article)

    link = second_article.find_element(By.CSS_SELECTOR, "a[href*='team-details']")
    href = link.get_attribute("href")

    team_id = parse_qs(urlparse(href).query).get("team_id", [""])[0]
    print(team_id)
    driver.quit()
    return club_name



# it works!
def select_option(options, include_other=True):
    for index, option in enumerate(options, 1):
        print(f"{index}. {option}")
    if include_other:
        print("5. Other")

    while True:
        choice = int(input("> "))
        if 1 <= choice <= len(options):
            # user picked one of the options
            return {"value": options[choice - 1], "is_other": False}
        elif include_other and choice == 5:
            club_id = input("Enter club ID: ")
            return {"value": club_id, "is_other": True}
        else:
            print("enter a valid number")


# Select a team:
def select_team() -> dict:
    config = load_config()

    # 1) Select club: always show 4 clubs + "5. Other"
    clubs_names = list(config["clubs"].keys())[:4]  # ensure 4 options max
    print('Select a club: enter a number from 1-5')
    club_selection = select_option(clubs_names, include_other=True)

    if club_selection["is_other"]:
        # User entered a club ID manually -> don't read club id from config
        #TODO: fix this
        entered_club_id = club_selection["value"]
        print(entered_club_id)
        print("bbbbbbbbbbbb")
        print(get_details(entered_club_id))
        print("bb")
    
    chosen_club = club_selection["value"]
    print(f"\nSelected club: {chosen_club}\n")
    club_id = config['clubs'][chosen_club]['club id']

    club_teams = config['clubs'][chosen_club]['club teams']
    team_names = [team['team name'] for team in club_teams]
    print('Select a team: enter a number from 1-4')
    team_selection = select_option(team_names, include_other=False)
    chosen_team = team_selection["value"]
    team_id = None
    for team in club_teams:
        if team['team name'] == chosen_team:
            team_id = team['team id']
            break
    print(f"\nSelected team: {chosen_team}\n")

    print('Scraping in progress, HTML file will be ready soon...')
    team_details = {
        'club name': chosen_club,
        'club id': club_id,
        'team name': chosen_team,
        'team id': team_id,
    }
    return team_details

