import sys
import os
from fastapi import FastAPI, UploadFile,Request,Header,  File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from linebot.v3.exceptions import InvalidSignatureError


from dotenv import load_dotenv

# เพิ่มโฟลเดอร์ app เข้าไปใน sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# นำเข้าโมดูลจากโฟลเดอร์ app
from app.handlers.line_handler import handler
from app.services.image_service import predict_image
from app.utils.db_utils import connect_db, close_db

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


    
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    


