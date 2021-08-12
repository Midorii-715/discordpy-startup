import random


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.stalin_mode = False
        self.stalin_name = 'スターリン'
        self.stalin_x = 0
        self.stalin_y = 0

class Maze:
    __ROAD = 0
    __WALL = 1

    __STALIN_INVISIBLE = 0
    __STALIN_UP = 1
    __STALIN_DOWN = 2
    __STALIN_LEFT = 3
    __STALIN_RIGHT = 4
    __STALIN_SAME = 5

    def __init__(self):
        self.__player = {}
        self.__make_maze()

    def process(self, message):
        send_msg = ''
        member =  message.author
        name = message.author.display_name

        if message.content == '/maze help':
            send_msg = self.__help()
        elif message.content == '/maze enter':
            send_msg = self.__enter(message)
        elif message.content == '/maze enter stalin mode':
            send_msg = self.__enter(message)
            self.__player[name].stalin_mode = True
            self.__player[name].stalin_name = 'スターリン'
            self.__player[name].stalin_x = self.__finish_x
            self.__player[name].stalin_y = self.__finish_y
            if message.content[12:-5] != 'stalin':
                self.__player[name].stalin_name = message.content[12:-5]
        elif message.content == '/maze give up':
            send_msg = self.__give_up(message)

        if name in self.__player:
            if message.content == 'w':
                send_msg = self.__up(message)
            elif message.content == 's':
                send_msg = self.__down(message)
            elif message.content == 'a':
                send_msg = self.__left(message)
            elif message.content == 'd':
                send_msg = self.__right(message)

            if send_msg != '':
                goal_msg = self.__goal(message)
                if goal_msg != '':
                    send_msg += '\n'
                    send_msg += goal_msg
                else:
                    send_msg += '\n'
                    send_msg += self.__next(message)

                    if self.__player[name].stalin_mode:
                        send_msg += '\n'
                        send_msg += self.__stalin_move(message)

        if send_msg != '':
            return f"{member.mention} " + send_msg
        else:
            return None



    def __help(self):
        send_msg = '\n'
        send_msg += '/maze enter:             迷路に入る。最初からやり直す場合もこれ。\n'
        send_msg += '/maze enter stalin mode: スターリンモード。上級者向け。\n'
        send_msg += 'w:                       上へ行く。迷路に入っているときのみ有効。\n'
        send_msg += 's:                       下へ行く。迷路に入っているときのみ有効。\n'
        send_msg += 'a:                       左へ行く。迷路に入っているときのみ有効。\n'
        send_msg += 'd:                       右へ行く。迷路に入っているときのみ有効。\n'
        send_msg += '/maze give up:           迷路から出る。\n'
        send_msg += '\n'
        send_msg += 'ゴールすると自動的に迷路から出る。\n'

        return send_msg
    
    def __enter(self, message):
        send_msg = ''
        name = message.author.display_name

        if name in self.__player:
            send_msg = '迷路の入口に戻った。'
        else:
            send_msg = '迷路に入った。'

        player = Player()
        player.x = self.__initial_x
        player.y = self.__initial_y
        self.__player[name] = player

        return send_msg
    
    def __give_up(self, message):
        send_msg = ''
        name = message.author.display_name

        if name in self.__player:
            send_msg = name + 'は目の前が真っ暗になった。'
            send_msg += '\n'
            send_msg += '!!!GAME OVER!!!'

            self.__player.pop(name)
        else:
            send_msg = '迷路の外にいる。'

        return send_msg
    
    def __up(self, message):
        send_msg = ''
        player = self.__player[message.author.display_name]

        if self.__can_up(player.x, player.y) == self.__ROAD:
            send_msg = '上に進んだ。'
            player.y = player.y - 1
        else:
            send_msg = '壁があって進めない。'

        return send_msg
    
    def __down(self, message):
        send_msg = ''
        player = self.__player[message.author.display_name]

        if self.__can_down(player.x, player.y) == self.__ROAD:
            send_msg = '下に進んだ。'
            player.y = player.y + 1
        else:
            send_msg = '壁があって進めない。'

        return send_msg
    
    def __left(self, message):
        send_msg = ''
        player = self.__player[message.author.display_name]

        if self.__can_left(player.x, player.y) == self.__ROAD:
            send_msg = '左に進んだ。'
            player.x = player.x - 1
        else:
            send_msg = '壁があって進めない。'

        return send_msg
    
    def __right(self, message):
        send_msg = ''
        player = self.__player[message.author.display_name]

        if self.__can_right(player.x, player.y) == self.__ROAD:
            send_msg = '右に進んだ。'
            player.x = player.x + 1
        else:
            send_msg = '壁があって進めない。'

        return send_msg
    

    def __make_maze(self):
        '''
        0: 道
        1: 壁
        '''
        self.__initial_x = 4
        self.__initial_y = 8
        self.__finish_x = 4
        self.__finish_y = 0
        self.__maze = [[1,0,1,1,0,1,1,1,1],
                       [1,0,1,1,0,0,0,0,0],
                       [1,0,0,0,0,1,0,1,1],
                       [1,0,1,1,1,0,0,0,1],
                       [1,0,0,0,1,0,1,0,1],
                       [1,1,1,0,1,0,1,0,1],
                       [1,0,1,0,1,1,1,0,1],
                       [0,0,0,0,0,0,0,0,1],
                       [1,1,1,1,0,1,1,1,1]]

    def __next(self, message):
        player = self.__player[message.author.display_name]

        send_msg = '次は'
        if self.__can_up(player.x, player.y) == self.__ROAD:
            send_msg += '上 '
        if self.__can_down(player.x, player.y) == self.__ROAD:
            send_msg += '下 '
        if self.__can_left(player.x, player.y) == self.__ROAD:
            send_msg += '左 '
        if self.__can_right(player.x, player.y) == self.__ROAD:
            send_msg += '右 '
        send_msg += 'に進めそうだ。'
        return send_msg
    
    def __goal(self, message):
        send_msg = ''
        player = self.__player[message.author.display_name]

        if (player.x == self.__finish_x) and (player.y == self.__finish_y):
            send_msg = '🎉おめでとう！迷路から脱出できた！🎉'
            self.__player.pop(message.author.display_name)

        return send_msg

    def __can_up(self, x, y):
        retval = self.__WALL

        if y >= 1:
            if self.__maze[y-1][x] == self.__ROAD:
                retval = self.__ROAD
        return retval

    def __can_down(self, x, y):
        retval = self.__WALL
        
        if y < (len(self.__maze)-1):
            if self.__maze[y+1][x] == self.__ROAD:
                retval = self.__ROAD
        return retval

    def __can_left(self, x, y):
        retval = self.__WALL

        if x >= 1:
            if self.__maze[y][x-1] == self.__ROAD:
                retval = self.__ROAD
        return retval

    def __can_right(self, x, y):
        retval = self.__WALL
        
        if x < (len(self.__maze[0])-1):
            if self.__maze[y][x+1] == self.__ROAD:
                retval = self.__ROAD
        return retval

    def __stalin_move(self, message):
        send_msg = ''
        name = message.author.display_name
        player = self.__player[name]

        for index in range(10):
            _type, _dist = self.__stalin_visible(message)
            if _type == self.__STALIN_SAME:
                send_msg = self.__player[name].stalin_name + 'が目の前にいる。\n🔪あなたは' + self.__player[name].stalin_name + 'に粛清された。🔪\nhttps://youtu.be/xSr5ewJvVig'
                send_msg += '\n'
                send_msg += '!!!GAME OVER!!!'
                self.__player.pop(name)
                return send_msg
            elif _type == self.__STALIN_UP:
                send_msg = self.__player[name].stalin_name + 'が{}マス上にいる。'.format(_dist)
                player.stalin_y = player.stalin_y + 1
            elif _type == self.__STALIN_DOWN:
                send_msg = self.__player[name].stalin_name + 'が{}マス下にいる。'.format(_dist)
                player.stalin_y = player.stalin_y - 1
            elif _type == self.__STALIN_LEFT:
                send_msg = self.__player[name].stalin_name + 'が{}マス左にいる。'.format(_dist)
                player.stalin_x = player.stalin_x + 1
            elif _type == self.__STALIN_RIGHT:
                send_msg = self.__player[name].stalin_name + 'が{}マス右にいる。'.format(_dist)
                player.stalin_x = player.stalin_x - 1
            if _type != self.__STALIN_INVISIBLE:
                send_msg += '\n'
                send_msg += self.__player[name].stalin_name + 'が近づいてきた。'
                break

            dir = random.randint(1, 4)
            for move_index in range(dir, dir+4):
                if (dir-1)%4 == self.__STALIN_UP:
                    if self.__can_up(player.stalin_x, player.stalin_y) == self.__ROAD:
                        player.stalin_y = player.stalin_y - 1
                        break
                    elif self.__can_down(player.stalin_x, player.stalin_y) == self.__ROAD:
                        player.stalin_y = player.stalin_y + 1
                        break
                    elif self.__can_left(player.stalin_x, player.stalin_y) == self.__ROAD:
                        player.stalin_x = player.stalin_x - 1
                        break
                    elif self.__can_right(player.stalin_x, player.stalin_y) == self.__ROAD:
                        player.stalin_x = player.stalin_x + 1
                        break

        _type, _dist = self.__stalin_visible(message)
        if _type == self.__STALIN_SAME:
            send_msg += self.__player[name].stalin_name + 'が目の前にいる。\n🔪あなたは' + self.__player[name].stalin_name + 'に粛清された。🔪\nhttps://youtu.be/xSr5ewJvVig'
            send_msg += '\n'
            send_msg += '!!!GAME OVER!!!'
            self.__player.pop(name)

        return send_msg

    def __stalin_visible(self, message):
        player = self.__player[message.author.display_name]

        if (player.stalin_x == player.x) and (player.stalin_y == player.y):
            return self.__STALIN_SAME, 0
        
        if player.stalin_x == player.x:
            if player.stalin_y > player.y:
                visible = True
                for index in range(player.y, player.stalin_y):
                    if self.__maze[index][player.x] == self.__WALL:
                        visible = False
                if visible:
                    return self.__STALIN_DOWN, (player.stalin_y - player.y)
            else:
                visible = True
                for index in range(player.stalin_y, player.y):
                    if self.__maze[index][player.x] == self.__WALL:
                        visible = False
                if visible:
                    return self.__STALIN_UP, (player.y - player.stalin_y)
        
        if player.stalin_y == player.y:
            if player.stalin_x > player.x:
                visible = True
                for index in range(player.x, player.stalin_x):
                    if self.__maze[player.y][index] == self.__WALL:
                        visible = False
                if visible:
                    return self.__STALIN_RIGHT, (player.stalin_x - player.x)
            else:
                visible = True
                for index in range(player.stalin_x, player.x):
                    if self.__maze[player.y][index] == self.__WALL:
                        visible = False
                if visible:
                    return self.__STALIN_LEFT, (player.x - player.stalin_x)
        
        return self.__STALIN_INVISIBLE, 0
