from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urljoin
from utils.helper import load_config
import re



def get_club_details(club_id) -> dict:
    config = load_config()
    base_club_url_for_name = config["base club url en"]
    club_url_for_name = base_club_url_for_name.format(club_id=club_id)

    driver = webdriver.Chrome()
    driver.get(club_url_for_name)
    wait = WebDriverWait(driver, 20)
    club_name = driver.find_element(By.CSS_SELECTOR, "h1.page_main_title span.big").text
    driver.quit()

    base_club_url = config["base club url"]
    club_url = base_club_url.format(club_id=club_id)
    driver = webdriver.Chrome()
    driver.get(club_url)
    links = driver.find_elements(By.CSS_SELECTOR, "article.field-item a[href*='team_id']")

    # extract IDs from href attributes
    team_ids = []
    for link in links[1:5]:
        href = link.get_attribute("href")
        # Extract team_id using regex
        match = re.search(r'team_id=(\d+)', href)
        team_ids.append(match.group(1))
    club = dict(
    club_name=club_name,
    U19_ID=team_ids[0],
    U17_ID=team_ids[1], 
    U16_ID=team_ids[2],
    U15_ID=team_ids[3]
    )
    print(club)
    driver.quit()
    return club




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
            print("Enter a valid number")


# Select a team:
def select_team() -> dict:
    config = load_config()

    # 1) Select club: always show 4 clubs + "5. Other"
    clubs_names = list(config["clubs"].keys())[:4]  # ensure 4 options max
    print('Select a club: enter a number from 1-5')
    club_selection = select_option(clubs_names, include_other=True)
    team_names = ["U19", "U17", "U16", "U15"]

    # User entered a club ID manually -> don't read club id from config
    if club_selection["is_other"]:
        entered_club_id = club_selection["value"]
        club_id = entered_club_id
        club = get_club_details(entered_club_id)
        chosen_club = club["club_name"]
        print(f"\nSelected club: {chosen_club}\n")

        ids = list(club.values())[1:]  # skip first value (club_name)
        teams_dict = dict(zip(team_names, ids))
        print('Select a team: enter a number from 1-4')
        team_selection = select_option(team_names,include_other=False)
        chosen_team = team_selection["value"]
        team_id = teams_dict[chosen_team]
        print(f"\nSelected team: {chosen_team}\n")

        
    else:
        # get club ID:
        chosen_club = club_selection["value"]
        print(f"\nSelected club: {chosen_club}\n")
        club_id = config['clubs'][chosen_club]['club id']
        club_teams = config['clubs'][chosen_club]['club teams']
        print('Select a team: enter a number from 1-4')
        team_selection = select_option(team_names, include_other=False)
        chosen_team = team_selection["value"]
        team_id = None
        for team in club_teams:
            if team['team name'] == chosen_team:
                team_id = team['team id']
                break
        print(f"\nSelected team: {chosen_team}\n")

    team_details = {
            'club name': chosen_club,
            'club id': club_id,
            'team name': chosen_team,
            'team id': team_id,
        }
    print('Scraping in progress, HTML file will be ready soon...')

    return team_details

