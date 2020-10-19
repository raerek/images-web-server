from bottle import Bottle, route, run, template, static_file
import os
import sys
import requests

IMAGES_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/images'
IMAGE_SRV = os.environ.get('IMAGE_SRV', None)

app = Bottle()

@app.get('/')
def index():
    ''' Show the default page.

    Passing image list and hostname to the "base.tpl" template.
    The template in retrun displays the hostname in the title,
    and the images as the content of the page.

    If the environment variable IMAGE_SRV exists, try to open it.
    If no luck exit immediately.
    '''
    error_message = None
    if IMAGE_SRV:
        images_txt_url = 'http://' + IMAGE_SRV + '/images/remote-images.txt'
        try:
            resp = requests.get(images_txt_url)
            images = [ line for line in resp.text.splitlines()]
        except requests.exceptions.RequestException as e:
            images = None
            error_message = 'No ' + images_txt_url + ' found.'
    else:
        images = [ f for f in os.listdir(IMAGES_FOLDER) if os.path.splitext(f)[1].lower() in [".jpg", ".jpeg", ".png"] ]
    hostname = os.uname().nodename # Does not work on Windows.
    return template('base', images=images, hostname=hostname, error_message=error_message)

@app.get('/images/<image>')
def serve_pictures(image):
    ''' Serving images form here,

    - either as local static files
    - or proxied from IMAGE_SRV.
    '''
    if IMAGE_SRV:
        try:
            # server answered
            image_url = 'http://' + IMAGE_SRV + '/images/' + image
            resp = requests.get(image_url)
            if resp.status_code == 200:
                return resp.content
            else:
                # most likely 404, but we catch all for now
                raise requests.exceptions.RequestException()
        except requests.exceptions.RequestException as e:
            # server did not answer, or bad anser
            # We send back an image with an error meassage since we are
            # in the middle of a webpage requesting images.
            return static_file('proxy_error.png', root=os.path.dirname(os.path.realpath(__file__)))
    else:
        # sending back local image
        return static_file(image, root=IMAGES_FOLDER)

if __name__ == '__main__':
    run(app, host = '0.0.0.0', port = 3000, reloader=True, debug=False)
