---
title: "A Tale of a Suicidal Container"
date: 2024-02-21T12:25:03+05:30
# draft: true
tags: ["deep-learning", "mlops", "python", "ml", "ai"]
categories:
    - projects
    - glance-inmobi
---
One fine day as I sat down to optimize the size of a Docker image. Like many times before, I opted for [distroless](https://github.com/GoogleContainerTools/distroless) images as my base, a choice I had made countless times before without a hitch.

Distroless images, for the uninitiated, are peek minimalism, containing only the essential libraries and binaries required to run the application. Not only do they trim the fat off the image size, but they also mitigate the risk of [CVEs](https://www.cve.org/About/Overview) lurking within

Little did I know, what appeared to be a simple task soon spiraled into hours of troubleshooting and head-scratching.

I made a seemingly innocuous change to the Dockerfile.

From:
```dockerfile
FROM golang:1.20
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o /app
ENTRYPOINT ./app
```
to :
```dockerfile
FROM golang:1.20 AS build
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o /app

FROM gcr.io/distroless/base
COPY --from=build /app /
ENTRYPOINT ["/app"]
```
With the changes made, I deployed to the development environment. To my surprise, the pods failed to spin up, with containers exiting immediately and logging `exit status 1`.

Interesting! The code remained untouched; it had to be the change in the base image. I swapped `gcr.io/distroless/base` for `golang:1.20` in the Dockerfile in the second stage. But the issue persisted. Oddly, the app ran fine outside the containers and with the earlier Dockerfile. But the newer Dockerfile, with or without distroless base, was not working.

Attempting to gain more insight, I toggled debug mode to true, hoping for additional logs.  Wait what? It works. Yet, the mystery deepened as the same Dockerfile, with the distroless base, functioned seamlessly only in debug mode. Debug mode merely adjusts the log level and operates with a single worker, effectively disabling [preforking](https://www.oreilly.com/library/view/web-performance-tuning/1565923790/apbs08.html).

The issue likely lies with the preforking mechanism in the `gofiber` library which the app uses. Upon inspecting the codebase, I [stumbled upon](https://github.com/gofiber/fiber/blob/5e30112d08b1a76f38f838a175988a3712846bd7/prefork.go#L157-L161) a familiar piece of code:
```go
...
	for range time.NewTicker(watchInterval).C {
		if os.Getppid() == 1 {
			os.Exit(1) //nolint:revive // Calling os.Exit is fine here in the prefork
		}
	}
...
```
Hey, I know this.
![I know this gif](/images/A-tale-of-suicidal-container/I-know-this.gif)
This snippet essentially checks if the parent process is still alive. If not, it exits. Such behavior is common in preforking servers. The parent process listens to the port and forks children to handle requests. If the parent process dies, the children are useless. So, they exit. But how do they know if the parent died? They check if the parent process id is 1. In Linux, the parent process id 1 is `init` process. Any orphaned process is adopted by `init` process.

The culprit? The line `ENTRYPOINT ["/app"]` in the Dockerfile. Docker assigns PID 1 to the entrypoint process, this unwittingly condemned my application to an existential crisis. With no parent process to claim it, the app chose the path of least resistance: to commit suicide. Effectively it kills itself because it thinks it's an orphan.

There's a significant distinction between `ENTRYPOINT ./app` and `ENTRYPOINT ["/app"]` in Docker. The former treats `./app` as a string executed by the shell, making the app a child of the shell. The latter, however, directly executes `["/app"]`, leading the app to assume PID 1.

Switching back to `ENTRYPOINT ./app` wasn't an option due to distroless' lack of a shell. Enter [`tini`](https://github.com/krallin/tini), a lightweight init system designed to solve precisely this problem.  While I've encountered `tini` in Dockerfiles before, I never truly grasped its necessity until now. It serves as dummy processes to avoid the PID 1 problem.

Another aspect I previously overlooked was the distinction between `CMD` and `ENTRYPOINT`. `CMD` executes the command within `ENTRYPOINT`.
```dockerfile
FROM golang:1.20 AS build
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o /app
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

FROM gcr.io/distroless/base
COPY --from=build /app /
ENTRYPOINT ["/tini"]
CMD ["/app"]
```
This is essentially the same as `ENTRYPOINT ["/tini", "/app"]`.

