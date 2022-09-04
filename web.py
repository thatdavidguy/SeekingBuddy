def web_stuff(path):
    import os, io
    import pandas as pd
    credential_path = "ServiceAccountToken.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.web_detection(image=image)
    annotations = response.web_detection
    
    if annotations.best_guess_labels:
        l_label = []
        for label in annotations.best_guess_labels:
            print('\nBest guess label: {}'.format(label.label))
            l_label.append(label.label)
    my_confidence = 0
    if annotations.pages_with_matching_images:
        print('\nPages with matching images found'.format(
            len(annotations.pages_with_matching_images)))
        my_confidence += len(annotations.pages_with_matching_images) * 0.7
        print('ADDED: {} TO MYCONFIDENCE'.format(len(annotations.pages_with_matching_images) * 0.7))
       # for page in annotations.pages_with_matching_images:
        #    if page.full_matching_images:
         #       for image in page.full_matching_images:
          #          print('\t\tImage url  : {}'.format(image.url))
           # if page.partial_matching_images:
            #    for image in page.partial_matching_images:
             #       print('\t\tImage url  : {}'.format(image.url))
                    
    if annotations.visually_similar_images:
        print('\n{} visually similar images found'.format(
            len(annotations.visually_similar_images)))
        my_confidence += len(annotations.visually_similar_images) * 0.3
        print('ADDED: {} TO MYCONFIDENCE'.format(len(annotations.visually_similar_images) * 0.3))

    #    for image in annotations.visually_similar_images:
    #        print('\tImage url    : {}'.format(image.url))
            
    if annotations.web_entities:
        print('\n{} Web entities found'.format(
            len(annotations.web_entities)))
        l_score = []
        l_desc = []
        for entity in annotations.web_entities:
            if (entity.score > 0.6):
                print('\n\tScore      : {}'.format(entity.score))
                print(u'\tDescription: {}'.format(entity.description))
            l_score.append(entity.score)
            l_desc.append(entity.description)
        data = {'Description':l_desc,
            'Score':l_score,
           }
        df = pd.DataFrame(data)
    print("\nMy confidence: {}".format(my_confidence))
    return(l_label,df,my_confidence,annotations)