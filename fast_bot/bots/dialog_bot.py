from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper
from botbuilder.core import MessageFactory,CardFactory
from botbuilder.schema import Attachment, AudioCard, MediaUrl, ThumbnailUrl, ChannelAccount


class DialogBot(ActivityHandler):
    """
    This Bot implementation can run any type of Dialog. The use of type parameterization is to allows multiple
    different bots to be run at different endpoints within the same project. This can be achieved by defining distinct
    Controller types each with dependency on distinct Bot types. The ConversationState is used by the Dialog system. The
    UserState isn't, however, it might have been used in a Dialog implementation, and the requirement is that all
    BotState objects are saved at the end of a turn.
    """

    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        if conversation_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. user_state is required but None was given"
            )
        if dialog is None:
            raise ValueError("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have ocurred during the turn.
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )
    def create_audio_card(self) -> Attachment:
      card = AudioCard()
      card.media = [
          MediaUrl(
              url="https://r1---sn-up1xupob-avne.googlevideo.com/videoplayback?expire=1726797477&ei=RYLsZt3EGN_zsfIPxd7LGQ&ip=209.141.37.75&id=o-ALmLzZQ99wMQVQuYIqiVd0EhO0i56uQkNK6hYfAAuTw6&itag=249&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&siu=1&vprv=1&svpuc=1&mime=audio%2Fwebm&rqh=1&gir=yes&clen=2464725&dur=406.641&lmt=1726241970218950&keepalive=yes&c=ANDROID_TESTSUITE&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Csiu%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRQIgEnj6w5cTA0Tu881CLRwKUkyOYEtxU3e8Oi9cl0hIBTsCIQDIDcYvrg7UnvGkVFdq3lexsG9xM2TRYM5Vr5ihE5Hiuw%3D%3D&range=0-&cms_redirect=yes&mh=BF&mip=102.68.109.1&mm=31&mn=sn-up1xupob-avne&ms=au&mt=1726775579&mv=m&mvi=1&pl=24&lsparams=mh,mip,mm,mn,ms,mv,mvi,pl&lsig=ABPmVW0wRQIgOD_yb9o7uZIdEZ2edpcjwVxSVDYchkg1rhOeyb_qPAgCIQCjZIM17V8enGdp8fCC5TdOviL2clcmO_ARRSeUuLEM-A%3D%3D"
              )
              ]
      card.subtitle = "Testing Audio card"
      card.title = "play audio"
      card.image = ThumbnailUrl(url="https://pypi.org/static/images/logo-small.6eef541e.svg")
      return CardFactory.audio_card(card)
    

    async def on_members_added_activity(
            self, 
            members_added: [ChannelAccount], 
            turn_context: TurnContext
            ):
        cardAtt = self.create_audio_card()
        msg_activity = MessageFactory.attachment(cardAtt)
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(msg_activity)
