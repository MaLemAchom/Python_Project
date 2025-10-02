import os, sys, platform, csv
from pathlib import Path
from datetime import datetime

import numpy as np
from PIL import Image

# libs with helpful error messages
try:
    import face_recognition
except Exception:
    print("ERROR: face_recognition not installed in this interpreter.\n"
          "Conda (recommended): conda install -c conda-forge dlib face-recognition")
    raise
try:
    import cv2
except Exception:
    print("ERROR: OpenCV (cv2) not installed in this interpreter.\n"
          "Conda: conda install -c conda-forge opencv")
    raise

FACES_DIR = Path(__file__).parent / "faces"
TOLERANCE = 0.5
PROCESS_EVERY_OTHER_FRAME = True

def load_face_rgb(path: Path) -> np.ndarray:
    # Force to 8-bit RGB so dlib won't crash on RGBA/HEIC/16-bit images
    with Image.open(path) as im:
        im = im.convert("RGB")
        arr = np.array(im, dtype=np.uint8)
    return arr

def discover_known_faces(faces_dir: Path):
    exts = {".jpg", ".jpeg", ".png"}  # keep it simple: work with true JPEG/PNG only
    encodings, names = [], []

    if not faces_dir.exists():
        print(f"Creating faces directory at: {faces_dir}")
        faces_dir.mkdir(parents=True, exist_ok=True)
        print("Add clear, front-facing photos: faces/malem.jpg, faces/rohan.jpg")
        return encodings, names

    files = [p for p in faces_dir.iterdir() if p.suffix.lower() in exts]
    if not files:
        print(f"No face images found in {faces_dir}. Add JPG/PNG images and run again.")
        return encodings, names

    for img_path in files:
        try:
            rgb = load_face_rgb(img_path)
            locs = face_recognition.face_locations(rgb)
            if not locs:
                print(f"[skip] No face detected in: {img_path.name}")
                continue
            enc = face_recognition.face_encodings(rgb, locs)[0]
            name = img_path.stem.replace("_", " ").replace("-", " ").strip()
            name = name[:1].upper() + name[1:]
            encodings.append(enc)
            names.append(name)
            print(f"[ok] Loaded: {img_path.name} -> {name}")
        except Exception as e:
            print(f"[skip] {img_path.name}: {e}")

    return encodings, names

def open_camera():
    if platform.system() == "Darwin" and hasattr(cv2, "CAP_AVFOUNDATION"):
        cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    else:
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam. On macOS, allow Camera access for VS Code/Terminal:\n"
              "System Settings → Privacy & Security → Camera.")
    return cap

def main():
    known_encs, known_names = discover_known_faces(FACES_DIR)
    if not known_encs:
        print("No known faces loaded. Fix your images (real JPEG/PNG) and re-run.")
        sys.exit(1)

    remaining = set(known_names)

    current_date = datetime.now().strftime("%Y-%m-%d")
    csv_name = f"{current_date}.csv"
    new_file = not Path(csv_name).exists()
    f = open(csv_name, "a", newline="")
    writer = csv.writer(f)
    if new_file:
        writer.writerow(["Name", "Timestamp"])

    cap = open_camera()
    if not cap or not cap.isOpened():
        f.close()
        sys.exit(1)

    print("Press 'q' to quit.")
    process = True
    face_locations, face_names = [], []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to read from camera.")
            break

        small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        if not PROCESS_EVERY_OTHER_FRAME or process:
            locs = face_recognition.face_locations(rgb_small)
            encs = face_recognition.face_encodings(rgb_small, locs)
            face_names = []

            for enc in encs:
                matches = face_recognition.compare_faces(known_encs, enc, tolerance=TOLERANCE)
                dists = face_recognition.face_distance(known_encs, enc)
                name = "Unknown"
                if len(dists):
                    i = int(np.argmin(dists))
                    if matches[i]:
                        name = known_names[i]
                face_names.append(name)

                if name != "Unknown" and name in remaining:
                    remaining.remove(name)
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([name, ts])
                    f.flush()
                    print(f"[marked] {name} at {ts}")

            face_locations = locs

        if PROCESS_EVERY_OTHER_FRAME:
            process = not process

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4; right *= 4; bottom *= 4; left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 32), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, f"{name} Present", (left + 6, bottom - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    f.close()
    print(f"Saved attendance to: {csv_name}")

if __name__ == "__main__":
    main()
