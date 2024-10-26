# LAB 5 Full Description
### To build and run
>**docker compose build --no-cache && docker compose up**

I don't why in my machine [ubuntu 22.04], docker-compose version: 2.29.2
> docker-compose up --build --no-cache

> docker-compose up build --no-cache

commands don't run likee this.
## Base Image

In lab file we did a simple trick. Here:
> ./main [folder]

Contains the main files of this application like you can say this one the root image to be used. Instead of replicating each files in each service we called this base image and wrote new codes as needed.
# docker-compose.yml
- Each service will use the base image so we had to define the **image** and **container** name for the base image. Later each service will we defined the **image** name now this is not strictly necessary but for better caching system we can use that. If we define that we can run docker compose without the build command and it will use and existing **main_service** image if available. <font color="cyan">But in our case defining the **image** is important becuase our **calc**, **string**, **last** folder has no **Dockerfile** inside. So, if you run docker compose it will throw an error saying that base image is missing.</font>
- Each service uses the **common network** so, we needed to define the network in docker.As our applications will **communicate** with each other we also defined an **internal network** and assigned it to every app.
- **Ports** are defined for each application access.
- **Redis** configuration has been defined in the base image as but also in other services. This operation is not necessary if you stick to the base image configuration. If, there is a chance for different services to use different **redis** or **database** services then you should define it in each services. We did it here just for learning purpose.
- 
## Service Images
We will get to know about the service images later in the docker-compose.yml file. Only special cases are discussed here.
### Redis Service
Check the docker compose
### Calc Service
Check the docker compose
### String Service
Check the docker compose
### Last Service
Check the docker compose

# <font color="cyan">Errors I faced</font>
1. <font color="red">Base image not found</font> <br>
    > This is why we used image tag for the base image and tagged the base to each service images. **image:main_service**
2. <font color="red">Remove the port and host from all python files</font> <br>
    > As we defined the host and port in the Dockerfile it is not necessary to define them in the main file, it will create redundancy issues.
3. <font color="red">Changes in code not displayed in browser</font> <br>
    > Pur the settings in debug mode. It is flask issue.
4. <font color="red">Calling a service from another one</font> <br>
    > Our last service was running on 127.0.0.1:8002. But if we internally call one service from another, external **ips** and **ports** will not work in this case. So we had to rename our api call to this: **http://last_service:5000/store**. Yes, you have to define the host port not the external one. The rest will be taken care of by docker networks.
5. <font color="red">**redis** and **requests** library</font> <br>
    > **redis** and **requests** should be installed in **requirements.txt** otherwise the libraries cannot be used, because they does not come from flask.


