import random


class Game:
    def __init__(self):
        self.domino_set = []
        self.stock_pieces = []
        self.computer_pieces = []
        self.player_pieces = []
        self.domino_snake = []
        self.status = ''
        self.domino_score = {}

    def ai_move(self, comp_pieces, dom_snake):
        temp_list = comp_pieces + dom_snake
        comp_pieces_rating = {}
        for i in range(0, 7):
            self.domino_score[i] = sum(x.count(i) for x in temp_list)
        for domino in comp_pieces:
            if self.domino_score[domino[0]] != self.domino_score[domino[1]]:
                comp_pieces_rating[tuple(domino)] = self.domino_score[domino[0]] + self.domino_score[domino[1]]
            else:
                comp_pieces_rating[tuple(domino)] = self.domino_score[domino[0]]
        comp_pieces_rating_sorted = dict(sorted(comp_pieces_rating.items(), key=lambda x: x[1], reverse=True))
        return comp_pieces_rating_sorted

    def game_initiate(self):
        for i in range(7):
            for j in range(7):
                if [j, i] not in self.domino_set:
                    self.domino_set.append([i, j])
        while True:
            random.shuffle(self.domino_set)
            self.stock_pieces = self.domino_set[:14]
            self.computer_pieces = self.domino_set[14:21]
            self.player_pieces = self.domino_set[21:]
            computer_max = 0
            player_max = 0

            for i in range(7):
                if self.computer_pieces[i][0] == self.computer_pieces[i][1]:
                    if computer_max < self.computer_pieces[i][0]:
                        computer_max = self.computer_pieces[i][0]
                if self.player_pieces[i][0] == self.player_pieces[i][1]:
                    if player_max < self.player_pieces[i][0]:
                        player_max = self.player_pieces[i][0]

            if computer_max > player_max:
                status = 'player'
                self.domino_snake.append([computer_max, computer_max])
                self.computer_pieces.remove([computer_max, computer_max])
                return self.stock_pieces, self.computer_pieces, self.player_pieces, self.domino_snake, status
            elif player_max > computer_max:
                status = 'computer'
                self.domino_snake.append([player_max, player_max])
                self.player_pieces.remove(([player_max, player_max]))
                return self.stock_pieces, self.computer_pieces, self.player_pieces, self.domino_snake, status

    def game_step(self, status=''):
        if status == '':
            stock_pieces, computer_pieces, player_pieces, domino_snake, status = self.game_initiate()

        print(70*'=')
        print(f'Stock size: {len(self.stock_pieces)}')
        print(f'Computer pieces: {len(self.computer_pieces)}\n')

        if len(self.domino_snake) > 6:
            begin = self.domino_snake[:3]
            end = self.domino_snake[-3:]
            print(*begin, '...', *end, sep='')
        else:
            print(*self.domino_snake, sep='')

        print(f'\nYour pieces:')
        for i in range(len(self.player_pieces)):
            print(f'{i+1}:{self.player_pieces[i]}')
        if not (self.domino_snake[0][0] == self.domino_snake[len(self.domino_snake)-1][1] and sum(x.count(self.domino_snake[0][0]) for x in self.domino_snake) == 8):
            if status == 'computer':
                input('Status: Computer is about to make a move. Press Enter to continue...')
                computer_pieces_score = self.ai_move(self.computer_pieces, self.domino_snake)
                items = iter(computer_pieces_score.items())
                while True:
                    try:
                        item = next(items)
                        if len(self.computer_pieces) and len(self.player_pieces):
                            index_ = self.computer_pieces.index(list(item[0]))
                            if self.domino_snake[-1][1] in self.computer_pieces[index_]:
                                if self.domino_snake[-1][1] == self.computer_pieces[index_][0]:
                                    self.domino_snake.append(self.computer_pieces.pop(index_))
                                    break
                                elif self.domino_snake[-1][1] == self.computer_pieces[index_][1]:
                                    temp_item = self.computer_pieces.pop(index_)
                                    self.domino_snake.append(temp_item[::-1])
                                    break
                            elif self.domino_snake[0][0] in self.computer_pieces[index_]:
                                if self.domino_snake[0][0] == self.computer_pieces[index_][1]:
                                    self.domino_snake.insert(0, self.computer_pieces.pop(index_))
                                    break
                                elif self.domino_snake[0][0] == self.computer_pieces[index_][0]:
                                    self.domino_snake.insert(0, self.computer_pieces.pop(index_)[::-1])
                                    break
                        elif not len(self.player_pieces):
                            return 'player_won'

                    except StopIteration:
                        if len(self.stock_pieces):
                            self.computer_pieces.append(self.stock_pieces.pop())
                        break
                if not len(self.player_pieces):
                    return 'player_won'
                self.status = 'player'
            elif status == 'player':
                print(f'Status: It\'s your turn to make a move. Enter your command.')
                while True:
                    try:
                        next_step = int(input())
                        if len(self.computer_pieces) and len(self.player_pieces):
                            if next_step > 0:
                                if self.domino_snake[-1][1] in self.player_pieces[next_step - 1]:
                                    if self.domino_snake[-1][1] == self.player_pieces[next_step - 1][0]:
                                        self.domino_snake.append(self.player_pieces.pop(next_step - 1))
                                    elif self.domino_snake[-1][1] == self.player_pieces[next_step - 1][1]:
                                        self.domino_snake.append(self.player_pieces.pop(next_step - 1)[::-1])
                                else:
                                    raise Exception
                            elif next_step < 0:
                                if self.domino_snake[0][0] in self.player_pieces[abs(next_step) - 1]:
                                    if self.domino_snake[0][0] == self.player_pieces[abs(next_step) - 1][1]:
                                        self.domino_snake.insert(0, self.player_pieces.pop(abs(next_step) - 1))
                                    elif self.domino_snake[0][0] == self.player_pieces[abs(next_step) - 1][0]:
                                        self.domino_snake.insert(0, self.player_pieces.pop(abs(next_step) - 1)[::-1])
                                else:
                                    raise Exception
                            elif next_step == 0 and len(self.stock_pieces):
                                self.player_pieces.append(self.stock_pieces.pop())
                        elif not len(self.computer_pieces):
                            return 'computer_won'
                        elif not len(self.player_pieces):
                            return 'player_won'
                        break
                    except (ValueError, IndexError):
                        print('Invalid input. Please try again.')
                    except Exception:
                        print('Illegal move. Please try again.')
                self.status = 'computer'
        elif len(self.computer_pieces) and len(self.player_pieces):
            return 'draw'
        return self.status


if __name__ == '__main__':
    my_game = Game()
    status_ext = my_game.game_step()
    while True:
        if status_ext == 'player':
            status_ext = my_game.game_step('player')
        elif status_ext == 'computer':
            status_ext = my_game.game_step('computer')
        elif status_ext == 'computer_won':
            print('Status: The game is over. The computer won!')
            break
        elif status_ext == 'player_won':
            print('Status: The game is over. You won!')
            break
        elif status_ext == 'draw':
            print('Status: The game is over. It\'s a draw!')
            break
