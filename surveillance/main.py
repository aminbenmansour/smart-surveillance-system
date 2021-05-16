import os
import cv2
import face_recognition
import numpy as np
from alert import alert_led, alert_buzz




video_capture = cv2.VideoCapture(0)


#Store objects in array
known_person=[] #Name of person string
known_image=[] #Image object
known_face_encodings=[] #Encoding object

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

is_alerting = False


#Loop to add images in friends folder
for file in os.listdir("profiles"):
    try:
        #Extracting person name from the image filename eg: david.jpg
        known_person.append(file.replace(".jpg", ""))
        file=os.path.join("profiles/", file)
        known_image = face_recognition.load_image_file(file)
        #print(face_recognition.face_encodings(known_image)[0])
        known_face_encodings.append(face_recognition.face_encodings(known_image)[0])
        #print(known_face_encodings)

    except Exception as e:
        pass


while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    #

    # Only process every other frame of video to save time
    if process_this_frame:
        if not 'th_led' in locals() and not 'th_buzz' in locals():
            th_led = alert_led()
            th_buzz = alert_buzz()

        #Known people existence
        first_match_index = False

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Intruder"


            #Match Known faces to the most close captured faces based to encoding
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding) 

            #Raising ValueError when profile is empty
            try:
                best_match_index = np.argmin(face_distances)
            except ValueError:
                pass


            if matches[best_match_index]:
                name = known_person[best_match_index]

            face_names.append(name)


            unknown_exists = True if "Intruder" in face_names else False
            first_match_index = True if True in matches else False

            condition_alert = unknown_exists and not first_match_index and not is_alerting 
            condition_unalert = first_match_index and is_alerting

        


            if condition_alert:
                th_led.start()
                th_buzz.start()

                is_alerting = True

            elif condition_unalert:
                th_led.stop()
                th_buzz.stop()

                is_alerting = False

                del th_led
                del th_buzz
                


    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        print(len(face_locations))
        print(face_names)
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 255, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 10, bottom - 10), font, 1.0, (0, 0, 0), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()