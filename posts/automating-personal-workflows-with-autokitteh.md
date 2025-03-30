<!--
.. title: Automating Personal Workflows with Autokitteh
.. slug: automating-personal-workflows-with-autokitteh
.. date: 2025-03-30 00:14:16 UTC-07:00
.. tags: kubernetes, automation
.. category:
.. link:
.. description:
.. type: text
-->

I wanted to build some workflow automation for various tasks I do often (like coming across a link that I want to share with my work after writing a little introduction message). I knew it would need to be flexible and customizable, so I wanted something I could run myself and control every aspect of.

After doing lots of investigation (primarily via the [awesome-workflow-engines list](https://github.com/meirwah/awesome-workflow-engines)), I settled on [Autokitteh](https://autokitteh.com/). It has all the features I care about:

* Self-hosted (no SaaS)
* Workflows can be defined and managed in plain text (so they can be versioned)
   * This eliminated most of the IFTTT and Zapier clones like [Automatisch](https://automatisch.io/)
* Workflows can be written in Python
   * This eliminated [Huginn](https://github.com/huginn/huginn)
* Pre-created integrations for services I use (for this purpose, mainly Slack and Todoist)
   * This eliminated [Node-RED](https://nodered.org/) and [Dagu](https://github.com/dagu-org/dagu)
* No "open-core" feature paywalls
   * This eliminated [n8n](https://n8n.io/), [Windmill.dev](https://www.windmill.dev/), and [Activepieces](https://www.activepieces.com/)

The thing I liked most about it is how the workflow definitions let you set up integrations and provide them to the workflow code, so you can use the integrations in any way you can imagine instead of just the ways that come predefined. It also allows you to trivially mix and match integrations, so I can (for instance) take a Slack message and create a Todoist task from it just by smushing the two APIs together.

Read on to learn how I set everything up.

<!-- TEASER_END -->

## Server Installation

Autokitteh has [several ways to run the backend service](https://docs.autokitteh.com/get_started/start_server/). I was able to experiment a bit with "Dev" mode running on my laptop, but for running unattended workflows I wanted something slightly more sturdy.

I took [the docker-compose configuration](https://github.com/autokitteh/autokitteh/blob/main/compose.yaml) Autokitteh provides and [whipped up a quick Helm chart](https://github.com/handyman5/autokitteh-chart) to run it. I also had to [create and publish a Docker image](https://hub.docker.com/r/comptona/autokitteh-image) so the Helm chart had something to pull (since the docker-compose file builds the image from a Dockerfile live).

Once I had that Helm chart created, I added it to my ArgoCD setup for my homelab and it was off to the races!

## Client Setup

I downloaded [the `ak` binary from its repo](https://github.com/autokitteh/autokitteh/releases) and configured it to point to my server:

``` shell
ak config set http.service_url https://<my-server-hostname>
```

Then I was able to use `ak deploy --manifest <example>` to deploy [the example projects](https://github.com/autokitteh/kittehub) that Autokitteh provides. I started with [the Slack project](https://github.com/autokitteh/kittehub/tree/main/samples/slack) just to get a feel for how it would work. The [Slack integration setup docs](https://docs.autokitteh.com/integrations/slack/) were straightforward and easy to follow, and in no time I had a workflow up and running that could handle slash commands and mentions!

_(Note that I had to add the Slack environment variables to the backend service instead of specifying them in the config file; this is why the Helm chart I created supports a `envFrom` parameter in its values file.)_

I also created a Makefile to help me remember how to deploy my changes:

``` Makefile
AK=~/.local/bin/ak

# example: `make deploy-example-slack`

deploy-%:
        $(AK) deploy --manifest $*/autokitteh.yaml
```

## Workflow Ideas

I have so many workflows I want to build, I can't wait to get started:

* Add a new link as a bookmark (in case I want to reference it later)
* Add a new link to read later
  * This would leverage another service I wrote that downloads the plain text of the article, creates a summary, and generates a RSS feed with that summary and an estimate of the reading time that I subscribe to in [Feedly](https://feedly.com/)
* Add a new podcast episode I'm not subscribed to
  * Go grab the MP3 with [yt-dlp](https://github.com/yt-dlp/yt-dlp) and put it in a [Syncthing](https://syncthing.net/) directory my podcast app is watching

And I'm sure I'll think of more as time goes on. I'm really excited to work with this tool and I look forward to figuring out everything it can do.
