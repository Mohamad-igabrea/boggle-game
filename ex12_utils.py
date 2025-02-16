
from copy import deepcopy
from boggle_board_randomizer import LETTERS, randomize_board


def load_words_dict(file):
    milon = open(file)
    lines = set(line.strip() for line in milon.readlines())
    milon.close()
    return lines


def help_filtered_words(coord, word, counter, path_word, all_coord, board):
    if word == path_word:
        return True
    if counter == len(word):
        return False
    for row in range(coord[0] - 1, coord[0] + 2):
        for col in range(coord[1] - 1, coord[1] + 2):
            if (row < 0 or row > 3) or (col < 0 or col > 3) or ((row, col) in all_coord):
                continue
            big_n_word = ""
            for i in range(len(board[row][col])):
                if len(word) > counter + i:
                    big_n_word = big_n_word + word[counter + i]
                else:
                    break
            if board[row][col] == big_n_word:
                if help_filtered_words((row, col), word, counter + len(board[row][col]), path_word
                                                    + big_n_word, all_coord + [(row, col)], board):
                    return True


def filtered_words(all_words, board):
    list_of_filtered_words = []
    for word in all_words:
        c = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                big_n_word = ""
                if len(board[row][col]) > 0:
                    for i in range(len(board[row][col])):
                        big_n_word = big_n_word + word[i]
                    if board[row][col] == big_n_word:
                        if help_filtered_words((row, col), word, len(board[row][col])
                                ,"" + big_n_word, [] + [(row, col)], board):
                            list_of_filtered_words.append(word)
                            c = 3
                            break
            if c == 3:
                break
    return list_of_filtered_words


def legal_path(cord):
    #this function checks if every coordinate of the path is in the surrounding of the coordinate that had chosen before it
    cords = []
    for row in range(cord[0] - 1, cord[0] + 2):
        for col in range(cord[1] - 1, cord[1] + 2):
            if (row < 0 or row > 3) or (col < 0 or col > 3) or (row, col) == cord:
                continue
            cords.append((row, col))
    return cords


def is_valid_path(board, path, words):
    #this function checks if the path is legal and give me a word that belongs to words
    if len(path) == 0:
        return None
    if (path[0][0] < 0 or path[0][0] > 3) or (path[0][1] < 0 or path[0][1] > 3):
        return None
    if len(path) != len(set(path)):
        return None
    counter = 0
    for i in range(1, len(path)):
        if path[i] not in legal_path(path[counter]):
            return None
        counter += 1
    word = ""
    for cord in path:
        word += board[cord[0]][cord[1]]
    if word in words:
        return word
    return None


def help_find_length_n_paths(cord, n, counter, board, words, paths, path):

    if n == counter:
        if is_valid_path(board, path, words) is not None:
            paths.append(deepcopy(path))
            return paths
        return paths
    for row in range(cord[0] - 1, cord[0] + 2):
        for col in range(cord[1] - 1, cord[1] + 2):
            if (row < 0 or row > 3) or (col < 0 or col > 3) or (cord[0] == row and col == cord[1]) or (row, col) in path:
                continue
            paths = help_find_length_n_paths((row, col), n, counter + 1, board, words, paths, path + [(row, col)])
    return deepcopy(paths)


def find_length_n_paths(n, board, words):
    """
        :param n: the length of the path
        :param board: the board with the letter
        :param words: a list of words
        :return: all paths with the length of n that returns a given word
        """
    words2 = filtered_words(words, board)
    paths = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            paths = paths + help_find_length_n_paths((row, col), n, 1, board, words2, [], [] + [(row, col)])
    return paths


def find_length_n_words(n, board, words):
    """

     :param n: the length of a word
     :param board: an input
     :param words: a list of words
     :return: the paths that lead to the word in the board
     """

    words = filtered_words(words, board)
    paths = []
    word_max_len = 0
    n_words = []
    for word in words:
        if len(word) == n:
            n_words.append(word)
            if len(word) > word_max_len:
                word_max_len = len(word)
    n = word_max_len
    for i in range(1, n + 1):
        for row in range(len(board)):
            for col in range(len(board[row])):
                paths = paths + help_find_length_n_paths((row, col), i, 1, board, n_words, [], [] + [(row, col)])
    return paths


def max_score_paths(board, words):
    """

     :param board: a input
     :param words: a list of words
     :return: the path with the maximum length
     """
    words2 = filtered_words(words, board)
    print(words2)
    all_paths = []
    for word in words2:
        for n in range(len(word), 0, -1):
            paths = find_length_n_paths(n, board, [word])
            if len(paths) != 0:
                all_paths.append(paths[0])
                break
    return all_paths
