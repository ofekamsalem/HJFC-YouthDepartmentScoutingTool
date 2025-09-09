# from models.update_player_attributes import get_potential_players
from datetime import datetime
from dataclasses import fields
import html
from models.player import Player

def export(players):
    cols = [f.name for f in fields(Player) if f.name != "involvements" and f.name != "club_id" and f.name != "team_id"]



    hebrew_headers = {
        "club_name": "שם מועדון",
        "team_name": "שכבת גיל",
        "player_name": "שם שחקן",
        "age_group": "שנתון",
        "player_id": "מזהה שחקן",
        "total_minutes": "סך הכל דקות",
        "minutes_percentage": "אחוז דקות",
        "minutes_rank": "דירוג ברוטציה",
        "total_goals": "שערים"
    }

    title = "שחקנים פוטנציאלים למחלקת נוער בהפועל ירושלים"

    html_parts = [
        "<!doctype html>",
        '<html lang="he" dir="rtl">',
        "<head>",
        '  <meta charset="UTF-8">',
        f"  <title>{html.escape(title)}</title>",
        "  <style>",
        "    body { font-family: Arial, sans-serif; background:#f7f7f7; margin:0; }",
        "    .container { max-width: 1100px; margin: 40px auto; background:#fff; padding: 24px; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.08); }",
        "    h1 { text-align:center; margin-top:0; }",
        "    table { width:100%; border-collapse: collapse; margin-top:20px; }",
        "    th, td { border:1px solid #ddd; padding: 8px; text-align: right; }",
        "    th { background:#fafafa; }",
        "    tr:hover { background:#fcfcfc; }",
        "  </style>",
        "</head>",
        "<body>",
        '  <div class="container">',
        f"    <h1>{html.escape(title)}</h1>",
        f'    <div style="text-align:center;color:#666;">נוצר בתאריך {datetime.now().strftime("%d-%m-%Y, %H:%M")}</div>',
        "    <table>",
        "      <thead>",
        "        <tr>",
    ]

    for c in cols:
        html_parts.append(f"          <th>{html.escape(hebrew_headers.get(c, c))}</th>")

    html_parts += [
        "        </tr>",
        "      </thead>",
        "      <tbody>",
    ]

    for p in players:
        html_parts.append("        <tr>")
        for c in cols:
            val = getattr(p, c)
            if c == "minutes_percentage":
                try:
                    val_str = f"{float(val):.1f}%"
                except Exception:
                    val_str = str(val)
            else:
                val_str = str(val)
            html_parts.append(f"          <td>{html.escape(val_str)}</td>")
        html_parts.append("        </tr>")

    html_parts += [
        "      </tbody>",
        "    </table>",
        "  </div>",
        "</body>",
        "</html>",
    ]

    html_content = "\n".join(html_parts)

    filename = "players_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("New file:", filename)