# Remove for testing with pylint ;)
# pylint: disable=fixme

# **It took me ? hours to solve this assignment.**
# Solved by (Matrikelnummern): 785812, 786191


import json
import re

from lxml import html

from enum import Enum
import re
import json

import requests
from flask import Blueprint, request, Response

from app import database_holder

from app.models import Image, Caption

BASE = Blueprint('', __name__, url_prefix='')
V1 = Blueprint('v1', __name__, url_prefix='/v1')

BASE_URL_DATASET = 'https://image-annotations.marschke.me/NAACL/'


@V1.route('/health', methods=['GET'])
@BASE.route('/health', methods=['GET'])  # This route exists for the health check of the docker container
def check_health():
    return json.dumps({
        "status": "up",
        "message": "operational",
    }), 200


def get_image_json_object(image):
    caption_list = []

    for caption in image.captions:
        caption_list.append({
            'text': caption.text
        })
    return {
        'id': image.id,
        'category': image.category,
        'captions': caption_list,
    }


@V1.route('/tasks', methods=['GET'])
def get_tasks():
    return json.dumps({
        'taskList': [
            'Answer questions stated in get_answers() (5 Points)',
            'Build API defined in docs/api-definition.yml (precise as possible) (23 Points)',
        ]
    })


# 2 Points code style:
#   Linter (each "real" error -0.5)
#   Readability (up to -2 if very "obfuscated")
#
# Bonus points for really nice solutions and approaches, which aren't covered by our solution / in our opinion nicer
# than in our solution

@V1.route('/answers', methods=['GET'])
def get_answers():
    result = {
        'Is a REST API bound to a single exchange format like JSON? How can multiple formats be used? (1 Point)':
            'It is not! The client can request a particular format using the \'Accepts\' request-header-field and the server.'
            'can specify the format of his reponse in the response\'s header-field \'Content-Type\'.',
        'Are all operations on this REST APIs idempotent? Explain why! (1 Point)':
            'Yes. As specified in the API, even the POST request is idempotent. Normally, this request is not idempotent because it is supposed to create and insert a new value into the'
            'underlying persistent store. Thereby two POST requests to an endpoint of /users would create two'
            'users who both hold their distinct user-id.',
        'Why could it be problematic to work with full URLs as links? Name and explain two reasons (2 Points)': [
            'Without a proper abstraction of the endpoint tree, it could be difficult to maintain consistency in such cases'
            'where the API designers decide to change the routing scheme or even the base url. With relative URLs, this does'
            'not occur as the containing subtree of the routing model can be reattached somewhere else and relative routing'
            'within this subtree would continue to work',
        ],
        'Hand in requirements (1 Point)': [
            'ZIP the complete source code directly from the root directory (so no useless subdirs in ZIP please)',
            'Make an own solution, show us that this is your solution by adding comments where they are needed to '
            'understand your source code',
            'Do not change any file names if not really needed (and then please document).',
            'Do not alter return definitions from functions get_tasks and get_answers.',
            'Write your answers in German or English, in code please write all English.',
            'Please write down your matriculation number at top of this file.',
            'Please add a comment at top of this file how much time you needed for this assignment (please be honest).',
        ]
    }

    for key in result:
        if key != 'Hand in requirements (1 Point)':
            result[key] = '[Solution hidden] Hey, what are you searching? A solution? Tzz. ;)'

    return json.dumps(result), 200


# TODO implement missing routes
# You can request images from the database by executing something like
# for image in Image.select().limit(limit).offset(offset):
#     do something with the image
#
# To access captions, you need to access image.captions for a list of all caption object (more precisely a generator)
#
# For counting all images in DB you can use this command: Image.select().count()
# If using pylint please add # pylint: disable=no-value-for-parameter to the end of the line.
#
# You can access GET arguments by request.args.get('key', 'default') where request is a global object defined by Flask


@V1.route('images/<image_id>/bitmap', methods=['GET'])
def get_image_bitmap(image_id):
    try:
        # read get_image_bitmap parameter and check its constraints
        image_id = int(image_id)
    except ValueError:
        return json.dumps({'error': 'the value has the wrong type'}), 500
    try:
        # Construct url from params
        image = Image.get_by_id(image_id)
        source = BASE_URL_DATASET + image.src
        response = requests.get(source)

        headers = dict(filter(
            lambda header: header[0] in [
                'Content-Type', 'ETag', 'Last-Modified'],
            response.headers.items()
        ))
        return response.content, 200, headers
    except:
        return json.dumps({'error': 'An error occured'}), 500


@V1.route('/images/fetch', methods=['POST'])
def update_image_storage():
    """This operation should clear DB if run multiple times on the same DB

    8 Points: 3 for xpath (1 each), 1 for correct resource GET, 1 for correct DB cleaning, 1 for correct DB saving,
              2 for correct regex, 2 for Transaction explanation
    -0.5 for small mistakes (return value...)

    :return: json if successful or not
    """

    # TODO get BASE_URL_DATASET, we would suggest requests for it (already installed) Think about error handling.
    try:
        page = requests.get(BASE_URL_DATASET)
    except requests.exceptions.Timeout:
        print('A timeout occured.')
        # Maybe set up for a retry, or continue in a retry loop
    except requests.exceptions.TooManyRedirects:
        print('Too many redirects were made.')
        # Tell the user their URL was bad and try a different one
    except requests.exceptions.RequestException as e:
        print('An error occured', e)
        # catastrophic error. bail.
        sys.exit(1)


    # TODO Please explain what this line is doing. Why is it needed? In which case? (directly here as comment)
    # The `with` keyword guarantees that some cleanup routine for the to-be-executed routine is implicitly run
    # after the scope exits. In this particular case, the clean-up-routine is the return statement, such that
    # the 'status': 'finished' value is guaranteed to be sent together with the 200 status code.
    with database_holder.database.transaction():
        # Empty databases
        Image.delete().execute()  # pylint: disable=no-value-for-parameter
        Caption.delete().execute()  # pylint: disable=no-value-for-parameter

        # TODO We encourage you to use the html.fromstring method provided by the lxml package (already installed).
        tree = html.fromstring(page.text)
        
        # "status": "/html/body/table/tr[1000]/td[2]/table/tr[5]/td"
        
        pictureTrees = tree.xpath('/html/body/table/tr');

        # TODO After parsing the XML tree, please use the xpath method to iterate over all elements
        for index, pictureTree in enumerate(pictureTrees, start=1):
            
            # print('processing pictureTree #', index);
                   
            # Extract the source attribute
            src = next(iter(pictureTree.xpath('td[1]/img/@src')), None)
            if src == None:
                continue  # skip entry if no image is in row

            # print('src is ', src);

            # Take only substring with category descriptor
            category = re.match('^(\w.*)\/', src).group(1)
            if category == None:
                continue  # skip entry if category could can't be extracted
            
            # print('category is ', category);

            # Save Image in DB, nothing magical here
            imageDb = Image(src=src, category=category)
            imageDb.save()

            # print('saved image entry!');

            # Save the captions additionally
            for captionTree in pictureTree.xpath('td[2]/table/*/td/text()'):
                # Remove whitespaces on edges
                caption_text = captionTree.strip()
                Caption(text=caption_text, image=imageDb).save()
                
                # print('Added caption', caption_text);

    return json.dumps({'status': 'finished'}), 200
