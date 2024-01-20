# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class UserBankInformation:
    """
      This is our application state. Just a regular serializable Python class.
    """
    def __init__(self, name: str = None, bank: str = None, account_number: int = 0):  # this would not get to be used for this MVP release
        self.name = name
        self.bank = bank
        self.account_number = account_number
