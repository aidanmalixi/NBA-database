import os
import pandas as pd
from balldontlie import BalldontlieAPI

class Fetcher:
    def __init__(self, api_key=None):
        self.api = BalldontlieAPI(api_key=api_key)

    def get_players(self, search_name=None, per_page=100):
        collection = {"per_page": per_page}
        if search_name:
            collection["search"] = search_name
        return self.api.nba.players.list(**collection).data
    
    def get_teams(self):
        return self.api.nba.teams.list().data
    
    def get_games(self, season="2024", per_page=100):
        return self.api.nba.games.list(seasons=[season], per_page=per_page).data
    
    def to_csv(self, data, out_path):
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        pd.DataFrame(data).to_csv(out_path, index=False)
        print(f"Saved to {out_path}")

if __name__ == "__main__":
    api_key = "0cebf21e-052e-460d-ae94-110a22d5e1a6"
    fetcher = Fetcher(api_key)

    # teams = fetcher.get_teams()
    # fetcher.to_csv(teams, "data/raw/nba_teams.csv")

    # games = fetcher.get_games(season=2024)
    # fetcher.to_csv(games, "data/raw/nba_games_2024.csv")

    players = fetcher.get_players(search_name="wembanyama")
    fetcher.to_csv(players, "data/raw/wemby.csv")