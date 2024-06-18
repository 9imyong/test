import subprocess
import cv2
import numpy as np
### sdp test
# RTP 스트리밍을 받을 포트 번호
port_number = 1212

# SDP 파일의 URL
sdp_url = 'http://192.168.50.36:8000/stream.sdp'  # 예시 URL
# FFmpeg 명령어
ffmpeg_command = [
    'D:\\Dev\\tools\\ffmpeg-6.1.1-full_build\\bin\\ffmpeg.exe',
    '-analyzeduration', '100000000',  # 100초 분량으로 설정 (100000000 마이크로초)
    '-probesize', '100000000',  # 100MB로 설정
    '-i', sdp_url,  # SDP 파일의 URL 지정
    '-vf', 'showinfo',  # 비디오 정보 출력 필터 설정 (옵션)
    '-f', 'image2pipe',  # 파이프로 이미지 출력 설정
    '-pix_fmt', 'bgr24',  # 이미지 포맷 설정
    '-vcodec', 'rawvideo',  # 비디오 코덱 설정
    '-'  # stdout으로 프레임을 전달
]
# FFmpeg 프로세스 시작
ffmpeg_process = subprocess.Popen(
    ffmpeg_command,
    stdout=subprocess.PIPE,  # stdout을 파이프로 연결하여 프레임을 읽음
)
while True:
    # stdout으로부터 프레임 데이터 읽기
    raw_frame = ffmpeg_process.stdout.read(1920 * 1080 * 3)  # 적절한 프레임 크기 설정
    if len(raw_frame) != 1920 * 1080 * 3:
        break  # 프레임 크기가 올바르지 않으면 종료

    # raw_frame을 numpy array로 변환
    frame = np.frombuffer(raw_frame, dtype=np.uint8)
    frame = frame.reshape((1080, 1920, 3))  # 프레임 크기에 맞게 reshape

    # OpenCV를 사용하여 프레임 확인
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # 'q' 키를 누르면 종료

# 모든 작업이 끝나면 창 닫기 및 프로세스 종료
cv2.destroyAllWindows()
ffmpeg_process.kill()