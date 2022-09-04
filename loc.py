from google.cloud import vision
from google.cloud.vision_v1 import types
import cv2 
import pandas as pd
from web import web_stuff
def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    #print('Number of objects found: {}'.format(len(objects)))
    #for object_ in objects:
    #    print('\n{} (confidence: {})'.format(object_.name, object_.score))
    #    print('Normalized bounding polygon vertices: ')
    #    for vertex in object_.bounding_poly.normalized_vertices:
    #        print(' - ({}, {})'.format(vertex.x, vertex.y))
    return(objects)

def add_rect(image,label,x1,y1,x2,y2):
    x1 = int(x1*image.shape[1])
    y1= int(y1*image.shape[0])
    x2 = int(x2*image.shape[1])
    y2 = int(y2*image.shape[0])
    start_point = (x1,y1)
    end_point = (x2,y2)
    color = (0, 0, 255)
    thickness = 2
    image = cv2.rectangle(image, start_point, end_point, color, thickness)
    font = 0.5
    thick = 1
    if (image.shape[1] < 450):
        font = 0.3
        thick = 1
    elif (image.shape[1] < 900):
        font = 0.6
        thick = 2
    elif (image.shape[1] >= 900):
        font = 0.7
        thick = 3 
    if (y1-20 < 0):
        image = cv2.putText(image, label, (x1, y1+10), cv2.FONT_HERSHEY_SIMPLEX, font, (36,255,12), thick)
    else:
        image = cv2.putText(image, label, (x1, y1-20), cv2.FONT_HERSHEY_SIMPLEX, font, (36,255,12), thick)
    return(image)

def see(path,objects):
    l_label = []
    l_score = []
    l_x1 = []
    l_y1 = []
    l_x2 = []
    l_y2 = []
    image = cv2.imread(path)
    for object_ in objects:
        score = str(object_.score)
        label = object_.name +' '+ score[:4]
        count = 1
        for vertex in object_.bounding_poly.normalized_vertices:
            if count == 1:
                x1 = vertex.x
                y1 = vertex.y
            if count == 3:
                x2 = vertex.x
                y2 = vertex.y
            count += 1
        image = add_rect(image,label,x1,y1,x2,y2)
        l_label.append(object_.name)
        l_score.append(object_.score)
        l_x1.append(x1)
        l_y1.append(y1)
        l_x2.append(x2)
        l_y2.append(y2)
        
    data = {'Label':l_label,
            'Score':l_score,
            'x1':l_x1,
            'y1':l_y1,
            'x2':l_x2,
            'y2':l_y2
           }
    df = pd.DataFrame(data)
    return(image,df)

def find_prop(path,objects):
    image,df = see(path,objects)

    scale_percent = 50000/image.shape[0]
    width = int(image.shape[1] * scale_percent / 100)
    #height = int(image.shape[0] * scale_percent / 100)
    dim = (width, 500)

    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return(image,df)