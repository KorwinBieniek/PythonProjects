def input_num_of_teams():
    while True:
        n_teams = int(input('Enter the number of teams in the tournament: '))
        if validate_num_of_teams(n_teams):
            return n_teams


def validate_num_of_teams(n_teams):
    if n_teams < 2:
        print('The minimum number of teams is 2, try again.')
        return False
    return True


def name_teams(n_teams):
    teams = {}
    num = 0
    while num < n_teams:
        team_name = input(f'Enter the name for team #{num + 1}: ')
        if validate_name((team_name)):
            teams[team_name] = 0
            num += 1
    return teams


def validate_name(team_name):
    if len(team_name) < 2:
        print('Team names must have at least 2 characters, try again.')
        return False
    elif len(team_name.split()) > 2:
        print('Team names may have at most 2 words, try again.')
        return False
    return True


def number_of_games_played(n_teams):
    while True:
        n_games = int(input('Enter the number of games played by each team: '))
        if validate_num_of_games(n_games, n_teams):
            return n_games


def validate_num_of_games(n_games, n_teams):
    if n_games < n_teams - 1:
        print('Invalid number of games. Each team plays each other at least once in the regular season, try again.')
        return False
    return True


def number_of_wins_for_team(teams, n_games):
    for k in teams.keys():
        while True:
            n_wins = int(input(f'Enter the number of wins Team {k} had: '))
            if validate_wins(n_wins, n_games):
                teams[k] = n_wins
                break
    return teams


def validate_wins(n_wins, n_games):
    if n_wins < 0:
        print('The minimum number of wins is 0, try again.')
        return False
    elif n_wins > n_games:
        print(f'The maximum number of wins is {n_games}, try again.')
        return False
    return True


def generate_first_round(teams):
    team_sorted_by_wins = sorted(teams, key=teams.get, reverse=True)

    return [
        (team_sorted_by_wins[i], team_sorted_by_wins[-i - 1])
        for i in range(len(team_sorted_by_wins) // 2)
    ]


def print_first_round(team_pairs):
    for pair in team_pairs:
        print(f'Home: {pair[1]} VS Away: {pair[0]}')


def main():
    n_teams = input_num_of_teams()
    teams = name_teams(n_teams)
    n_games = number_of_games_played(n_teams)
    teams = number_of_wins_for_team(teams, n_games)
    print('Generating the games to be played in the first round of the tournament...')
    team_pairs = generate_first_round(teams)
    print_first_round(team_pairs)

if __name__ == '__main__':
    main()
