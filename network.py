"""
File: network.py
Author: Amarjot Gill
Date: 11/22/2020
Lab Section: 44
Email:  agill3@umbc.edu
Description:  This program is the main code for project3,
in here the user will be able to add switch boards, connect swtich boards,
add phone numbers to these switch boards, call phones, and have the option to save
and load their created network using file io.
"""

from phone import Phone
from switchboard import Switchboard


HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'
OPEN_BRACKET = '['
CLOSE_BRACKET = ']'
OPEN_CURLY = '{'
CLOSE_CURLY = '}'


class Network:
    def __init__(self):
        """
            Construct a network by creating the switchboard container object

            You are free to create any additional data/members necessary to maintain this class.
        """
        # list to contain all the switch boards in this network
        self.switchboard_list = []

    def load_network(self, filename):
        """
        :param filename: the name of the file to be loaded.  Assume it exists and is in the right format.
                If not, it's ok if your program fails.
        :return: success?
        """
        open_file = open(filename, "r")
        # this resets the network
        self.switchboard_list = []
        for line in open_file:
            split_line = line.split()
            # creates and appends a new switchboard object
            switch = Switchboard(int(split_line[0]))
            self.switchboard_list.append(switch)

            for i in range(len(split_line) - 1):
                # I used [ to determine the start of the trunk line connections
                if split_line[i] == OPEN_BRACKET:
                    i += 1
                    # will keep going and append anything in between [] which are the numbers of trunk lines
                    while split_line[i] != CLOSE_BRACKET:
                        switch.trunk_number_only.append(int(split_line[i]))
                        i += 1
                # { is used for phones in the switchboard
                if split_line[i] == OPEN_CURLY:
                    i += 1

                    while split_line[i] != CLOSE_CURLY:
                        # this creates the phone objects
                        switch.add_phone(int(split_line[i]))
                        i += 1

            for switches in self.switchboard_list:
                # if the area code is in the current switches trunk_number_only then
                # using the connect_switchboards function the trunk connection will be made.
                if switches.area_code in switch.trunk_number_only:
                    self.connect_switchboards(switches.area_code, switch.area_code)

        open_file.close()

    def save_network(self, filename):
        """
        :param filename: the name of your file to save the network.  Remember that you need to save all the
            connections, but not the active phone calls (they can be forgotten between save and load).
            You must invent the format of the file, but if you wish you can use either json or csv libraries.
        :return: success?
        """

        file_save = open(filename, "w")
        for switch in self.switchboard_list:
            file_save.write("{}".format(switch.area_code) + "\t")
            # if trunk lines exist then this will run
            if switch.trunk_number_only:
                # [ is the start to store the numbers of trunk connections
                file_save.write(OPEN_BRACKET + "\t")
                # will write ever number
                for number in switch.trunk_number_only:
                    file_save.write(str(number) + "\t")
                # ] is to symbolize the end of trunk lines
                file_save.write(CLOSE_BRACKET + "\t")
            # { is used for phones, works the same as the trunk_lines
            if switch.phone_number_only:
                file_save.write(OPEN_CURLY + "\t")
                for phone in switch.phone_number_only:
                    file_save.write(str(phone) + "\t")
                # } is used to symbolize the end of writing the phones
                file_save.write(CLOSE_CURLY)
            file_save.write("\n")

        file_save.close()

    def add_switchboard(self, area_code):
        """
        add switchboard should create a switchboard and add it to your network.

        By default it is not connected to any other boards and has no phone lines attached.
        :param area_code: the area code for the new switchboard
        :return:
        """
        for i in range(len(self.switchboard_list)):
            # checks if the switchboard is already in the list thus already being made
            if self.switchboard_list[i].area_code == area_code:
                return print("switchboard has already been created")
        else:
            # creates a switchboard Object with the enter area_code
            self.switchboard_list.append(Switchboard(area_code))
            print("Switchboard has been created")

    def connect_switchboards(self, area_1, area_2):
        """
            Connect switchboards should connect the two switchboards (creates a trunk line between them)
            so that long distance calls can be made.

        :param area_1: area-code 1
        :param area_2: area-code 2
        :return: success/failure
        """
        switch_board_exist = False
        switch_board_exist2 = False
        # runs a loop too see if both switchboards exist before trying to connect
        for i in range(len(self.switchboard_list)):
            # finds both boards that need to be connected
            if area_1 == self.switchboard_list[i].area_code:
                area_1_number = self.switchboard_list[i]
                switch_board_exist = True

            elif area_2 == self.switchboard_list[i].area_code:
                area_2_number = self.switchboard_list[i]
                switch_board_exist2 = True

        # if both exist the function add_trunk_connection will be called to connect them
        if switch_board_exist and switch_board_exist2:
            area_1_number.add_trunk_connection(area_2_number, area_2)

        else:
            # if one or both dont exist this will alert the user that
            print("one of the switchboards has not been created yet")

    def display(self):
        """
            Display should output the status of the phone network as described in the project.
        """
        for i in range(len(self.switchboard_list)):
            print("Switchboard with area code:", self.switchboard_list[i].area_code)
            print("\t", "Trunk Lines are:")
            # if the Object's trunk_lines list is not empty this will run printing each object in that list
            if self.switchboard_list[i].trunk_lines:
                for x in range(len(self.switchboard_list[i].trunk_lines)):
                    print("\t", "\t",
                          "Trunk line connection to:", self.switchboard_list[i].trunk_lines[x].area_code)
            print("\t", "Local phone numbers are:")
            # if the Object's phone_number_list is not empty this will run,
            if self.switchboard_list[i].phone_number_list:
                for z in range(len(self.switchboard_list[i].phone_number_list)):
                    # if the Phone's phone_call list is empty it will print it is not in use
                    if not self.switchboard_list[i].phone_number_list[z].phone_call:
                        print("\t", "\t", "Phone with number"
                              , self.switchboard_list[i].phone_number_list[z].number, "is not in use")
                    # if the Phone's phone_call is not empty that means it is connected and on a call
                    elif self.switchboard_list[i].phone_number_list[z].phone_call:
                        print("\t", "\t", "Phone with number"
                              , self.switchboard_list[i].phone_number_list[z].number,
                              "is connected too", self.switchboard_list[i].phone_number_list[z].phone_call[0])


if __name__ == '__main__':
    the_network = Network()
    s = input('Enter command: ')
    while s.strip().lower() != QUIT:
        switch_exist = False
        split_command = s.split()
        if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT:
            area_1 = int(split_command[1])
            area_2 = int(split_command[2])
            the_network.connect_switchboards(area_1, area_2)
        elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD:
            the_network.add_switchboard(int(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == PHONE_ADD:
            number_parts = split_command[1].split(HYPHEN)
            area_code = int(number_parts[0])
            phone_number = int(''.join(number_parts[1:]))
            # this will check to make sure the switchboard exist
            for i in range(len(the_network.switchboard_list)):
                if the_network.switchboard_list[i].area_code == area_code:
                    switch_exist = True
                    # sets current_board = to whatever object switchboard matches area_codes
                    current_board = the_network.switchboard_list[i]
                    # calls add phone function for this switch_board
                    current_board.add_phone(phone_number)
            # will let the user know the switch isnt made yet
            if not switch_exist:
                print("That switch does not exist yet")

        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_SAVE:
            the_network.save_network(split_command[1])
            print('Network saved to {}.'.format(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_LOAD:
            the_network.load_network(split_command[1])
            print('Network loaded from {}.'.format(split_command[1]))
        elif len(split_command) == 3 and split_command[0].lower() == START_CALL:
            src_number_parts = split_command[1].split(HYPHEN)
            src_area_code = int(src_number_parts[0])
            src_number = int(''.join(src_number_parts[1:]))

            dest_number_parts = split_command[2].split(HYPHEN)
            dest_area_code = int(dest_number_parts[0])
            dest_number = int(''.join(dest_number_parts[1:]))
            board_exist = False
            # will check to make sure src_area_code exist in an switchboard
            for i in range(len(the_network.switchboard_list)):
                if the_network.switchboard_list[i].area_code == src_area_code:
                    board_exist = True
                    # sets phone_board = to the board with the src_area_code
                    phone_board = the_network.switchboard_list[i]
                    for x in range(len(phone_board.phone_number_list)):
                        # checks to make sure the src_number exist
                        if phone_board.phone_number_list[x].number == src_number:
                            phone = phone_board.phone_number_list[x]
                            # resets the searched list every time a new call is made
                            searched = []
                            # calls the connect_call function
                            phone_board.connect_call(dest_area_code, dest_number, phone, searched)

            if not board_exist:
                print("switch has not been created yet")

        elif len(split_command) == 2 and split_command[0].lower() == END_CALL:
            number_parts = split_command[1].split('-')
            area_code = int(number_parts[0])
            number = int(''.join(number_parts[1:]))
            # checks to make sure the area_code exist and sets current_board to it
            for i in range(len(the_network.switchboard_list)):
                if the_network.switchboard_list[i].area_code == area_code:
                    current_board = the_network.switchboard_list[i]
                    # checks to make sure number exist and sets current_phone = to the phone object
                    for x in range(len(current_board.phone_number_list)):
                        if current_board.phone_number_list[x].number == number:
                            current_phone = current_board.phone_number_list[x]
                            # runs the disconnect function
                            current_phone.disconnect()

        elif len(split_command) >= 1 and split_command[0].lower() == DISPLAY:
            the_network.display()

        s = input('Enter command: ')
