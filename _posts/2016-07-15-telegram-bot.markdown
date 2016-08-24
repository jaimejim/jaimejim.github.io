---
title: "Simple Telegram Bot for Task Management"
layout: post
date: 2016-07-15 18:14
tag:
- JS
- bot
- Telegram
blog: true
star: true
---

I would claim to be a pretty organized person, mostly because I have to if I don't want to go crazy tracking the work happening on various standard orgs, internal projects and mailing lists.

As I only have ten fingers I am sadly not capable of using [orgmode](http://orgmode.org) efficiently. If you are one of the *chosen ones* that can exclusively use Emacs I strongly recommend it. Instead, I use **[PlainTasks](https://github.com/aziz/PlainTasks)** (first on Sublime, now on Atom), kudos to [@aziz](https://github.com/aziz) for doing them BTW.

A fairly active IETF working Group has a relatively large number of items that need to be done, for example these are the [tasks for CoRE](http://jaimejim.github.io/temp/coretodo.txt). I aggregate them by draft/RFC, for example ETCH would be:

```
ETCH draft-ietf-core-etch:
Notes:
    Summary available
    http://jaimejim.github.io/temp/draft-ietf-core-etch
 ✔ [ETCH] [IETF96] Address comments (preconditions and use of iPTACH/PATCH)
 on mailing list before shepherd-writeup @due(16-07-25) @done(2016-08-15 11:06)
 ✔ [ETCH] [IETF96] shepherd-writeup (in progress in parallel)
 @due(16-07-18 15:28) @jaime @high @done(2016-08-15 11:06)
 ☐ [ETCH] Awaiting for authors to initiate expert review on the media types
 @due(2016-08-22 08:23)
 ☐ [ETCH] Awaiting for authors to confirm IPR @due(2016-08-22 08:23)
 ☐ [ETCH] IESG Submission of draft-ietf-core-etch @due(16-07-25 15:25) delayed
 to @due(16-08-20 15:25)
 ☐ [ETCH] IETFLC @iesg
 ☐ [ETCH] AD go ahead if IETFLC OK. @iesg
 ☐ [ETCH] IESG Ballot (ADs read it). @iesg  
```

On my computer I have a cron job that alerts me when a task is happening, but to sync among several people is not that easy. I quickly noticed that several of us were chatting through [Telegram](https://telegram.org/blog/bot-revolution), thus I thought that maybe a bot that sends us reminders could be helpful.

Telegram has enabled an API for developers to create bots, quickly several implementations popped out, in particular I found [Telegram Node Bot](https://github.com/Naltox/telegram-node-bot) pretty useful.
I won't repeat what the Github README says, so just go ahead and check it out.

As it turns out, it was very quick and simple to put together a bot to fetch the task list, find the the due action points, and just send them over Telegram. Beforehand I would like to apologize for the ~~shitty~~ *suboptimal* code, it works but it isn't pretty.

``` js
// Belvedere Bot 0.1
// @jaimejim http://jaimejim.github.io
var http = require('http')
var fs = require('fs')
var tg = require('telegram-node-bot')('insert-your-token-here')
var ct = new Date()

function gettas (callback) {
  http.request('http://<url_of_tasks>.todo', function (error, response, body) {
    if (!error && response.statusCode == 200) {
      var i = body.indexOf('@due')
      var out = ''
      var counter = 0
      var txt = ''
      while (i !== -1){
        var dt = getdate(body.substring(i + 5, i + 13))
        if ((dt.getYear() == ct.getYear()) && (dt.getMonth() == ct.getMonth())
        && (dt.getDay() == ct.getDay())) {
          txt = body.substring(0, i)
          out = out + '\n' + body.substring(txt.lastIndexOf(' ☐ '), i)
        } else {
        }
        i = body.indexOf('@due', i + 1)
      }
      console.log(out)
      callback(out)
    }
  })
}

gettask(function (data) {
  tg.router.when(['list'], 'ListController').otherwise('OtherwiseController')

  tg.controller('ListController', ($) => {
    tg.for('list', () => {

      $.sendMessage('These are your tasks for today:\n')
      $.sendMessage(data)
    })
  })

  tg.controller('OtherwiseController', ($) => {
    $.sendMessage('Sorry, what? \n')
  })

  tg.controller(($) => {
    if (dt.getYear() == ct.getYear()) {
      $.sendMessage('Time is ' + dt.getYear() + ' \n')
    }
  })
})

function getdate (st) {
  var dpattern = /(\d{4})\-(\d{2})\-(\d{2})/
  return new Date('20' + st.replace(dpattern, '$1-$2-$3'))
}
```

On the server side you could install [forever](https://github.com/foreverjs/forever) in case the bot crashes (which it did a couple of times for me):

``` bash
$jaime:~$ [sudo] npm install forever -g
$jaime:~$ forever start belvederebot.js
info:    Forever started process(es):
data:        uid  command         script          forever pid  id logfile                       uptime       
data:    [0] KtcN /usr/bin/nodejs belvederebot.js 4987    1019    
/home/jaime/.forever/KtcN.log 0:0:24:4.495
$jaime:~$ forever list
```

And that's all, this is how the bot looks like once running.
![Telegram Bot running]({{ site.url }}/assets/images/telegram_bot.png)
