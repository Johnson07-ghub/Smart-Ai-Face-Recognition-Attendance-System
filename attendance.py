import cv2
import face_recognition
import pickle
import pandas as pd
from datetime import datetime

# ================= LOAD TRAINED ENCODINGS =================

with open("trainer/encodings.pkl", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

# ================= CAMERA =================

cap = cv2.VideoCapture(0)

marked_names = set()

print("Face Recognition Attendance System Started")

# ================= MAIN LOOP =================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Resize for faster processing
    small_frame = cv2.resize(
        frame,
        (0, 0),
        fx=0.25,
        fy=0.25
    )

    rgb_small = cv2.cvtColor(
        small_frame,
        cv2.COLOR_BGR2RGB
    )

    # Detect Faces
    face_locations = face_recognition.face_locations(
        rgb_small
    )

    face_encodings = face_recognition.face_encodings(
        rgb_small,
        face_locations
    )

    # ================= RECOGNITION =================

    for face_encoding, face_location in zip(
        face_encodings,
        face_locations
    ):

        matches = face_recognition.compare_faces(
            known_encodings,
            face_encoding,
            tolerance=0.50
        )

        name = "Unknown Person"

        face_distances = face_recognition.face_distance(
            known_encodings,
            face_encoding
        )

        if len(face_distances) > 0:

            best_match_index = face_distances.argmin()

            if matches[best_match_index]:
                name = known_names[best_match_index]

        # Restore original frame coordinates

        top, right, bottom, left = face_location

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # ================= DRAW BOX =================

        if name != "Unknown Person":

            color = (0, 255, 0)

            if name not in marked_names:

                now = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                pd.DataFrame(
                    [[name, now]]
                ).to_csv(
                    "attendance.csv",
                    mode="a",
                    header=False,
                    index=False
                )

                marked_names.add(name)

                print(f"{name} marked present")

        else:

            color = (0, 0, 255)

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            color,
            3
        )

        cv2.rectangle(
            frame,
            (left, bottom - 35),
            (right, bottom),
            color,
            cv2.FILLED
        )

        cv2.putText(
            frame,
            name,
            (left + 6, bottom - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    # ================= DISPLAY =================

    cv2.imshow(
        "AI Face Recognition Attendance System",
        frame
    )

    key = cv2.waitKey(1)

    if key == 27:  # ESC Key
        break

# ================= CLEANUP =================

cap.release()
cv2.destroyAllWindows()