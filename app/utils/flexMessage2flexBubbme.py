from linebot.models import BubbleContainer, BoxComponent, TextComponent, SeparatorComponent

def convert_flex_json_to_bubble(flex_json):
    """ แปลง JSON Flex Message ไปเป็น FlexBubble ของ LINE SDK """
    def parse_component(component):
        """ แปลงองค์ประกอบต่างๆ ใน JSON ไปเป็น LINE SDK Components """
        if component["type"] == "text":
            return TextComponent(
                text=component["text"],
                size=component.get("size"),
                color=component.get("color"),
                weight=component.get("weight"),
                align=component.get("align"),
                margin=component.get("margin"),
                wrap=component.get("wrap", False),
                flex=component.get("flex")
            )
        elif component["type"] == "separator":
            return SeparatorComponent(margin=component.get("margin"))
        elif component["type"] == "box":
            return BoxComponent(
                layout=component["layout"],
                margin=component.get("margin"),
                spacing=component.get("spacing"),
                contents=[parse_component(content) for content in component["contents"]]
            )
        return None

    body = parse_component(flex_json["body"])
    
    return BubbleContainer(body=body)