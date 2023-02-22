# Meduzzen internship

## To start the app
1 option: Open "Meduzzen-internship\app" folder and run "uvicorn main:app" or "uvicorn main:app --reload" if you want to reload a server automatically when you update your code.
2 option: Open "Meduzzen-internship\app" folder and run "python main.py".

## To run tests
In "Meduzzen-internship" folder run "python -m pytest".

## To start docker
-In "Meduzzen-internship" folder run "docker build -t image_name ." (it will build image)
-In "Meduzzen-internship" folder run "docker run -d --name container_name -p APP_HOST:port_to_use:APP_PORT/tcp image_name" i.e "docker run -d --name mycontainer -p 127.0.0.1:8000:8000/tcp myimage"
(it will run a container and tests automatically)

To see terminal run "docker logs container_name"