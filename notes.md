# running test file: From Code dir, write "py -m test.test_handler". This will run the file as a module, and allow it to see the handler.py file in the sibling folder.

Protocol design:
- What exact strings does the client send? (Client -> Server commands)
    * POWER ON          - Turns TV on
    * POWER OFF         - Turns TV off 
    * CHANNEL UP        - move one channel up
    * CHANNEL DOWN      - move one channel down
    * SET CHANNEL 5     - sets a specific channel. this has a parameter
    * GET CHANNEL       - reads back the current channel
    * GET COUNT         - reads back the value of C, aka the channel count
    * STATUS            - shows whether the TV is on or off

- What exact strings does the server send back? (Server -> Client reply)
    * OK                        - Generic acknowledgement after eg. POWER ON, CHANNEL UP
    * ERROR: TV is off          - Error message if user tries anything but TURN ON when tv is off
    * ERROR: invalid channel    - Error message if user tries to SET CHANNEL outside of C scope
    * ERROR: invalid command      - Error message if user tries to send an invalid command
    * CHANNEL 5                 - Answers a GET CHANNEL query with actual data
    * STATUS ON/STATUS OFF      - Answers the STATUS command specifically

- Whats the format? Plain text commands like the calculator example, or something structured?
    * Text. I want it to be readable for myself to increase readability



# Requirements and how I will solve them #
1.1.1. The Smart TV is a server.
    * Make server the smart TV

1.1.2. The TV has a fixed number of available channels C, where C >= 3. You choose C in your implementation.
    * Parameterize C in the server class, set its value to 3 or more
    * CS_cmd GET COUNT to let client know how many avilable channels this TV has

1.1.3. Channel 1 is the current channel when the server starts.
    * Let the CHANNEL parameter initially be 1 in the server

1.1.4. When the TV is turned OFF and then ON again, it remembers the previous channel. But restarting the server may reset the channel to 1.
    * Use a TVState class to store the state of the TV, holding variables like power, channel and num_channels

1.1.5. While the TV is OFF, the only TV-control command that changes state is POWER ON.
    * checks handle_command(command, tv_state) to check if TV is on and command is anything but TURN ON before actually handling command + SC_cmd ERROR: TV is off

1.1.6. While the TV is ON, the remote can read the channel count, read the current channel, set a channel, move one channel up and move one channel down.
    * CS_cmds GET COUNT, GET CHANNEL, SET CHANNEL a, CHANNEL UP, CHANNEL DOWN

1.1.7. Invalid channel and unknown commands must be handled.
    * SC_cmds ERROR: invalid channel, ERROR: invalid command

1.1.8. Channel UP and DOWN use wrap-around: For example from channel with highest number, UP goes to 1; from 1, DOWN goes to channel with highest number.
    * For CS_cmd CHANNEL UP: if channel == C: channel = 1 else: channel += 1
    * For CS_cmd CHANNEL DOWN: if channel == 1: channel = C else: channel -= 1

1.2.1. The remote is a TCP client.
    * make client the remote

1.2.2. A remote connects to one TV at a time.
    * make a loop inside loop in server loop to keep tv state in between remote connections

1.2.3. It must allow the user to turn the TV ON/OFF, move the channel UP/DOWN.
    * CS_cmds TURN ON, TURN OFF, CHANNEL UP, CHANNEL DOWN

1.2.4. Must support STATUS command. STATUS command should show whether the TV is ON or OFF.
    * CS_cmd STATUS     SC_cmds STATUS ON, STATUS OFF