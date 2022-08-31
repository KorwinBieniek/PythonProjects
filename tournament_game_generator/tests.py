import unittest
import main

class TestTeamsNum(unittest.TestCase):
    def test_less_than_2(self):
        '''
        Test that it returns false for less than 2 teams.
        :return: boolean
        '''
        n_teams = 1
        result = main.validate_num_of_teams(n_teams)
        self.assertFalse(result)

    def test_2_teams(self):
        '''
        Test that it returns true for 2 teams.
        :return: boolean
        '''
        n_teams = 2
        result = main.validate_num_of_teams(n_teams)
        self.assertTrue(result)

    def test_more_than_2(self):
        '''
        Test that it returns false for more than 2 teams.
        :return: boolean
        '''
        n_teams = 4
        result = main.validate_num_of_teams(n_teams)
        self.assertTrue(result)

class TestTeamsName(unittest.TestCase):
    def test_proper_name(self):
        '''
        Test that it returns true for proper team name.
        :return: boolean
        '''
        name = 'Java Script'
        result = main.validate_name(name)
        self.assertTrue(result)

    def test_more_than_2_words(self):
        '''
        Test that it returns false for more than 2 words in team name.
        :return: boolean
        '''
        name = 'C Is Best'
        result = main.validate_name(name)
        self.assertFalse(result)

    def test_no_words(self):
        '''
        Test that it returns false for no words in team name.
        :return: boolean
        '''
        name = ''
        result = main.validate_name(name)
        self.assertFalse(result)

    def test_less_than_two_characters(self):
        '''
        Test that it returns false for less than 2 characters in team name.
        :return: boolean
        '''
        name = 'C'
        result = main.validate_name(name)
        self.assertFalse(result)

class TestGamesPlayedNum(unittest.TestCase):
    def test_no_games(self):
        '''
        Test that it returns false for less than n_teams - 1 games.
        :return: boolean
        '''
        games = 0
        result = main.validate_num_of_games(games, 2)
        self.assertFalse(result)

    class TestTeamsName(unittest.TestCase):
        def test_proper_num_of_games(self):
            '''
            Test that it returns true for n_teams - 1 games.
            :return: boolean
            '''
            games = 3
            result = main.validate_num_of_games(games, 4)
            self.assertTrue(result)

class TestWinsNum(unittest.TestCase):
    def test_negative_wins(self):
        '''
        Test that it returns false for less than 0 wins.
        :return: boolean
        '''
        wins = -1
        result = main.validate_wins(wins, 4)
        self.assertFalse(result)

    class TestTeamsName(unittest.TestCase):
        def test_more_than_num_games_wins(self):
            '''
            Test that it returns false for more than n_teams wins.
            :return: boolean
            '''
            wins = 5
            result = main.validate_wins(wins, 4)
            self.assertFalse(result)

    def test_proper_num_of_wins(self):
        '''
        Test that it returns true for proper num of wins.
        :return: boolean
        '''
        wins = 3
        result = main.validate_wins(wins, 4)
        self.assertTrue(result)

class TestFirstRoundTeams(unittest.TestCase):
    def test_6_proper_teams(self):
        '''
        Test that it returns proper list of tuples for teams in the first round.
        :return: list
        '''
        teams = {'AA': 1, 'BB': 4, 'CC': 3, 'DD': 4, 'EE': 2, 'FF': 5}
        teams_list = [('FF', 'AA'), ('BB', 'EE'), ('DD', 'CC')]
        result = main.generate_first_round(teams)
        self.assertEqual(result, teams_list)

    def test_4_proper_teams(self):
        '''
        Test that it returns proper list of tuples for teams in the first round.
        :return: list
        '''
        teams = {'Python': 2, 'Ruby': 1, 'JavaScript': 0, 'C#': 3}
        teams_list = [('C#', 'JavaScript'), ('Python', 'Ruby')]
        result = main.generate_first_round(teams)
        self.assertEqual(result, teams_list)

if __name__ == '__main__':
    unittest.main()