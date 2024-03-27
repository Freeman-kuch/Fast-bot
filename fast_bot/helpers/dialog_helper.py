# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus
import requests


class DialogHelper:
    @staticmethod
    async def run_dialog(
        dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(dialog.id)





async def prompt_response(prompt):
    data = {"prompt": prompt}
    url = "https://finbot-api-f971cbaa66ee.herokuapp.com/mvp/prompt"
    headers = {
    "Content-Type": "application/json",
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        return response.json()["detail"]
    return str(response.json()["code"]).replace("*", "* ")