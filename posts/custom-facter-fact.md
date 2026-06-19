---
title: How to make a custom Facter fact that’s also a script
slug: custom-facter-fact
date: 2011-10-13 12:00:00 UTC-07:00
tags: puppet
category: 
link: 
description: 
type: text
---

_(originally from <https://web.archive.org/web/20150422203246/http://ajcsystems.com/blog/page/2/>)_

At $work, we use Puppet to manage some of our servers, and part of that involves [writing custom facts](https://web.archive.org/web/20150422203246/http://projects.puppetlabs.com/projects/1/wiki/Adding_Facts) for Facter, Puppet’s tool for gathering node information. (If you’re not familiar, here’s a [quick description of Facter](https://web.archive.org/web/20150422203246/http://puppetlabs.com/puppet/related-projects/facter/).)

These custom facts can use information present on a given host, such as hostname or IP address, to make their determination. However, we’ve also found it useful to be able to ask a custom fact, “what answer would you give if you were run on a given host?”

The answer:

<script src="https://gist.github.com/handyman5/1283770.js"></script>

This is a simple Facter fact that takes a hostname and determines which Ganglia grid to place it in. When run as a part of Facter, it will operate as a fact:

> $ facter 
> architecture => x86_64
> [...]
> grid => build
> hardwareisa => x86_64
> hardwaremodel => x86_64
> [...]

But when called as a standalone script, it will operate as though it were running on that host:

> $ ./grid.rb build01
> build

Building facts like this will let you keep any custom logic you might have in one place, but reuse it in different contexts. Code reuse FTW.

P.S.- If you’re thinking about posting a comment to the effect that Facter can be run with one or more arguments of facts to output:

> $ facter architecture
> x86_64

you’re missing the point. This technique allows you to run Facter facts on a _different_ host than the target and still get the benefit of the logic embedded in the fact.
