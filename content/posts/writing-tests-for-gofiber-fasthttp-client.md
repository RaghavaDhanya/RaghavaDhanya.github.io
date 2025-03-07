---
title: "Writing Tests for Gofiber Fasthttp Client"
date: 2025-01-23T10:20:44+05:30
draft: true
---

API clients or SDKs are common for providing your users with a way to interact with your service. In Go, we can use Fasthttp client to make requests to a server. Fasthttp client is a high-performance HTTP client that is used by Gofiber. Writing tests for these clients is important to ensure that the client is working as expected.

Let's look at a simple application that we can use as an example for writing tests for Gofiber Fasthttp client. Let's say this server provides two routes: ping and fetch data and it returns error 401 if the id is not provided.
you can test it using curl.

```sh
go run main.go
```

```sh
curl http://localhost:3000/ping
```

```sh
curl http://localhost:3000/fetch-data?id=1
```

Now let's write a simple client library that can be used to interact with this server. Internally, this client will use Fasthttp client to make requests to the server.

```go
package client

import (
    "github.com/valyala/fasthttp"
)

type Client struct {
    url string
}

func NewClient(url string) *Client {
    return &Client{
        url: url,
    }
}

func (c *Client) Ping() (string, error) {
    req := fasthttp.AcquireRequest()
    defer fasthttp.ReleaseRequest(req)

    req.SetRequestURI(c.url + "/ping")

    resp := fasthttp.AcquireResponse()
    defer fasthttp.ReleaseResponse(resp)

    if err := fasthttp.Do(req, resp); err != nil {
        return "", err
    }

    if resp.StatusCode() != fasthttp.StatusOK {
        return "", fmt.Errorf("unexpected status code: %d", resp.StatusCode())
    }

    return string(resp.Body()), nil
}

func (c *Client) FetchData(id string) (string, error) {
    req := fasthttp.AcquireRequest()
    defer fasthttp.ReleaseRequest(req)

    req.SetRequestURI(c.url + "/fetch-data?id=" + id)

    resp := fasthttp.AcquireResponse()
    defer fasthttp.ReleaseResponse(resp)

    if err := fasthttp.Do(req, resp); err != nil {
        return "", err
    }

    if resp.StatusCode() != fasthttp.StatusOK {
        return "", fmt.Errorf("unexpected status code: %d", resp.StatusCode())
    }

    return string(resp.Body()), nil
}
```

Now let's write tests for this client library. Basic idea for these kinds of tests is to create a mock server that will respond to requests made by the client library. We can use httptest package to create a mock server. Easiest one I've found is fasthttputil.NewInmemoryListener().

```go
package client

import (
    "github.com/valyala/fasthttp"
    "github.com/valyala/fasthttp/fasthttputil"
    "testing"
    "encoding/json"
)

func TestClient_Ping(t *testing.T) {
    ln := fasthttputil.NewInmemoryListener()
    defer ln.Close()

    go func() {
        if err := fasthttp.Serve(ln, func(ctx *fasthttp.RequestCtx) {
            ctx.SetBodyString("pong")
        }); err != nil {
            t.Fatal(err)
        }
    }()

    client := NewClient("http://localhost")
    client.url = "http://" + ln.Addr().String()

    resp, err := client.Ping()
    if err != nil {
        t.Fatal(err)
    }

    if resp != "pong" {
        t.Fatalf("expected pong, got %s", resp)
    }

}

func TestClient_PingError(t *testing.T) {
    ln := fasthttputil.NewInmemoryListener()
    defer ln.Close()

    go func() {
        if err := fasthttp.Serve(ln, func(ctx *fasthttp.RequestCtx) {
            ctx.SetStatusCode(fasthttp.StatusBadRequest)
            ctx.SetBodyString("bad request")
        }); err != nil {
            t.Fatal(err)
        }
    }()

    client := NewClient("http://localhost")
    client.url = "http://" + ln.Addr().String()

    _, err := client.Ping()
    if err == nil {
        t.Fatal("expected error, got nil")
    }

    if err.Error() != "unexpected status code: 400" {
        t.Fatalf("expected unexpected status code: 400, got %s", err.Error())
    }

}

func TestClient_FetchData(t *testing.T) {
    ln := fasthttputil.NewInmemoryListener()
    defer ln.Close()

    go func() {
        if err := fasthttp.Serve(ln, func(ctx *fasthttp.RequestCtx) {
            if string(ctx.QueryArgs().Peek("id")) == "" {
                ctx.SetStatusCode(fasthttp.StatusBadRequest)
                ctx.SetBodyString("id is required")
                return
            }
            ctx.SetBodyString(`{"data":"some data"}`)
        }); err != nil {
            t.Fatal(err)
        }
    }()

    client := NewClient("http://localhost")
    client.url = "http://" + ln.Addr().String()

    resp, err := client.FetchData("1")
    if err != nil {
        t.Fatal(err)
    }

    var data map[string]string
    if err := json.Unmarshal([]byte(resp), &data); err != nil {
        t.Fatal(err)
    }

    if data["data"] != "some data" {
        t.Fatalf("expected some data, got %s", data["data"])
    }
}
```

