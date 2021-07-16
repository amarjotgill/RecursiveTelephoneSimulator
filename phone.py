"""
File: phone.py
Author: Amarjot Gill
Date: 11/22/2020
Lab Section: 44
Email:  agill3@umbc.edu
Description:  This program contains the Phone class
for the project, this will be one individual phone object which
will also be assigned to a swtich board, in this Class the phone can connect to another
phone and also disconnect to another phone.
"""


class Phone:
    def __init__(self, number, switchboard, area_code):
        """
        :param number: the phone number without area code
        :param switchboard: the switchboard to which the number is attached.
        """
        self.number = number
        self.switchboard = switchboard
        # contains only numbers of the phone it is connected too
        self.phone_call = []
        self.area_code = area_code
        # contains the actual class Object of the phone that is connected
        self.end_call = []
        # you will need more parameters/attributes

    def connect(self, area_code, other_phone_number, connecting_phone):
        """
        :param area_code: the area code of the other phone number
        :param other_phone_number: the other phone number without the area code
        :return: **this you must decide in your implementation**
        """
        # make sure both phone_calls are empty
        # if they are not empty this means one of the phones is already in use
        if not self.phone_call and not connecting_phone.phone_call:
            self.phone_call.append(str(area_code) + "-" + str(other_phone_number))
            connecting_phone.phone_call.append(str(self.area_code) + "-" + str(self.number))
            self.end_call.append(connecting_phone)
            connecting_phone.end_call.append(self)

            print(str(area_code) + "-" + str(other_phone_number),
                  "and", str(self.area_code) + "-" + str(self.number), "have been connected")
        else:
            print("Phone is already in use")

    def disconnect(self):
        """
        This function should return the connection status to disconnected.  You need
        to use new members of this class to determine how the phone is connected to
        the other phone.

        You should also make sure to disconnect the other phone on the other end of the line.
        :return: **depends on your implementation**
        """
        # if the list is not empty it will set the list and the Object inside's phone_call = []
        # this techinally "hangs" up the call because they are no longer connected
        if self.phone_call:
            # sets everything on both ends = [] too hang up
            self.end_call[0].phone_call = []
            self.end_call[0].end_call = []
            self.phone_call = []
            self.end_call = []
            print("The call has been disconnected")

        else:
            # will run if phone_call is empty meaning it is not currently in a call
            print("You can not disconnect the line because it is not in use")

