---
title: Adventures in One-Liners
date: 2013-08-22
author: Adam Compton
tags: [linux]
atUri: "at://did:plc:yxhvd47p53gmb5zfiktqq3og/site.standard.document/3mohnjcfo4t2m"
---

_(originally from <https://web.archive.org/web/20150421214026/http://ajcsystems.com/blog/blog/2013/08/22/adventures-in-one-liners/>)_

I wrote this one-liner today, and that it exists makes me sad.

``` shell
rrdtool update $tmpfile $(curl "http://127.0.0.1:4242/api/query?start=$(($(date +'%s')+$start))&m=sum:$metric\{cluster=$cluster,hostname=$hostname\}" | python -c "import sys, json; j=json.loads(sys.stdin.read())[0]['dps']; sys.stdout.write(' '.join(['%d:%s' % (int(x), j[x]) for x in sorted(j.keys())]))")
```

That it actually works just downright terrifies me.
