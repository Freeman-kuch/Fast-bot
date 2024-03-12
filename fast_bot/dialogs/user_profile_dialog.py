# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    PromptOptions,
)
from botbuilder.core import MessageFactory, UserState

from data_models.user_profile import UserBankInformation

from helpers.dialog_helper import prompt_response


class UserProfileDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(UserProfileDialog, self).__init__(UserProfileDialog.__name__)

        self.user_profile_accessor = user_state.create_property("UserBankInformation")   # this creates a place holder to store the users information in the session(sort of)

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.transaction_prompt_step,
                    self.final_step,
                ],
            )
        )
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.initial_dialog_id = WaterfallDialog.__name__

    async def transaction_prompt_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # WaterfallStep always finishes with the end of the Waterfall or with another dialog;
        # here it is a Prompt Dialog. Running a prompt here means the next WaterfallStep will
        # be run when the users response is received.
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("""
Hello there! 👋 I'm your helpful USSD transaction assistant, 
ready to make your Naira bank USSD transactions a breeze!
To initiate a transaction, 
simply provide me with the details in the following format:
    'Send [amount] to [account number] to [receiver's bank] from [your bank name].'

For example:
'Send ₦500 to John Doe's account at Bank XYZ from My GTB Bank.'
        
            """),
            ),
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["transaction_prompt"] = step_context.result  # BULLSEYE THIS IS WHAT I SEND TO THE API.... PREPROCESS???
        testing = await prompt_response(step_context.values["transaction_prompt"])
        await step_context.context.send_activity(testing)
        return await step_context.begin_dialog(self.initial_dialog_id)

    
