# RSS Feed Display

A simple application to display RSS Feeds.

## Building The Docker Container

```
docker build -t rss -f Dockerfile .
```

## Running with Docker Locally

`RSS Feed Display` expects a file in the same directory named `feeds.txt`.  
This file should contain a list of RSS feeds, one per line.

You can run it locally (after filling out the `feeds.txt` file and building) with this command:
```
 docker run -p 5000:5000 -v .\feeds.txt:/app/feeds.txt rss  
```

The application will be available at http://localhost:5000/

## Deploying to Kubernetes

I have a simple Kubernetes deployment located in `kubernetes\deployment.yaml`.
Fill in the RSS feeds and your image.

Change the settings as needed (for now it's creating an RSS namespace and deploying there), and then add an ingress.

> [!WARNING]
> 
> I haven't made any of this production ready, so do not deploy it anywhere publicly accessible