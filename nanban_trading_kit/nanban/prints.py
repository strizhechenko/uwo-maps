import colorama

bools = {
    True: f'{colorama.Fore.LIGHTGREEN_EX}{True}{colorama.Fore.RESET}',
    False: f'{colorama.Fore.RED}{False}{colorama.Fore.RESET}'
}


def hr(c='_'):
    print(c * 27)


def col(title, value):
    print(f'{title:20}: {value}')


def wrap(text, color, reset=colorama.Fore.RESET):
    return f'{color}{text}{reset}'


def bold(text):
    return wrap(text, colorama.Style.BRIGHT, colorama.Style.RESET_ALL)


def header(title, color=colorama.Fore.BLUE):
    print(bold(wrap(title, color)))
