---
title: "Simple telegram bot for task management"
layout: post
date: 2016-06-10 09:00
tag:
- JS
- bot
- Telegram
blog: true
star: true
---

CoRE WG tasks
http://jaimejim.github.io/temp/coretodo.txt

![Telegram Bot running]({{ site.url }}/assets/images/telegram_bot.png)


Plaintasks

Orgmode
https://github.com/aziz/PlainTasks
(kudos to [@aziz](https://github.com/aziz) for doing them)

Beforehand I would like to apologize for the shitty code, it works but it isn't pretty.

``` js
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
        if ((dt.getYear() == ct.getYear()) && (dt.getMonth() == ct.getMonth()) && (dt.getDay() == ct.getDay())) {
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


sudo npm -g install forever
   69  npm -g install forever
   70  sudo npm -g install forever
   71  forever start belvederebot.js
   72  ps
   73  ps -e
   74  man forever
   75  forever list
   76  cat /home/jaime/.forever/9VUC.log
   77  forever belvederebot.js stop
   78  list
   79  forever list
   80  forever belvederebot.js stop
   81  forever stop belvederebot.js
   82  forever list
   83  forever options
   84  forever start belvederebot.js
   85  forever stop belvederebot.js
   86  forever start belvederebot.js
