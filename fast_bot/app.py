import sys
import traceback
from datetime import datetime
from starlette import status
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from botbuilder.core import (
    ConversationState,
    MemoryStorage,
    TurnContext,
    UserState,
)
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity, ActivityTypes

from config import DefaultConfig 
from dialogs import UserProfileDialog  # starting from here and moving forward
from bots import DialogBot

CONFIG = DefaultConfig()

APP = FastAPI()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error]: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.now(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )

        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)

    # Clear out state
    await CONVERSATION_STATE.delete(context)


# Set the error handler on the Adapter.
# In this case, we want an unbound method, so MethodType is not needed.
ADAPTER.on_turn_error = on_error

# Create MemoryStorage, UserState and ConversationState
MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)  # we can use redis for this, just configure this and pass it to the
# dialogue
USER_STATE = UserState(MEMORY)

# create main dialog and bot
DIALOG = UserProfileDialog(USER_STATE)
BOT = DialogBot(CONVERSATION_STATE, USER_STATE, DIALOG)  # would need to redefine this to my custom bot, mostlikely to be an echo bot template anyway


# Listen for incoming requests on /api/messages.
@APP.post("/api/messages")
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(auth_header, activity, BOT.on_turn)  # this is where we forward
    # the request to the adapter
    if response:
        return JSONResponse(data=response.body, status_code=response.status)
    return Response(status_code=status.HTTP_200_OK)

# to run
# uvicorn app:APP --reload
