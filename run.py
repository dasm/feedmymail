# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import smtplib
import feedparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email(object):
    messages = []

    def __init__(self, sender, recipient):
        """Create Email instance with Sender and Recipient."""
        self.sender = sender
        self.recipient = recipient

    def _build_headers(self):
        """Build message headers with Sender and Recipient."""
        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender
        msg['To'] = self.recipient
        return msg

    def add_message(self, subject='', html_message=''):
        msg = self._build_headers()
        msg['Subject'] = subject

        txt_message = re.sub('<[^<]+?>', '', html_message)

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(txt_message.encode('utf-8'), 'plain')
        part2 = MIMEText(html_message.encode('utf-8'), 'html')
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this
        # case the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        self.messages.append(msg)

    def send(self):
        # Send the message via local SMTP server.
        s = smtplib.SMTP('localhost')
        # sendmail function takes 3 arguments: sender's address, recipient's
        # address and message to send - here it is sent as one string.
        for message in self.messages:
            s.sendmail(self.sender, self.recipient, message.as_string())
        s.quit()


class RSSReader(object):
    def add_feed(self, feed_url):
        pass

    def remove_feed(self, feed_url):
        pass

    def process_feed(self, url=''):
        feed = self._read_feed(url)
        content = []
        for post in feed.entries:
            try:
                summary = post.summary_detail.value
            except AttributeError:
                summary = post.summary
            link = post.link
            title = post.title
            content.append((link, title, summary))

        return {'title': feed.feed.title, 'content': content}

    def _read_feed(self, url):
        return feedparser.parse(url)


class ContentBuilder(object):
    with open('app/templates/header.html') as header:
        template_header = header.read()

    with open('app/templates/content.html') as content:
        template_content = content.read()

    with open('app/templates/email.html') as email:
        template_email = email.read()

    def __init__(self, content):
        self.content = content

    def _build_menu(self):
        menus = []
        template = '<a href="#item_{number}">{title}</a>'

        for i, element in enumerate(self.content):
            _url, title, _detail = element
            menus.append(template.format(number=i, title=title))

        self.menu = '<br>'.join(menus)

    def _build_details(self):
        details = []
        template = '''
<h2><a name="item_{number}" class="content" href="{url}">{title}</a></h2>
<div class="content">{detail}</div>'''

        for i, element in enumerate(self.content):
            url, title, detail = element
            details.append(template.format(number=i, url=url, title=title,
                           detail=detail))

        self.details = '<hr>'.join(details)

    def build_html(self):
        self._build_menu()
        self._build_details()
        template = '''
<html>
<head></head>
<body>
    <div style="border:1px solid #000; padding: 10px;">{menu}</div>
    <hr>
    <div style="border:1px solid #000; padding: 10px;">{details}</div>
</body>
</html>
'''
        return template.format(menu=self.menu, details=self.details)


if __name__ == '__main__':
    feeds = (
        'http://www.jarzebski.pl/feed.xml',
        'http://agatainthecity.pl/rss',
        'http://feeds.feedburner.com/AgileCoaching',
        'http://www.agile247.pl/feed/',
        'http://feeds.feedburner.com/androidspin',
        'http://feeds.feedburner.com/blogspot/etVI',
        'http://rss.badsector.pl/BadsectorPL',
        'http://blog.testowka.pl/feed/',
        'http://alexba.eu/feed/',
        'http://boli.blog.pl/index.rss',
        'http://bronikowski.com/feed',
        'http://www.cdaction.pl/rss_newsy.xml',
        'http://feeds.feedburner.com/codinghorror/',
        'http://www.commitstrip.com/en/feed/',
        'http://www.cad-comic.com/rss/rss.xml',
        'http://feeds.dilbert.com/DilbertDailyStrip',
        'http://www.thedoghousediaries.com/?feed=rss2',
        'http://blog.dragonsector.pl/feeds/posts/default',
        'http://dspodcast.pl/feed/',
        'http://www.duelinganalogs.com/rss.php',
        'http://dwagrosze.com/feed',
        'http://erocomica.blogspot.com/feeds/posts/default',
        'http://www.fantasmagieria.net/?feed=podcast',
        'http://feeds.feedburner.com/uclick/calvinandhobbes',
        'http://www.blastwave-comic.com/rss/blastwave.xml',
        'http://gynvael.coldwind.pl/rss_pl.php',
        'http://www.glosywmojejglowie.pl/feed/',
        'http://feeds.feedburner.com/JakOszczedzacPieniadze',
        'http://www.joelonsoftware.com/rss.xml',
        'http://kijwdupie.tumblr.com/rss',
        'http://feeds.feedburner.com/kulturawplot',
        'http://kokoart.net/nowa2/?feed=rss2',
        'http://feeds.gawker.com/lifehacker/vip.xml',
        'http://feeds.feedburner.com/like-a-geek?format=xml',
        'http://lukasz.langa.pl/feed/recent/rss-pl.xml',
        'http://feeds.feedburner.com/maciejaniserowicz',
        'http://volt9.tanihost.com/?feed=rss2',
        'http://alexbarszczewski.natemat.pl/rss/',
        'http://feeds.feedburner.com/nerfnow/full',
        'http://feeds.feedburner.com/niebezpiecznik',
        'http://oglaf.com/feeds/rss/',
        'http://feeds.feedburner.com/omaketheater',
        'http://feeds.feedburner.com/Opium-org-pl',
        'http://feeds.feedburner.com/Optipess',
        'http://planet.python.org/rss20.xml',
        'http://www.operator.enea.pl/rss/rss_unpl_7.xml',
        'http://poczytajmimako.blogspot.com/feeds/posts/default?alt=rss',
        'http://www.gloswielkopolski.pl/rss/gloswielkopolski.xml',
        'http://produktywnie.pl/feed/',
        'http://www.questionablecontent.net/QCRSS.xml',
        'http://www.qfant.pl/feed/',
        'http://feeds.feedburner.com/zeefeed',
        'http://feeds.feedburner.com/scotthyoung/HAHx',
        'http://henrik.nyh.se/scrapers/sinfest.rss',
        'http://springfieldpunx.blogspot.com/feeds/posts/default',
        'http://feeds.feedburner.com/steamgifts',
        'http://samcik.blox.pl/rss2',
        'http://syndication.thedailywtf.com/TheDailyWtf',
        'http://www.fallout3.net/rss.xml',
        'http://www.epoznan.pl/rss.php',
        'http://feeds.feedburner.com/wulffmorgenthaler',
        'http://xion.org.pl/feed/',
        'http://xkcd.com/rss.xml',
        'http://www.youneedabudget.com/blog/feed/',
        'http://zenhabits.net/feed/',
        'http://zenpencils.com/feed/',
        'http://znadplanszy.pl/full-feed/posts/',
        'http://www.zuchrysuje.pl/feed/',
        'http://lowcygier.pl/feed/',
        'http://rss.swiatczytnikow.pl/SwiatCzytnikow',
    )

    for feed in feeds:
        print(feed)
        rss = RSSReader()
        content = rss.process_feed(feed)

        builder = ContentBuilder(content['content'])
        message = builder.build_html()

        sender = 'john.doe@gmail.com'
        email = Email('FeedMyMail', sender)
        email.add_message(content['title'], message)
        email.send()
