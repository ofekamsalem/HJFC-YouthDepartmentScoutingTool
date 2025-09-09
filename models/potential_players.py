from utils.helper import load_config
from .team import Team

     

def get_potential_players(team: Team) -> list:
    config = load_config()
    rules = config["rules for unused players"]

    min_percentages = int(rules["minutes percentages"]["minimum"])
    max_percentages = int(rules["minutes percentages"]["maximum"])
    min_rank = int(rules["minutes rank"]["minimum"])
    max_rank = int(rules["minutes rank"]["maximum"])
    potential_players = []
    team.calc_minutes_percentage_for_each_player()
    team.calc_minutes_rank_for_each_player()
    for player in team.team_players.values():
            mins_percentages = player.minutes_percentage
            mins_rank = player.minutes_rank
            played_under_90_mins = player.has_played_under_90_minutes_in_last_3_games()
            in_squad_last_3_games = player.in_squad_last_3_games()
            not_started_last_3_games = player.not_started_in_last_3_games()
            if min_percentages <= mins_percentages <= max_percentages and min_rank <= mins_rank <= max_rank and played_under_90_mins and in_squad_last_3_games and not_started_last_3_games:
                potential_players.append(player) 
    return potential_players

