from include.handler import handle_command

def main():

    while True:
        command = input('TEST_COMMAND>> ')
        if command == '':
            '\n'
        else:
            response = handle_command(command)
            print(response)

        if command.upper() == 'QUIT':
            break


if __name__ == "__main__":
    main()