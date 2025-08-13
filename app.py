from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
from face_recognition_module import detect_and_encode, recognize_faces

app = FastAPI(title="Face Recognition API")

@app.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    # Đọc ảnh upload
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Phát hiện & encode faces
    test_encodings = detect_and_encode(img_rgb)

    # Nhận diện
    results = recognize_faces(test_encodings)
    return {"results": results}
from fastapi.responses import HTMLResponse

@app.get("/upload", response_class=HTMLResponse)
async def upload_page():
    return """
    <h2>Face Recognition Upload</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/*">
      <button type="submit">Upload</button>
    </form>
    """

@app.post("/upload", response_class=HTMLResponse)
async def handle_upload(file: UploadFile):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    test_encodings = detect_and_encode(img_rgb)
    results = recognize_faces(test_encodings)

    # Hiển thị kết quả
    result_html = "<h3>Kết quả nhận diện:</h3><ul>"
    for r in results:
        result_html += f"<li>{r['name']} - Box: {r['box']} - Distance: {r['distance']}</li>"
    result_html += "</ul>"
    return result_html
from fastapi.responses import HTMLResponse

@app.get("/upload", response_class=HTMLResponse)
async def upload_page():
    return """
    <h2>Face Recognition Upload</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/*">
      <button type="submit">Upload</button>
    </form>
    """
@app.post("/upload", response_class=HTMLResponse)
async def handle_upload(file: UploadFile):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    test_encodings = detect_and_encode(img_rgb)
    results = recognize_faces(test_encodings)

    result_html = "<h3>Kết quả nhận diện:</h3><ul>"
    for r in results:
        result_html += f"<li>{r['name']} - Box: {r['box']} - Distance: {r['distance']}</li>"
    result_html += "</ul>"
    return result_html


