#!/usr/bin/env python3


from getpass import getpass
import os, sys
import re
import random
import time


def check_python_version(v):
    v = str(v).split('.')
    try:
        if not 1 < int(v[0]) <= 3:
            raise ValueError('Error: You are requiring invalid Python version',v[0])
    except ValueError as e:
        print(e)
        sys.exit(1)
    if sys.version_info[0] != int(v[0]):
        print('This script requires Python version ' + v[0] + '+')
        print('You are using {0}.{1}.{2} {3}'.format(sys.version_info[0], sys.version_info[1], sys.version_info[2],sys.version_info[3]))
        sys.exit(1)


def player_names(mode=None):
    robot_names = ['Roomba', 'Terminator', 'R2D2', 'Claptrap', 'Bender',
                   'Jarvis', 'Awesom-O', 'Alexa', 'Paranoid Marvin', 'Optimus Prime']
    while True:
        if mode == 'H_vs_H':
            user1_name = input('First player\'s name: ').strip()
            user2_name = input('Second player\'s name: ').strip()
        elif mode == 'H_vs_AI':
            user1_name = input('Human\'s name: ').strip()
            user2_name = random.choice(robot_names)
        else:
            user1_name, user2_name = None, None
            while user1_name == user2_name:
                user1_name = random.choice(robot_names)
                user2_name = random.choice(robot_names)

        if (re.match('[^A-Za-z0-9-]',user1_name)) or (re.match('[^A-Za-z0-9-]',user2_name)):
            print('\nInvalid characters detected\n')
            print('user1:',user1_name,'\nuser2:',user2_name)
            continue
        elif not user1_name or not user2_name:
            print('\nName can\'t be blank\n')
            continue
        else:
            break

    return user1_name, user2_name


def choices():
    while True:
        try:
            print('\n*** ROCK PAPER SCISSORS ***\n')
            print('\nPick Your Game:\n')
            print('1. Human vs Human\n2. Human vs AI\n3. AI vs AI')

            choice = input('\n1, 2 or 3?:').strip('.')
            if not re.match(r'^(1|2|3)', choice):
                os.system('clear')
                raise ValueError('\nInvalid Choice: Pick either 1, 2 or 3\n')

            N = input('\nNumber of games:')
            if not re.match(r'^(\d)', N) or int(N) < 1:
                os.system('clear')
                raise ValueError('\nInvalid Choice: ' + str(N) + '\nEnter a valid number of games to play\n')

            if choice[0] == '1':
                mode = 'H_vs_H'
                print('\nHuman vs Human!\n')
            elif choice[0] == '2':
                mode = 'H_vs_AI'
                print('\nHuman vs AI!\n')
            else:
                mode = 'AI_vs_AI'
                print('\nAI vs AI!\n')
            print('TOTAL OF', N, 'GAMES\n')
            break
        except ValueError as e:
            print(e)
        except TypeError as e:
            print(e)

    return N, mode


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


def run_game(user1_name, user2_name, games, mode=None):
            # win        lose
    rules = {'rock':    'scissors',
            'paper':    'rock',
            'scissors': 'paper'}

    stats = []

    user1_wins = 0
    user2_wins = 0

    game_count = 1

    if mode == 'AI_vs_AI':
        os.system('clear')
        print('\nHi {0} and {1}!'.format(user1_name, user2_name))
        time.sleep(2)
    else:
        os.system('clear')
        print('\nHi {0} and {1}!'.format(user1_name, user2_name))

    while game_count <= games:
        print('\n' + '-' * 16)
        print('\033[42;30m| GAME # {0} of {1}\033[m'.format(str(game_count), games))
        print('-' * 16)

        print('\nChoose from the following:'.format(user1_name, user2_name))
        for i, hand in enumerate(rules, 1):
            print(str(i) + ': ' + hand)

        if mode == 'H_vs_H' or mode == 'H_vs_AI':
            user1 = getpass('\n' + user1_name + ': ')
            if user1 == '1':
                user1 = 'rock'
            elif user1 == '2':
                user1 = 'paper'
            elif user1 == '3':
                user1 = 'scissors'

            if user1 not in rules:
                print('Wrong choice: {0}\nPick from {1}'.format(user1,[(i,x) for i,x in enumerate(rules,1)]))
                continue
        spinner = spinning_cursor()
        think = random.randint(20,30)
        if mode == 'AI_vs_AI':
            user1 = random.choice(list(rules.keys()))
            user2 = random.choice(list(rules.keys()))
            print()
            print(user1_name,'vs',user2_name)
            for _ in range(think):
                sys.stdout.write(next(spinner))
                sys.stdout.flush()
                time.sleep(.1)
                sys.stdout.write('\b')
        elif mode == 'H_vs_AI':
            user2 = random.choice(list(rules.keys()))
        else:
            user2 = getpass(user2_name + ': ')
            if user2 == '1':
                user2 = 'rock'
            elif user2 == '2':
                user2 = 'paper'
            elif user2 == '3':
                user2 = 'scissors'

            if user2 not in rules:
                print('Wrong choice: {0}\nPick from {1}'.format(user2,[(i,x) for i,x in enumerate(rules,1)]))
                continue

        os.system('clear')
        for win,lose in rules.items():
            if user1 == win and user2 == lose:
                stats.append((game_count,user1_name,win + ' beats ' + lose))
                print('\n({0}) "{1}" beats ({2}) "{3}"\n'.format(user1_name,win,user2_name,lose))
                print('** \033[1;31m{0} {1}\033[0m **'.format(user1_name,'WINS!'))
                user1_wins += 1
            if user2 == win and user1 == lose:
                stats.append((game_count, user2_name, win + ' beats ' + lose))
                print('\n({0}) "{1}" beats ({2}) "{3}"\n'.format(user2_name, win, user1_name, lose))
                print('** \033[1;31m{0} {1}\033[0;m **'.format(user2_name, 'WINS!'))
                user2_wins += 1

        if user1 == user2:
            print(user1 + ' and ' + user2)
            print('\n** \033[1;34m{0}\033[0;m **'.format("It's a draw"))
        else:
            game_count += 1

        print('\n  {0}\n  {1:20}: {2}\n  {3:20}: {4}'.format('STATS:',user1_name,user1_wins,user2_name,user2_wins))
        if user1_wins > user2_wins:
            print('\033[1;43m{0} {1}\033[0;m'.format(user1_name,'is in the lead!'))
        elif user1_wins < user2_wins:
            print('\033[1;43m{0} {1}\033[0;m'.format(user2_name, 'is in the lead!'))
        else:
            print('\033[1;47m{0} and {1} {2}\033[0;m'.format(user1_name,user2_name,'you have a draw!'))

    os.system('clear')
    print('\n\033[40;31m|^| GAME OVER |^|\033[m')
    print('\n  {0}\n  {1:20}: {2}\n  {3:20}: {4}'.format('FINAL STATS:',user1_name,user1_wins,user2_name,user2_wins))
    if user1_wins > user2_wins:
        print('\n\033[1;46m{0} {1}\033[0;m\n'.format(user1_name,'WINS the GAME!\n'))
    elif user1_wins < user2_wins:
        print('\n\033[1;46m{0} {1}\033[0;m\n'.format(user2_name, 'WINS the GAME!\n'))
    else:
        print('\n\033[1;47m{0} and {1} {2}\033[0;m'.format(user1_name,user2_name,'this GAME is a DRAW!\n'))

    print('{0:5} {1:^15} {2:^22}'.format('GAME#','WINNER','EVENT'))
    print('{0} {1} {2}'.format('-' * 5, '-' * 15, '-' * 22))
    for each in stats:
        print('{0:<5} {1:15} {2:22}'.format(each[0],each[1],each[2]))
    print()


if __name__ == "__main__":
    check_python_version('3')

    while True:
        os.system('clear')

        num_games, MODE = choices()
        player1, player2 = player_names(MODE)

        run_game(player1, player2, int(num_games), MODE)

        while True:
            prompt = input("Play another game? (yes/no): ")
            if re.match(r'^y', prompt.lower()):
                break
            elif re.match(r'^n', prompt.lower()):
                sys.exit(0)
            else:
                print("Invalid input:", str(prompt))
                print("Type 'yes' or 'no'\n")

