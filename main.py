from models.potential_players import get_potential_players
from scrapers.team_selection import select_team
from models.team_creation import create_team
from utils.export_to_html import export
from scrapers.teams_names_and_ids_scraper import get_team_id_name_map
from models.team import Team

# def create_team(team_details) -> Team:
#     team_name = ""
#     team_id = team_details['team id']
#     club_name = team_details['team_id']
#     club_id = "" 
#     team = Team(club_name, club_id, team_name, team_id)

def main():
    print("Select the type of players you want to analyze:")
    print("1. Rotation-edge players - those with relatively low playing minutes compared to the rest of the squad")
    print("2. Those playing above their age group")
    print("3. Top scorers")

    type = int(input("> "))

    choice = int(input("Select mode:\n" "1. Run on a specific league (enter league ID)\n"  "2. Run on predefined teams\n" "> "))
    if choice == 1:
        teams_dict = get_team_id_name_map(input("Enter league ID: "))
        for team_id, club_name in teams_dict.items():
            team_details = {
                "team name": "",          
                "team id": team_id,       
                "club name": club_name,   
                "club id": ""             
            }
            team = create_team(team_details)
            team.parse_games()
            players = get_potential_players(type,team)
            export(players)
    else:    
        team_details = select_team()
        team = create_team(team_details)
        team.parse_games()
        players = get_potential_players(type, team)
        export(players)
    


if __name__ == '__main__':
    main()
