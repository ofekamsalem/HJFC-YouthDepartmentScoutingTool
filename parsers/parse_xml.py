import xml.etree.ElementTree as ET
import json

def load_config():
    tree = ET.parse("config/config.xml")
    root = tree.getroot()

    config = {
        "year": root.findtext("year"),
        "season id": root.findtext("season_id"),
        "base league url en": root.findtext("base_league_url_en"),
        "base club url en": root.findtext("base_club_url_en"),
        "base club url": root.findtext("base_club_url"),
        "base team url en": root.findtext("base_team_url_en"),
        "base team url": root.findtext("base_team_url"),
        "base game url": root.findtext("base_game_url"),
        "base player url": root.findtext("base_player_url"),
        "base team games url": root.findtext("base_team_games_url"),
        "base team_players list url": root.findtext("base_team_players_list_url"),
        "rules for unused players": {},
        "rules for key players": {},   # <-- add this
        "clubs": {},
    }

    # rules_for_unused_players
    unused = root.find("rules_for_unused_players")
    minutes = unused.find("minutes_percentages")
    rotation = unused.find("minutes_rank")

    config["rules for unused players"]["minutes percentages"] = {
        "minimum": minutes.findtext("minimum_percentages"),
        "maximum": minutes.findtext("maximum_percentages"),
    }
    config["rules for unused players"]["minutes rank"] = {
        "minimum": rotation.findtext("minimum_rank"),
        "maximum": rotation.findtext("maximum_rank"),
    }

    # rules_for_key_players
    key = root.find("rules_for_key_players")
    min_minutes = key.find("minimum_minutes_percentages")
    goals = key.find("goals")

    config["rules for key players"]["minimum minutes percentages"] = {
        "percentages": min_minutes.findtext("percentages"),
    }
    config["rules for key players"]["goals"] = {
        "minimum rank in scoring leaders table": goals.findtext("minimum_rank_in_scoring_leaders_table"),
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
