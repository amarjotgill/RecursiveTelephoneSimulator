"""
File: switchboard.py
Author: Amarjot Gill
Date: 11/22/2020
Lab Section: 44
Email:  agill3@umbc.edu
Description:  This program contains the Switchboard class
in this Switchboard class it will add phones to it's database, be able to add
trunk connections to other switch boards to it's database, and also using
recursion it will be able to connect calls and will alert the user if calls
can not be connected.
"""

from phone import Phone


class Switchboard:
    def __init__(self, area_code):
        """
        :param area_code: the area code to which the switchboard will be associated.
        """
        self.area_code = area_code
        # list to contain the Class objects of the phone
        self.phone_number_list = []
        # these list are the numbers only for the saving and loading file part of the project
        self.phone_number_only = []
        self.trunk_number_only = []
        # list contains the Class objects of the lines connected to the switch_board
        self.trunk_lines = []

        # you will probably need more data here.

    def add_phone(self, phone_number):
        """
        This function should add a local phone connection by creating a phone object
        and storing it in this class.  How you do that is up to you.

        :param phone_number: phone number without area code
        :return: depends on implementation / None
        """
        for i in range(len(self.phone_number_list)):
            # checks too see if the number is already in use
            if self.phone_number_list[i].number == phone_number:
                return print("this number is already in use")
        else:
            # creates and appends the Phone object
            self.phone_number_list.append(Phone(phone_number, self, self.area_code))
            self.phone_number_only.append(phone_number)
            print("Done!")

    def add_trunk_connection(self, switchboard, number):
        """
        Connect the switchboard (self) to the switchboard (switchboard)

        :param switchboard: should be either the area code or switchboard object to connect.
        :return: success/failure, None, or it's up to you
        """
        # checks too make sure the switch is not already linked
        if switchboard not in self.trunk_lines:
            # appends the object to trunk_lines
            self.trunk_lines.append(switchboard)
            # appends the board to the object that just got appended
            switchboard.trunk_lines.append(self)

            # number_only is for loading and saving file purposes
            self.trunk_number_only.append(number)
            switchboard.trunk_number_only.append(self.area_code)
            print("Trunk lines have been connected")
        else:
            # lines would be already connected if switchboard is in self.trunk_lines
            print("Lines are already connected")

    def connect_call(self, area_code, number, first_phone, previous):
        """
        This must be a recursive function.

        :param area_code: the area code to which the destination phone belongs
        :param number: the phone number of the destination phone without area code.
        :param previous: you must keep track of the previously tracked codes
        :return: Depends on your implementation, possibly the path to the destination phone.
        """

        link_exist = False
        """
        will look at the trunk lines in the current switchboard
        if an object's area_code in it's list is the same as the destination area code
        then it will check if the number is in the object's phone list
        if it does then it will return the connect function from the Phone class
        """
        for i in range(len(self.trunk_lines)):
            if self.trunk_lines[i].area_code == area_code:
                for x in range(len(self.trunk_lines[i].phone_number_list)):
                    if self.trunk_lines[i].phone_number_list[x].number == number:
                        link_exist = True
                        return first_phone.connect(area_code, number, self.trunk_lines[i].phone_number_list[x])
        # if the link doesn't exist this one will run
        if not link_exist:
            for i in range(len(self.trunk_lines)):
                # will make sure it has not already checked this board to avoid infinite recursion
                if self.trunk_lines[i] not in previous:
                    # will add this to the previous list
                    previous.append(self.trunk_lines[i])
                    # returns new switchboard
                    return self.trunk_lines[i].connect_call(area_code, number, first_phone, previous)
            else:
                # if none of those work then this will return because the lines can not be connected
                return print(str(area_code) + "-" + str(number),
                             "and", str(first_phone.area_code) + "-" + str(first_phone.number), "were not connected")


