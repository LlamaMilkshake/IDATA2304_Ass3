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


def off_by_default():
    print('Testing to see if TV is OFF by default: ')
    if not handler.get_power():
        print('Test 1 of 1 successful')
    else:
        print('Test 1 of 1 failed')

def power_off_limitations():
    print('Testing to see if TV being OFF prohobits TV state changing commands: ')
    if not handler.get_power():
        if handler.handle_command(channel_up_cmd) == 'ERROR: TV is off':
            print('Test 1 of 3 successful')
        else:
            print('Test 1 of 3 failed')

        if handler.handle_command(get_channel_cmd) == 'ERROR: TV is off':
            print('Test 2 of 3 successful')
        else:
            print('Test 2 of 3 failed')

        if handler.handle_command(get_count_cmd) == 'ERROR: TV is off':
            print('Test 3 of 3 successful')
        else:
            print('Test 3 of 3 failed')
    else:
        print('Could not run this test. TV is ON')
    
def power_on_actions():
    print('Testing to see if TV being ON allows commands invoking state actions: ')
    if handler.get_power():
        if handler.handle_command(get_channel_cmd) == 'CHANNEL ' + str(handler.get_channel()):
            print('Test 1 of 3 successful')
        else:
            print('Test 1 of 3 failed')

        if handler.handle_command(set_channel_cmd + ' 2') == 'OK':
            if handler.get_channel() == 2:
                print('Test 2 of 3 successful')
            else:
                print('Test 2 of 3 failed')
        else:
            print('Test 2 of 3 failed')

        if handler.handle_command(set_channel_cmd + ' a') == 'ERROR: invalid channel':
            print('Test 3 of 3 successful')
        else:
            print('Test 3 of 3 failed')
    else:
        print('Could not run this test. TV is OFF')

def main():
    print('Running TV logic tests...')

    off_by_default()

    handler.set_power(False)
    power_off_limitations()

    handler.set_power(True)
    power_on_actions()


if __name__ == '__main__':
    main()