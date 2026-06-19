---
title: Dr. jQuery-Cycle, or how I learned to stop using Keynote and love HTML
slug: dr-jquery-cycle
date: 2012-10-08 12:00:00 UTC-07:00
tags: javascript, code
category: 
link: 
description: 
type: text
atUri: "at://did:plc:yxhvd47p53gmb5zfiktqq3og/site.standard.document/3momrx6scyr2p"
---

_(originally from <https://web.archive.org/web/20150422001009/http://ajcsystems.com/blog/blog/2012/10/08/dr-jquery-cycle-or-how-i-learned-to-stop-using-keynote-and-love-html/>)_

We have a number of fancy dashboards displaying on TVs here at $work, and some of them are implemented with Keynote to get the endless-cycling effect. This is lame because Keynote is very hard to use for this purpose (precise grid positioning, versioned changes, lots of other stuff).

<!-- TEASER_END -->

I recently stumbled across the [jQuery Cycle plugin](http://jquery.malsup.com/cycle/) while trying to improve this situation, and it rocks. It does everything we need for this purpose and then some.

The one adaptation I needed to make was to implement a few keyboard commands, to pause/resume the slideshow and go to the next or previous slide. Behold:

``` javascript
jQuery(document).ready(function() {
  jQuery('.slideshow').cycle({ fx: 'fade'});
  jQuery(document).keydown(function(e) {
    if(e.which == 37) {
      jQuery('.slideshow').cycle('prev')
    } else if(e.which == 39) {
      jQuery('.slideshow').cycle('next')
    } else if(e.which == 32) {
      jQuery('.slideshow').cycle('toggle');
      return false;
    }
  });
});
```

Also useful was the [jQuery keycode cheatsheet](http://mikemurko.com/general/jquery-keycode-cheatsheet/).
