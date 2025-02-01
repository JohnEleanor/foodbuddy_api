import sys
import os
from fastapi import FastAPI, UploadFile,Request,Header,  File, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from linebot.v3.exceptions import InvalidSignatureError
# from bs4 import BeautifulSoup
import requests
import json
from pydantic import BaseModel


from dotenv import load_dotenv

# เพิ่มโฟลเดอร์ app เข้าไปใน sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# นำเข้าโมดูลจากโฟลเดอร์ app
from app.handlers.line_handler import handler
from app.services.image_service import predict_image
from app.utils.db_utils import connect_db, close_db
from app.services.find_food import get_food_data

import os
import shutil

def remove_pycache(directory="."):
    for root, dirs, files in os.walk(directory):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache_path)
            print(f"Removed: {pycache_path}")



load_dotenv()
remove_pycache()

app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get("/health")
def health():
    connection = connect_db()
    if connection:
        try:
            return {"status": "ok", "message": "Connection successful"}
        finally:
            close_db(connection)
    else:
        return {"status": "error", "message": "Connection failed"}

@app.post("/predict")
async def upload_image(image: UploadFile = File(...)):
    """
    Object Detection from an image.

    Args:
        image (UploadFile): The image file uploaded.
    Returns:
        dict: JSON format containing the Object Detection result.
    """
    try:
        # สร้างไฟล์ชั่วคราวและบันทึกไฟล์
        file_location = f"images/{image.filename}"

        with open(file_location, "wb") as file:
            image = file.write(await image.read())
            if (image):
                predict_result = predict_image(file_location)
                print(predict_result)
                if (predict_result):
                    file.close() # ปิดไฟล์
                    os.remove(file_location) # ลบไฟล์
                    return {"message": "Upload successful", "result": predict_result}
            else:
                return JSONResponse(status_code=400, content={"message": "Upload failed"})  
    
            
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Upload failed: {str(e)}"})

@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    body_str = body.decode('utf-8')
    try:
        handler.handle(body_str, x_line_signature)
        print("Received frome LINE")
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(status_code=400, detail="Invalid signature.")

    return 'OK'


# --------------------------------------------------------
# Pydantic model สำหรับ request body
class FoodRequest(BaseModel):
    name: str  # ชื่ออาหารที่ต้องการค้นหา


@app.post("/search_by_name")
def search_food(request: FoodRequest):
    """
    ค้นหาข้อมูลอาหารตามชื่อจาก ThaiFCD และดึง food_id
    """
    name = request.name  # รับชื่ออาหารจาก request body

    # โหลดข้อมูล JSON ที่เก็บข้อมูลอาหาร
    with open('food_data.json', 'r', encoding='utf-8') as file:
        load_json = json.load(file)

    # ตัวแปรเก็บข้อมูลอาหาร
    data = []

    # ทำการค้นหาข้อมูลอาหารจาก JSON
    for food in load_json:
        keyword_thai = food.get('Thai_name')
        keyword_thai_3 = keyword_thai.split(',')

        # วนลูปเช็คแต่ละคำในชื่ออาหาร
        for keyword in keyword_thai_3:
            if keyword.strip() == name.strip():  # เพิ่มการใช้ strip() เพื่อหลีกเลี่ยงปัญหาจากช่องว่าง
                food_item = {
                    'thai_name': food.get('Thai_name'),
                    'eng_name': food.get('English_name'),
                    'nutrition': food.get('nutrition')
                }
                data.append(food_item)
                break  # ถ้าค้นพบแล้วหยุดค้นหาต่อในคำอื่นๆ

    # ตรวจสอบว่ามีข้อมูลหรือไม่
    if data:
        return {"message": "ค้นหาข้อมูลสำเร็จ", "data": data}
    else:
        return {"message": "ไม่พบข้อมูลสำหรับชื่ออาหารนี้"}


class FoodRequest(BaseModel):
    name: str  # ชื่ออาหารที่ต้องการค้นหา 

@app.post("/search_food")
def search_from_database(request: FoodRequest):
    name = request.name  # รับชื่ออาหารจาก request body

    data = get_food_data(name)
    return {"data": data, "param" : name}
    


   
    
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
