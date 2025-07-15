import os
import pandas as pd
import boto3
from io import StringIO
from balldontlie import BalldontlieAPI

class Fetcher:
    def __init__(self, api_key=None, aws_bucket=None):
        self.api = BalldontlieAPI(api_key=api_key)
        self.s3_bucket = aws_bucket
        self.s3_client = boto3.client('s3')

    def get_players(self, search_name=None, per_page=100):
        collection = {"per_page": per_page}
        if search_name:
            collection["search"] = search_name
        return self.api.nba.players.list(**collection).data
    
    def get_teams(self):
        return self.api.nba.teams.list().data
    
    def get_games(self, season="2024", per_page=100):
        return self.api.nba.games.list(seasons=[season], per_page=per_page).data
    
    def to_s3_csv(self, data, s3_key):
        if data and hasattr(data[0], "model_dump"):
            data = [item.model_dump() for item in data]

        csv_buffer = StringIO()
        pd.DataFrame(data).to_csv(csv_buffer, index=False)

        self.s3_client.put_object(
            Bucket=self.s3_bucket,
            Key=s3_key,
            Body=csv_buffer.getvalue()
        )
        print(f"✅ Uploaded to s3://{self.s3_bucket}/{s3_key}")

if __name__ == "__main__":
    api_key = "0cebf21e-052e-460d-ae94-110a22d5e1a6"
    aws_bucket = "nba-csv-bucket"

    fetcher = Fetcher(api_key, aws_bucket)

    teams = fetcher.get_teams()
    fetcher.to_s3_csv(teams, "nba_data/nba_teams.csv")

    games = fetcher.get_games(season=2024)
    fetcher.to_s3_csv(games, "nba_data/nba_games_2024.csv")

    players = fetcher.get_players(search_name="wembanyama")
    fetcher.to_s3_csv(players, "nba_data/wemby.csv")
