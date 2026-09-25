from include import handler


power_on_cmd = 'POWER ON'
power_off_cmd = 'POWER OFF'
channel_up_cmd = 'CHANNEL UP'
channel_down_cmd = 'CHANNEL DOWN'
set_channel_cmd = 'SET CHANNEL'
get_channel_cmd = 'GET CHANNEL'
get_count_cmd = 'GET COUNT'
status_cmd = 'STATUS'
help_cmd = 'HELP'


def lower_case():
    print('Testing to see if lowercase commands can be handled: ')
    if handler.handle_command(power_on_cmd.lower()) == 'OK':
        print('Test 1 of 1 successful')
    else:
        print('Test 1 of 1 failed')

def upper_case():
    print('Testing to see if uppercase commands can be handled: ')
    if handler.handle_command(power_on_cmd.upper()) == 'OK':
        print('Test 1 of 1 successful')
    else:
        print('Test 1 of 1 failed')

def invalid_command():
    print('Testing to see if invalid commands are handled correctly: ')
    if handler.handle_command('WherE EaRe yOuUUUuUUuUUUuuu') == 'ERROR: invalid command':
        print('Test 1 of 1 successful')
    else:
        print('Test 1 of 1 failed')


def main():
    print('Running message formats tests...')

    lower_case()

    upper_case()

    invalid_command()


if __name__ == '__main__':
    main()