from dataclasses import dataclass, field
from .involvement import Involvement
from typing import Optional, List

MAX_MINUTES_LAST_3_GAMES = 90

from enum import IntEnum

class AgeGroup(IntEnum):
    U19 = 19
    U17 = 17
    U16 = 16
    U15 = 15

@dataclass
class Player:
    club_name: str
    club_id: str
    team_name: str
    team_id: str
    player_id: str
    player_name: str
    age_group: Optional[AgeGroup] = None
    total_minutes: int = field(init=False, default=0)
    minutes_percentage: float = 0.0  
    minutes_rank: int = 0
    total_goals: int = 0
    goals_rank: int  = 0
    involvements: List[Involvement] = field(default_factory=list)  

    # calculate total minutes the player has played
    @property
    def calc_total_minutes(self) -> int:
        return sum([inv.minutes for inv in self.involvements])
    
    # check if the player didn't start in the last 3 games, if he start the player is not for us if he didn't it's ok
    def not_started_in_last_3_games(self) -> bool:
        for inv in self.involvements[-3:]:
            if inv.started == True:
                return False
        return True
    
    # check if the player was in the squad in at least one of the last 3 games if he was in the squad for at least 1 game it's ok
    def in_squad_last_3_games(self) -> bool:
        for inv in self.involvements[-3:]:
            if inv.in_squad == True:
                return True   
        return False  
    
    # check if the player played fewer than 90 total minutes in the last 3 games
    def has_played_under_90_minutes_in_last_3_games(self) -> bool:
        if sum(inv.minutes for inv in self.involvements[-3:]) < MAX_MINUTES_LAST_3_GAMES:
            return True
        else:
            return False
    
    def add_game(self, game_ID: str, date: str, started: bool, in_squad: bool, subbed_in: bool, subbed_out: bool, subbed_in_min: Optional[int] = None, subbed_out_min: Optional[int] = None,goals = 0):
        inv = Involvement(
            game_ID=game_ID,
            date=date,
            started=started,
            in_squad=in_squad,
            subbed_in=subbed_in,
            subbed_out=subbed_out,
            subbed_in_min=subbed_in_min,
            subbed_out_min=subbed_out_min,
            goals=goals
        )
        self.involvements.append(inv)
        self.total_minutes += inv.minutes
        self.total_goals += inv.goals

