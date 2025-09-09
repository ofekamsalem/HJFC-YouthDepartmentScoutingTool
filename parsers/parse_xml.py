
import xml.etree.ElementTree as ET
import json

def load_config():
    tree = ET.parse("config.xml")
    root = tree.getroot()

    config = {
        "year": root.findtext("year"),
        "season id": root.findtext("season_id"),
        "base club url": root.findtext("base_club_url"),
        "base team url": root.findtext("base_team_url"),
        "base game url": root.findtext("base_game_url"),
        "base player url": root.findtext("base_player_url"),
        "base team games url": root.findtext("base_team_games_url"),
        "base team_players list url": root.findtext("base_team_players_list_url"),
        "rules for unused players": {},   
        "clubs": {},
    }

    # rules_for_unused_players
    rules = root.find("rules_for_unused_players")
    minutes = rules.find("minutes_percentages")
    rotation = rules.find("minutes_rank")

    config["rules for unused players"]["minutes percentages"] = {
        "minimum": minutes.findtext("minimum_percentages"),
        "maximum": minutes.findtext("maximum_percentages"),
    }

    config["rules for unused players"]["minutes rank"] = {
        "minimum": rotation.findtext("minimum_rank"),
        "maximum": rotation.findtext("maximum_rank"),
    }

    # clubs
    for club in root.find("clubs").findall("club"):
        club_name = club.findtext("name")
        club_id = club.findtext("club_id")
        teams = []
        for team in club.find("teams").findall("team"):
            teams.append({
                "team name": team.findtext("name"),
                "team id": team.findtext("team_id"),
            })
        config["clubs"][club_name] = {
            "club id": club_id,
            "club teams": teams,
        }

    return config

cfg = load_config()

with open("config.json", "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=4, ensure_ascii=False)

print("Wrote config.json successfully")
