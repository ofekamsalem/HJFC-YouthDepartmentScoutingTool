def get_team_id_name_map(league_id) -> dict:

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import re
    import time
    from utils.helper import load_config

    config = load_config()
    league_url = config["base league url en"].format(league_id=league_id)

    driver = webdriver.Chrome()
    driver.get(league_url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.table_row.link_url")))

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    team_dict = {}

    rows = driver.find_elements(By.CSS_SELECTOR, "a.table_row.link_url")
    

    for row in rows:
        href = row.get_attribute("href")
        divs = row.find_elements(By.TAG_NAME, "div")
        club_name = divs[1].text if len(divs) > 1 else ""
        club_name = club_name.replace("Team name\n", "")
        
        match = re.search(r'team_id=(\d+)', href)
        if match:
            team_id = match.group(1)
            team_dict[team_id] = club_name

    driver.quit()
    return team_dict

# result = get_team_id_name_map(40)
# print(result)

# WORKING!!!