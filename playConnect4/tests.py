import unittest
import main

# TODO add before_all initialization for board

class TestWinningScenarios(unittest.TestCase):
    def test_horizontal_X_win(self):
        '''
        Test that it returns true for X horizontal winning scenario.
        :return: boolean
        '''
        board = main.create_board(main.COLUMN_COUNT, main.ROW_COUNT)
        main.drop_token(board, 'X', 0)
        main.drop_token(board, 'X', 1)
        main.drop_token(board, 'X', 2)
        main.drop_token(board, 'X', 3)
        main.print_board(board)
        result = main.check_horizontal(board, 'X')
        self.assertTrue(result)

    def test_vertical_X_win(self):
        '''
        Test that it returns true for X vertical winning scenario.
        :return: boolean
        '''
        board = main.create_board(main.COLUMN_COUNT, main.ROW_COUNT)
        main.drop_token(board, 'X', 0)
        main.drop_token(board, 'X', 0)
        main.drop_token(board, 'X', 0)
        main.drop_token(board, 'X', 0)
        result = main.check_vertical(board, 'X')
        self.assertTrue(result)

    def test_horizontal_O_win(self):
        '''
        Test that it returns true for O horizontal winning scenario.
        :return: boolean
        '''
        board = main.create_board(main.COLUMN_COUNT, main.ROW_COUNT)
        main.drop_token(board, 'O', 6)
        main.drop_token(board, 'O', 3)
        main.drop_token(board, 'O', 4)
        main.drop_token(board, 'O', 5)
        result = main.check_horizontal(board, 'O')
        self.assertTrue(result)

    def test_vertical_O_win(self):
        '''
        Test that it returns true for O vertical winning scenario.
        :return: boolean
        '''
        board = main.create_board(main.COLUMN_COUNT, main.ROW_COUNT)
        main.drop_token(board, 'O', 2)
        main.drop_token(board, 'O', 2)
        main.drop_token(board, 'O', 2)
        main.drop_token(board, 'O', 2)
        result = main.check_vertical(board, 'O')
        self.assertTrue(result)

    def test_horizontal_X_no_win(self):
        '''
        Test that it returns true for O vertical winning scenario.
        :return: boolean
        '''
        board = main.create_board(main.COLUMN_COUNT, main.ROW_COUNT)
        main.drop_token(board, 'X', 1)
        main.drop_token(board, 'X', 3)
        main.drop_token(board, 'X', 5)
        main.drop_token(board, 'X', 6)
        result = main.check_vertical(board, 'X')
        self.assertFalse(result)

    def test_vertical_X_no_win(self):
        '''
        Test that it returns true for O vertical winning scenario.
        :return: boolean
        '''
        board = main.create_board(main.COLUMN_COUNT, main.ROW_COUNT)
        main.drop_token(board, 'X', 2)
        main.drop_token(board, 'X', 2)
        main.drop_token(board, 'X', 2)
        result = main.check_vertical(board, 'X')
        self.assertFalse(result)

    def test_horizontal_O_no_win(self):
        '''
        Test that it returns true for O vertical winning scenario.
        :return: boolean
        '''
        board = main.create_board(main.COLUMN_COUNT, main.ROW_COUNT)
        main.drop_token(board, 'O', 2)
        main.drop_token(board, 'O', 1)
        main.drop_token(board, 'O', 3)
        main.drop_token(board, 'O', 5)
        result = main.check_vertical(board, 'O')
        self.assertFalse(result)

    def test_vertical_O_no_win(self):
        '''
        Test that it returns true for O vertical winning scenario.
        :return: boolean
        '''
        board = main.create_board(main.COLUMN_COUNT, main.ROW_COUNT)
        main.drop_token(board, 'O', 2)
        main.drop_token(board, 'O', 2)
        main.drop_token(board, 'O', 2)
        main.drop_token(board, 'O', 1)
        main.drop_token(board, 'O', 3)
        result = main.check_vertical(board, 'O')
        self.assertFalse(result)

    def test_limit_token_insert(self):
        '''
        Test that we can't exceed the column height limit with another token..
        :return: boolean
        '''
        board = main.create_board(main.COLUMN_COUNT, main.ROW_COUNT)
        while main.is_valid_move(board, 1):
            main.drop_token(board, 'O', 1)

        self.assertFalse(main.is_valid_move(board, 1))



if __name__ == '__main__':
    unittest.main()