from linebot.v3 import WebhookHandler
from linebot.v3.messaging import ApiClient, Configuration, MessagingApi, MessagingApiBlob, ReplyMessageRequest, TextMessage,  FlexBubble, FlexImage, FlexBox, FlexText, FlexIcon, FlexButton, URIAction,  QuickReply,QuickReplyItem, MessageAction, CameraAction
from linebot.v3.webhooks import MessageEvent, TextMessageContent, ImageMessageContent, FollowEvent
from linebot.v3.messaging.models.show_loading_animation_request import ShowLoadingAnimationRequest
from services.image_service import predict_image
from utils.create_flex import create_flex_bubble
from utils.file_utils import save_image, remove_image
import os
from dotenv import load_dotenv

load_dotenv()

get_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
configuration = Configuration(access_token=get_access_token)

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image(event: ImageMessageContent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)
        line_bot_api.show_loading_animation(
            ShowLoadingAnimationRequest(
                chat_id=event.source.user_id,
                loadingSeconds=10
            )
        )
        file_name = save_image(event.message.id, line_bot_blob_api)
        if file_name:
            predict_result = predict_image(file_name)
            
            image_url = f"{os.getenv('API_URL')}/images/{event.message.id}.jpg"
            bubble = create_flex_bubble(image_url, predict_result)
            

            for item in predict_result:
                if (item["name"] == "ไม่สามารถระบุได้"):
                    line_bot_api.reply_message(
                    reply_message_request=ReplyMessageRequest(
                            replyToken=event.reply_token,
                            messages=[TextMessage(text="ขอโทษด้วย ฉันไม่สามารถเข้าใจรูปภาพอาหารได้ คะ")]
                        )
                    )
                else: 
                    line_bot_api.reply_message(
                    reply_message_request=ReplyMessageRequest(
                            replyToken=event.reply_token,
                            messages=[bubble, TextMessage(text="คุณต้องการบันทึกหรือไม่ถ้าต้องการให้พิพม์ 'บันทึก' ")]
                        )
                    )

            

          

            print(f"Removed: {file_name}")
            remove_image(file_name)

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        
        if event.message.text == "เเก้ไขเมนู":
            line_bot_api.reply_message(
                reply_message_request=ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[TextMessage(text="โปรดป้อนชื่อเมนูที่ถูกต้องหนูหน่อยค่ะ!")]
                )
            )
        
        else:
            line_bot_api.reply_message(
                reply_message_request=ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[TextMessage(text="สวัสดีค่า!", quick_reply = create_quick_reply())]
                )
            )


@handler.add(FollowEvent)
def handle_follow(event: FollowEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        reply_item = create_quick_reply()
        line_bot_api.reply_message(
            reply_message_request=ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[TextMessage(text="สวัสดีค่า!", quick_reply = reply_item)]
            )
        )



def create_quick_reply():
    quick_reply = QuickReply(
        items=[
           
            QuickReplyItem(
                action=CameraAction(label="ถ่ายรูปอาหาร"),
            ),
            QuickReplyItem(
                action=URIAction(label="ดูประวิติการกินอาหาร",uri="https://web-foodbuddy.vercel.app/")
            ),
            QuickReplyItem(
                action=URIAction(label="ตั้งเป้าหมายสุขภาพ",uri="https://web-foodbuddy.vercel.app/")
            ),
        ]
    )
    return quick_reply


