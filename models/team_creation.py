from scrapers.team_selection import select_team
from scrapers.players_list_scraper import get_players_names_and_ID
from scrapers.games_list_scraper import get_games_list
from .team import Team
from .player import Player
from .game import Game



# work! we have a new Team object
def create_team(team_details: dict) -> Team:
    # team_dict = select_team()
    team_name = team_details['team name']
    team_id = team_details['team id']
    club_name = team_details['club name']
    club_id = team_details['club id'] 
    team = Team(club_name, club_id, team_name, team_id)
    team.set_team_age_group()
    players_names_and_ID = get_players_names_and_ID(team.team_id)
    games_ID = get_games_list(team.team_id)

    # create Player objects:
    for player_id, player_name in players_names_and_ID.items():
        player = Player(team.club_name,team.club_id,team.team_name,team.team_id,player_id,player_name)
        team.add_player(player)

    team.set_age_group_for_each_player()

    for game_id, date in games_ID.items():
        game = Game(game_id,date)
        team.add_game(game)

    return team

