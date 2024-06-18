from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import cv2

app = FastAPI()

def list_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

def get_camera():
    cameras = list_cameras()
    if not cameras:
        raise HTTPException(status_code=404, detail="No camera found")
    cap = cv2.VideoCapture(cameras[0])  # 첫 번째 사용 가능한 카메라를 선택합니다.
    return cap

def generate_frames():
    cap = get_camera()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get('/video_feed')
async def video_feed():
    return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
