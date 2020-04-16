import os
from time import sleep


def alarm(content, pause_flag = True):
    
    os.system(f'say "{content}"')
    if pause_flag:
        input('Press any key to resume. ')


if __name__ == "__main__":
    alarm('first test', pause_flag = False)
    alarm('second test')