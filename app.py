from bottle import Bottle, route, run, template, static_file
import os
import sys
import requests

IMAGES_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/images'
IMAGE_SRV = os.environ.get('IMAGE_SRV', None)

if IMAGE_SRV:
    ''' If the environment variable IMAGE_SRV exists, try to open it.
    If no luck exit immediately.
    '''
    images_txt_url = 'http://' + IMAGE_SRV + '/images.txt'
    resp = requests.get(images_txt_url)
    if resp.status_code == 200:
        images_in_textfile = [ line for line in resp.text.splitlines()]
    else:
        sys.exit('No ' + images_txt_url + ' found.')

app = Bottle()

@app.get('/')
def index():
    ''' Show the default page.

    Passing image list to the "base.tpl" template, The template creates <img>
    tags for all filenames in the list.
    '''
    if IMAGE_SRV:
        images = images_in_textfile
    else:
        images = os.listdir(IMAGES_FOLDER)
    return template('base', images=images)

@app.get('/images/<image>')
def serve_pictures(image):
    ''' Serving images form here,

    - either as local static files
    - or proxied from IMAGE_SRV.'''
    if IMAGE_SRV:
        return requests.get('http://' + IMAGE_SRV + '/' + image).content
    else:
        return static_file(image, root=IMAGES_FOLDER)

if __name__ == '__main__':
    run(app, host = '0.0.0.0', port = 3000, reloader=True, debug=True)
