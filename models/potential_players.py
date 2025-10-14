from utils.helper import load_config
from .team import Team
from .player import Player



def get_potential_players(type: int,team: Team) -> list[Player]:
    config = load_config()
    rules_for_unused_players = config["rules for unused players"]

    min_percentages = int(rules_for_unused_players["minutes percentages"]["minimum"])
    max_percentages = int(rules_for_unused_players["minutes percentages"]["maximum"])
    min_rank = int(rules_for_unused_players["minutes rank"]["minimum"])
    max_rank = int(rules_for_unused_players["minutes rank"]["maximum"])
    rules_for_key_players = config["rules for key players"]
    mins_percentages_for_key_players = int(rules_for_key_players["minimum minutes percentages"]["percentages"])
    minimum_goals = int(rules_for_key_players["goals"]["minimum rank in scoring leaders table"])
    potential_players = []
    team.calc_minutes_percentage_for_each_player()
    team.calc_minutes_rank_for_each_player()
    team.calc_scoring_rank_for_each_player()
    
    for player in team.team_players.values():
            mins_percentages = player.minutes_percentage
            mins_rank = player.minutes_rank
            scoring_rank = player.goals_rank
            played_under_90_mins = player.has_played_under_90_minutes_in_last_3_games()
            in_squad_last_3_games = player.in_squad_last_3_games()
            not_started_last_3_games = player.not_started_in_last_3_games()

            if type == 1 and min_percentages <= mins_percentages <= max_percentages and min_rank <= mins_rank <= max_rank and played_under_90_mins and in_squad_last_3_games and not_started_last_3_games:
                potential_players.append(player) 
                return potential_players

            if type == 2 and mins_percentages >= mins_percentages_for_key_players and player.age_group < team.age_group:
                 potential_players.append(player)
                 return potential_players
            
            if type == 3 and scoring_rank <= minimum_goals:
                 potential_players.append(player)
    return potential_players
