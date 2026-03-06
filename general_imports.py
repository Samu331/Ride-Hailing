from os import system


def clear():  # To clear screen and account for different operating systems
    system('cls')


# Track whether a function has been called
class TrackFuncCall:

    not_called = True

    def __init__(self, func):
        self.func = func

    def __call__(self):
        self.not_called = False
