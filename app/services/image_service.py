from ultralytics import YOLO # type: ignore
import json
import os




def predict_image(image_path: str):
    print("[debug] Detecting.. call function")
    result_to_client = []
    model = YOLO("best.pt")
    result = model(image_path)
    predicted_names = [model.names[int(box.cls)] for box in result[0].boxes]
    predicted_confidences = [box.conf for box in result[0].boxes]

    if (len(predicted_names) == 0):
        result_to_client.append(
            {
                "name": "ไม่สามารถระบุได้",
                "confidence": 0.0,
                "predict": "ไม่สามารถระบุได้"
            }
        )
        return result_to_client
    confidence = round(predicted_confidences[0].item(), 2)
    print("[debug] Result : ", predicted_names) 
    print("[debug] Confidence : ", confidence)  
    
    
    for name in predicted_names:
        if (confidence <= 0.5): 
            result_to_client.append(
                {
                    "name": "ไม่สามารถระบุได้",
                    "confidence": confidence,
                    "predict": "ไม่สามารถระบุได้"
                }
            ) 
            return result_to_client


        if (name == "greencurry"):
           result_to_client.append(
               {
                   "name": "เเกงเขียวหวาน", 
                   "confidence": confidence
                }
            )
        elif (name == "red_pork_withRice"):
            result_to_client.append(
                {
                    "name": "ข้าวหมูเเดง",
                    "confidence": confidence
                }
            )
        elif (name == "stir_fried_basil"):
            result_to_client.append(
                {
                    "name": "ผัดกะเพรา",
                    "confidence": confidence
                }
            )
        


    return result_to_client