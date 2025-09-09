from dataclasses import dataclass, field
from .player import Player
from .player import AgeGroup
# from parsers.parse_game import parse_games
from .game import Game
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import Optional, List
from utils.helper import load_config





def _age_to_group(age: int) -> AgeGroup | None:
    # Map age → AgeGroup (tweak the rules if your league uses different cutoffs)
    if age >= 18:
        return AgeGroup.U19
    if age == 17:
        return AgeGroup.U17
    if age == 16:
        return AgeGroup.U16
    if age == 15:
        return AgeGroup.U15
    return None

def get_team_age_group(team_name: str) -> AgeGroup | None:
    match team_name:  
        case "U19":
            return AgeGroup.U19
        case "Youth A":
            return AgeGroup.U17
        case "Youth B":
            return AgeGroup.U16
        case "Youth C":
            return AgeGroup.U15
        case _:
            return None  

@dataclass
class Team:
    club_name: str
    club_id: str
    team_name: str
    team_id: str
    age_group: Optional[AgeGroup] = None
    team_players: dict[str, Player] = field(default_factory=dict)
    games: List[Game] = field(default_factory=list)     


    # add a player to the team's dictionary (key: player_id, value: Player)
    def add_player(self, Player):
        self.team_players[Player.player_id] = Player

    # get the player with the most total minutes
    def max_minutes_of_all_players(self) -> Player:
        top_player = max(self.team_players.values(), key=lambda p: p.total_minutes)
        return top_player

    # add a game to the team's games list
    def add_game(self, game: Game) -> None:
        self.games.append(game)

    def parse_games(self) -> None:
        from parsers.parse_game import parse_games
        parse_games(self)

    # for each player, calculate minutes percentage relative to the top-minutes player
    def calc_minutes_percentage_for_each_player(self) -> None:
        max_minutes_player = self.max_minutes_of_all_players()
        for player in self.team_players.values():
            player.minutes_percentage = 100 * (player.total_minutes / max_minutes_player.total_minutes)
    
    # for each player, calculate player position in table relative to the top-minutes player
    def calc_minutes_rank_for_each_player(self) -> None:
        players_sorted_by_minutes = sorted(self.team_players.values(), key=lambda p: p.total_minutes, reverse=True)
        for index, player in enumerate(players_sorted_by_minutes, start=1):
            player.minutes_rank = index
    
    # set group age of the team
    def set_team_age_group(self) -> None:
        self.age_group = get_team_age_group(self.team_name)

    
    def set_age_group_for_each_player(self) -> None:
        driver = webdriver.Chrome()
        config = load_config()
        season_year = int(config["year"])
        base_player_url = config["base player url"]
        for pid in self.team_players.keys():
            player_url = base_player_url.format(player_id=pid)
            driver.get(player_url)
            data_list = driver.find_element(By.CSS_SELECTOR, "ul.new-player-card_data-list")
            lis = data_list.find_elements(By.TAG_NAME, "li")
            birth_text = lis[0].text   
            year_of_birth = int(birth_text.split()[-1].split("/")[1])
            age = season_year - year_of_birth
            self.team_players[pid].age_group = _age_to_group(age) 
        driver.quit()

            
    



    

    



