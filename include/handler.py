power = False
channel = 1
num_channels = 6

power_on_cmd = 'POWER ON'
power_off_cmd = 'POWER OFF'
channel_up_cmd = 'CHANNEL UP'
channel_down_cmd = 'CHANNEL DOWN'
set_channel_cmd = 'SET CHANNEL'
get_channel_cmd = 'GET CHANNEL'
get_count_cmd = 'GET COUNT'
status_cmd = 'STATUS'
help_cmd = 'HELP'


set_channel_cmd_parts = set_channel_cmd.strip().split()

valid_commands = (power_on_cmd, power_off_cmd, 
                  channel_up_cmd, channel_down_cmd, 
                  set_channel_cmd, get_channel_cmd,
                  get_count_cmd, status_cmd, 
                  help_cmd)

def set_power(new_state):
    global power
    power = new_state

def set_channel(new_channel):
    global channel

    channel = int(new_channel)

def get_power():
    return power

def get_channel():
    return channel

def get_num_channels():
    return num_channels


def handle_command(cmd:str):
    cmd = cmd.upper()
    parts = cmd.strip().split()

    if cmd in valid_commands or (parts[0] == set_channel_cmd_parts[0] and parts[1] == set_channel_cmd_parts[1]):
        if cmd == help_cmd:
            return handle_help()
        elif cmd == status_cmd:
            return handle_status()
        elif cmd == power_on_cmd:
            return handle_power_on()
        elif cmd == power_off_cmd:
            return handle_power_off()
        elif not get_power():
            return 'ERROR: TV is off'
        
        elif get_power():
            if cmd == channel_up_cmd:
                return handle_channel_up()
            elif cmd == channel_up_cmd:
                return handle_channel_down()
            elif parts[0] == set_channel_cmd_parts[0] and parts[1] == set_channel_cmd_parts[1]:
                try:
                    if len(parts) <= 2:
                        return 'ERROR: must contain new channel to switch to'
                    else:
                        number = int(parts[2])
                        return handle_set_channel(parts[2])
                except Exception as e:
                    return 'ERROR: invalid channel'
            elif cmd == get_channel_cmd:
                return handle_get_channel()
            elif cmd == get_count_cmd:
                return handle_get_count()
            else:
                return 'ERROR: invalid command'
        else:
            return 'ERROR: invalid command'
    else:
        return 'ERROR: invalid command'



def handle_help():
    return (
        'Supported commands:\n'
        '-' + power_on_cmd + '\n'
        '-' + power_off_cmd + '\n'
        '-' + channel_up_cmd + '\n'
        '-' + channel_down_cmd + '\n'
        '-' + set_channel_cmd + '\n'
        '-' + get_channel_cmd + '\n'
        '-' + get_count_cmd + '\n'
        '-' + status_cmd + '\n'
        '-' + help_cmd + '\n'
    )

def handle_status():
    if get_power():
        return 'POWER ON'
    elif not get_power():
        return 'POWER OFF'
    else:
        return 'ERROR: something went wrong'

def handle_power_on():
    prev_power = get_power()
    set_power(True)

    log = status_update_power(prev_power, get_power())
    return 'OK\n' + log

def handle_power_off():
    prev_power = get_power()
    set_power(False)
    
    log = status_update_power(prev_power, get_power())
    return 'OK\n' + log

def handle_channel_up():
    global channel
    if channel == get_num_channels(): 
        channel = 1
        return 'OK'
    else: 
        channel += 1
        return 'OK'
    
def handle_channel_down():
    global channel
    if channel == 1: 
        channel = get_num_channels()
        return 'OK'
    else: 
        channel -= 1
        return 'OK'
    
def handle_set_channel(new_channel):
    if int(new_channel) >= 1 and int(new_channel) <= get_num_channels():
        set_channel(int(new_channel))
        return 'OK'
    else:
        return 'ERROR: invalid channel'

def handle_get_channel():
    return 'CHANNEL ' + str(get_channel())

def handle_get_count():
    return 'COUNT ' + str(get_num_channels())

def status_update_power(prev_power, curr_power):
    if prev_power:
        prev_power = 'ON'
    else:
        prev_power = 'OFF'

    if curr_power:
        curr_power = 'ON'
    else:
        curr_power = 'OFF'
    return ('[STATUS] TV power state changed from ' + prev_power + ' to ' + curr_power + '\n')
     