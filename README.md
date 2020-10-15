# Images Web Server

Images Web Server is an example app written in Python used on Docker classes. The app serves images.

## Setup
### Requriements
Install module dependenices with PIP:  
`pip3 install -r requirements.txt`  

The following modules (and their dependencies) will be installed:
- Bottle
- requests
- gunicorn (for "production" environments)

### Running the server
`python3 app.py` will run the server in development / debug mode using port 3000. You can open the site using http://localhost:3000/ .  
`gunicorn--bind 0.0.0.0:8000 --workers 3 app` will run the server in "production" mode on port 8000.

## Server modes
### Non-proxy mode
By default the server serves all image files found in the `images` folder. The server does not check whether non-image files are present in this folder. If present, they are likely to cause problems since the code generates `<img src="/images/file.ext">` tags for any files found.

### Proxy mode
If an environment variable called `IMAGE_SRV` is found then the server tries to load the `http://IMAGE_SRV/images.txt` file when starting up. If file is not found, the server exists. If the file is found then the images listed inside will be proxied on the page displayed by Images Web Server. The images should be available at http://IMAGE_SRV/filename.ext.

### `images.txt` file format
```
image_file1.jpg
image_file2.png
<no newline at the end>
```
