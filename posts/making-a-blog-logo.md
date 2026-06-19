---
title: Making a Blog Logo
slug: making-a-blog-logo
date: 2024-07-11 10:30:27 UTC-07:00
tags: meta
category: 
link: 
description: 
type: text
atUri: "at://did:plc:yxhvd47p53gmb5zfiktqq3og/site.standard.document/3momrx4wwky2b"
---

To commemorate the new blog, I wanted to have a cool logo up in the corner. Since one of my current interests is generative AI, I thought I'd try using it to generate myself a logo. This post explains the process.

<!-- TEASER_END -->

## Getting Started

I already have the kit set up to run a large language model (LLM) in my home network. However, I've only ever used it for text generation before; I had no idea how to make it generate images.

I started with [Koboldcpp](https://github.com/LostRuins/koboldcpp), since I recalled that it was able to generate images as of a recent release. This wiki page explained [how to generate images with Koboldcpp](https://github.com/LostRuins/koboldcpp/wiki#can-i-generate-images-with-koboldcpp), and provided some example models to try. I poked at a couple of different ones before I tried the `Anything v3` model linked from that page. I ran the model with `--sdmodel &lt;path-to-anything&gt;`.

I admit, it took me a while to figure out how to even start trying to generate an image! I had to poke around in the text generation UI ("kobold lite") for a while before I realized that the image generation UI was an entirely different path: `&lt;IP&gt;:5001/sdui`.

## Prompting the Model

Once I had that running, I had to figure out how to actually prompt the model and get images out. A useful technique I ran across is [to use an empty white square](https://www.reddit.com/r/StableDiffusion/comments/x8vxui/i_discovered_an_easy_way_to_force_a_line_drawing/) with the `img2img` option to force the model to generate something that's mostly white, which is what I wanted for my logo. (I used the `convert` command [to generate said image](https://superuser.com/a/294948).)

I wound up with:

![logo](/images/logo.png)

The settings I used were:

* Prompt: `sparse black line drawing vector logo icon, stylized male human head filled with gears and circuits, profile, no text, no fill, line art, adobe illustrator, vector art`
* Negative prompt: `color, blurry, complex, intricate, neon, mecha, robotech, spiky, anime`
* Sampler: `Euler a`
* Steps: 40
* Guidance: 15

## Takeaways

This took a lot of work! Both to get the image generation pipeline working in the first place, and also to tweak the parameters and try to get to an image I liked. Even this one isn't exactly where I'd want it, but I think it's about as good as it's going to get for my current level of setting-up-the-pipeline and prompting skills, so I'm setting it down for now. I did appreciate the ability to translate the rough image I had in mind to something tangible; I have no drawing talent whatsoever so it was nice to have borrowed access to this skill.
