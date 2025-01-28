from linebot.v3.messaging import FlexMessage, FlexContainer

def create_flex_bubble(image_url, predict_result):
    print("[debug] Predict Results : ", predict_result)
    percent = round(predict_result[0]['confidence'] * 100, 2)
    # percent = 100 if predict_result[0]['confidence'] == 0 else round(predict_result[0]['confidence'] * 100, 2)
    print("[debug] Percent : ", percent)
    bubble_string = f"""
                        {{
                    "type": "bubble",
                    "body": {{
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {{
                                "type": "text",
                                "text": "Foodbuddy",
                                "weight": "bold",
                                "color": "#1DB446",
                                "size": "sm"
                            }},
                            {{
                                "type": "text",
                                "text": "{predict_result[0]['name']}",
                                "weight": "bold",
                                "size": "xxl",
                                "margin": "md"
                            }},
                            {{
                                "type": "text",
                                "text": "ความมั่นใจ: {percent} %",
                                "size": "xs",
                                "color": "#aaaaaa",
                                "wrap": true
                            }},
                            {{
                                "type": "separator",
                                "margin": "xxl"
                            }},
                            {{
                                "type": "box",
                                "layout": "vertical",
                                "margin": "xxl",
                                "spacing": "sm",
                                "contents": [
                                {{
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {{
                                        "type": "text",
                                        "text": "หมู",
                                        "size": "sm",
                                        "color": "#555555",
                                        "flex": 0
                                    }},
                                    {{
                                        "type": "text",
                                        "text": "300 cal",
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end"
                                    }}
                                    ]
                                }},
                                {{
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {{
                                        "type": "text",
                                        "text": "หมู",
                                        "size": "sm",
                                        "color": "#555555",
                                        "flex": 0
                                    }},
                                    {{
                                        "type": "text",
                                        "text": "300 cal",
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end"
                                    }}
                                    ]
                                }},
                                {{
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {{
                                        "type": "text",
                                        "text": "หมู",
                                        "size": "sm",
                                        "color": "#555555",
                                        "flex": 0
                                    }},
                                    {{
                                        "type": "text",
                                        "text": "300 cal",
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end"
                                    }}
                                    ]
                                }},
                                {{
                                    "type": "separator",
                                    "margin": "xxl"
                                }},
                                {{
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "xxl",
                                    "contents": [
                                    {{
                                        "type": "text",
                                        "text": "น้ำตาล",
                                        "size": "sm",
                                        "color": "#555555"
                                    }},
                                    {{
                                        "type": "text",
                                        "text": "3 กรัม",
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end"
                                    }}
                                    ]
                                }},
                                {{
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {{
                                        "type": "text",
                                        "text": "คาร์โบไฮเดรต",
                                        "size": "sm",
                                        "color": "#555555"
                                    }},
                                    {{
                                        "type": "text",
                                        "text": "30 กรัม",
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end"
                                    }}
                                    ]
                                }},
                                {{
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {{
                                        "type": "text",
                                        "text": "ไขมัน",
                                        "size": "sm",
                                        "color": "#555555"
                                    }},
                                    {{
                                        "type": "text",
                                        "text": "99 กรัม",
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end"
                                    }}
                                    ]
                                }},
                                {{
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {{
                                        "type": "text",
                                        "text": "โปรตีน",
                                        "size": "sm",
                                        "color": "#555555"
                                    }},
                                    {{
                                        "type": "text",
                                        "text": "55 กรัม",
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end"
                                    }}
                                    ]
                                }}
                                ]
                            }}
                        ]
                    }},
                    "footer": {{
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {{
                            "type": "button",
                            "action": {{
                            "type": "message",
                            "label": "เเก้ไขเมนู",
                            "text": "เเก้ไขเมนู"
                            }},
                            "margin": "xs",
                            "height": "sm",
                            "style": "primary"
                        }}
                        ],
                        "position": "relative"
                    }},
                    "styles": {{
                        "footer": {{
                        "separator": true
                        }}
                    }}
                    }}
    """
    message = FlexMessage(alt_text="hello", contents=FlexContainer.from_json(bubble_string))
    return message