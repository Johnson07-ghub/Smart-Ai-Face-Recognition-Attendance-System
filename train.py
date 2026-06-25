import os
import cv2
import pickle
import face_recognition

dataset_path = "DataSets"

known_encodings = []
known_names = []

print("Starting Training...\n")

for person in os.listdir(dataset_path):

    person_path = os.path.join(dataset_path, person)

    if not os.path.isdir(person_path):
        continue

    print(f"Processing Folder: {person}")

    for img_name in os.listdir(person_path):

        img_path = os.path.join(person_path, img_name)

        try:

            image = cv2.imread(img_path)

            if image is None:
                print(f"Cannot Read Image: {img_path}")
                continue

            rgb = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

            encodings = face_recognition.face_encodings(rgb)

            if len(encodings) > 0:

                known_encodings.append(encodings[0])
                known_names.append(person)

                print(f"Added: {img_name}")

            else:

                print(f"No Face Found: {img_name}")

        except Exception as e:

            print(f"Error Processing {img_name}")
            print(e)

print("\nTraining Complete")
print("Total Face Samples:", len(known_names))

data = {
    "encodings": known_encodings,
    "names": known_names
}

os.makedirs("trainer", exist_ok=True)

with open("trainer/encodings.pkl", "wb") as f:
    pickle.dump(data, f)

print("\nModel Saved Successfully")
print("Location: trainer/encodings.pkl")