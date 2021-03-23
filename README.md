# computervision_template
This is template project for starting computer vision wok with all the libs and boiler plate code for logging,exception,flask etc.

# Test End point Method:
    - This is just to see if on start of app, we are able to read params and send sample response.
    - To trigger this test:
        1. Start this project as flask or gunicorn app:
            flask run
            or
            ./start-gunicorn.sh
        2. Send request as:
            curl -F 'img=https://i.ibb.co/C0fhFZy/staticmap.png'  -F param1=[[672,525],[664,703],[632,717],[606,740],[635,751]] "http://localhost:9898/test/path"

