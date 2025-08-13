import cv2
import numpy as np
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN

# Initialize models
mtcnn = MTCNN(keep_all=True)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Define known faces
known_faces = {
    "Dam Thuy Hien": "Face-recognition-bug-fixes/Images/hien.jpg",
    "Dam Minh Long": "Face-recognition-bug-fixes/Images/long.jpg"
}

# Functions
def detect_and_encode(image):
    with torch.no_grad():
        boxes, _ = mtcnn.detect(image)
        faces = []
        if boxes is not None:
            for box in boxes:
                face = image[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                if face.size == 0:
                    continue
                face = cv2.resize(face, (160, 160))
                face = np.transpose(face, (2, 0, 1)).astype(np.float32) / 255.0
                face_tensor = torch.tensor(face).unsqueeze(0)
                encoding = resnet(face_tensor).detach().numpy().flatten()
                faces.append((encoding, list(map(int, box))))
        return faces

def encode_known_faces(known_faces):
    encodings = []
    names = []
    for name, path in known_faces.items():
        img = cv2.imread(path)
        if img is not None:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_enc = detect_and_encode(img_rgb)
            if face_enc:
                encodings.append(face_enc[0][0])
                names.append(name)
    return encodings, names

known_face_encodings, known_face_names = encode_known_faces(known_faces)

def recognize_faces(test_encodings, threshold=0.6):
    results = []
    for enc, box in test_encodings:
        distances = np.linalg.norm(np.array(known_face_encodings) - enc, axis=1)
        min_idx = np.argmin(distances)
        if distances[min_idx] < threshold:
            results.append({"name": known_face_names[min_idx], "box": box, "distance": float(distances[min_idx])})
        else:
            results.append({"name": "Not Recognized", "box": box, "distance": float(distances[min_idx])})
    return results
