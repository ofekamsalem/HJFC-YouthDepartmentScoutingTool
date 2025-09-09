from models.potential_players import get_potential_players
from scrapers.team_selection import select_team
from models.team_creation import create_team
from utils.export_to_html import export


def main():
    team_details = select_team()
    team = create_team(team_details)
    team.parse_games()
    players = get_potential_players(team)
    export(players)
    


if __name__ == '__main__':
    main()
