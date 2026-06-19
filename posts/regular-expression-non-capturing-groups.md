---
title: Regular Expression Non-Capturing Groups (or, what’s "(?:" mean?)
slug: regular-expression-non-capturing-groups
date: 2012-10-10 12:00:00 UTC-07:00
tags: python, code, til
category: 
link: 
description: 
type: text
atUri: "at://did:plc:yxhvd47p53gmb5zfiktqq3og/site.standard.document/3momrx6pxpw2m"
---

_(originally from <https://web.archive.org/web/20150422001421/http://ajcsystems.com/blog/blog/2012/10/10/regular-expression-non-capturing-groups-or-whats-mean/>)_

When I was working recently on changing [poodledo](https://github.com/handyman5/poodledo)‘s parser from using a lexer to using regular expressions, I found myself implementing some crazy logic to try and ignore the results from matched groups whose matches I didn’t actually want (since I was using parentheses for their “pick one of these two alternatives” function instead of their “pull out this specific chunk as a match” function).

For example, take the string “task title @context name #due date”. Starting with the at-sign, I want to match all words until some other symbol is reached; or, to avoid confusing the parser, match everything following the at-sign and between two square brackets. Here’s the regex I came up with:

``` python
(^|\W)@([\b ]?(([\w\"\'.@]+ )*[\w\"\'.@]+)[\b]??|[\b(.+?)\b])
```

Using this regex, though, gave me a lot of extraneous matching groups:

``` python
>>> q = r'(^|\W)@([\b ]?(([\w\"\'.@]+ )*[\w\"\'.@]+)[\b]??|[\b(.+?)\b])'
>>> task = 'task title @context name #due date'
>>> re.findall(q, task)
[(' ', 'context name', 'context name', 'context ', '')]
```

How do I determine programmatically which of these groups is the one I want?

Digging around in the Python regex documentation, I found a section about [non-capturing groups](https://web.archive.org/web/20150422001421/http://docs.python.org/howto/regex.html#non-capturing-and-named-groups), which seemed like it would save me a significant amount of sanity. Apparently, Perl-5-compatible regular expression parsers often implement a regex extension syntax by following an open parenthesis with a question mark, and then some other symbols that indicate which extension is in use. In this specific case, “(?:” indicates a group whose matches shouldn’t be captured in the output list. Eureka!

``` python
>>> q = r'(?:^|\W)@(?:[\b ]?((?:[\w\"\'.@]+ )*[\w\"\'.@]+)[\b ]??|[\b(.+?)\b])'
>>> re.findall(q, task)
[('context name', '')]
```

Now the only logic I need is “Ignore matching groups which are empty”, my sanity is preserved, and all is well with the world.
