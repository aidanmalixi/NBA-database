from balldontlie import BalldontlieAPI

api = BalldontlieAPI(api_key = '0cebf21e-052e-460d-ae94-110a22d5e1a6')

# print(dir(api))

# print(dir(api.nba))

teams = api.nba.games.list().data
print(teams)


