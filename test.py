import os
import time
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/mnt/d/Cloud/vision api-61625b706645.json"
def detect_landmarks(path):
    """Detects landmarks in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    print('Landmarks:')

    for landmark in landmarks:
        print(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('Latitude {}'.format(lat_lng.latitude))
            print('Longitude {}'.format(lat_lng.longitude))

detect_landmarks("/mnt/d/taj.jpg")
print(time.time())