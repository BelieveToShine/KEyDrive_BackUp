from kit import *
from p_common import CR

DOCS_CF = ('How CloudFront delivers content', 'https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html')
DOCS_EXP = ('Managing how long content stays in the CloudFront cache', 'https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html')
DOCS_INV = ('Invalidating files in CloudFront', 'https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html')
DOCS_EC = ('Amazon ElastiCache documentation', 'https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html')
DOCS_STR = ('Caching strategies (ElastiCache)', 'https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html')
FOOT = 'Cloud services change often — caching products especially. This page teaches the ideas; for current product names, engines and limits, check the official AWS docs.'

def d_layers():
    d = Diagram('ce1', 640, 372, 'Four places a copy can live between a visitor and the database: the browser, the CloudFront edge, an ElastiCache cache and the database itself')
    rows = [
      ('🌐 Browser cache','files kept on the visitor\'s own device','cyan'),
      ('🌍 Edge cache (CloudFront)','a copy at an edge location near the visitor','emerald'),
      ('⚡ App cache (ElastiCache)','shared, in memory, between the app and the database','amber'),
      ('🗄️ Database or origin','the source of truth — the slowest place to ask','n'),
    ]
    for i,(t,s_,c) in enumerate(rows):
        y = 10 + i*96
        d.box(20, y, 600, 58, [(t,'t'),(s_,'s')], c)
        if i < 3:
            d.arrow([(320,y+58),(320,y+96)], 'n', label='miss: ask the next layer', at=(450,y+77))
    return d

def d_aside():
    d = Diagram('ce2', 640, 262, 'Lazy loading, also called cache-aside: the app checks the cache first, reads the database on a miss, then saves a copy in the cache')
    d.box(20, 40, 110, 150, [('📱 App','t'),('your code','s')], 'n')
    d.box(300, 30, 150, 80, [('⚡ Cache','t'),('ElastiCache','s')], 'amber')
    d.box(300, 150, 150, 80, [('🗄️ Database','t'),('source of truth','s')], 'violet')
    d.arrow([(130,66),(300,66)], 'amber', label='1 · check cache', at=(215,66))
    d.arrow([(130,98),(300,98)], 'amber', label='3 · save a copy', at=(215,98))
    d.arrow([(130,190),(300,190)], 'violet', label='2 · miss: read DB', at=(215,190))
    d.text(470, 58, 'Hit: the answer comes', anchor='start', size=9.5)
    d.text(470, 74, 'straight from the cache.', anchor='start', size=9.5)
    d.text(470, 170, 'Data changed? Write to the', anchor='start', size=9.5, weight=700)
    d.text(470, 186, 'database, then delete the', anchor='start', size=9.5, weight=700)
    d.text(470, 202, 'cached copy (or set a TTL).', anchor='start', size=9.5, weight=700)
    return d

def d_edge():
    d = Diagram('ce3', 640, 246, 'Visitors reach a nearby CloudFront edge location; only a cache miss travels on to the origin')
    d.box(10, 30, 110, 50, [('👤 Visitor A','t')], 'n')
    d.box(10, 150, 110, 50, [('👤 Visitor B','t')], 'n')
    d.box(270, 30, 120, 50, [('🌍 Edge','t'),('near A','s')], 'emerald')
    d.box(270, 150, 120, 50, [('🌍 Edge','t'),('near B','s')], 'emerald')
    d.box(510, 90, 120, 60, [('🏠 Origin','t'),('S3 or your app','s')], 'n')
    d.arrow([(120,55),(270,55)], 'emerald', label='short trip', at=(195,55))
    d.arrow([(120,175),(270,175)], 'emerald', label='short trip', at=(195,175))
    d.arrow([(390,55),(450,55),(450,110),(510,110)], 'amber', label='miss', at=(420,55))
    d.arrow([(390,175),(450,175),(450,130),(510,130)], 'amber', label='miss', at=(420,175))
    d.text(320, 230, 'A hit never leaves the edge; only a miss travels to the origin.', size=9.5, weight=700)
    return d

def build_caching_edge():
    body = ''
    body += see(figure(d_layers(),
        'a request travels down the layers until something has the answer. The <b>browser</b> may already hold the file. If not, a nearby <b>CloudFront edge</b> may have a copy. If not, an <b>ElastiCache</b> cache may hold the data. '
        'Only if all of those miss does the request reach the <b>database</b> — the slowest and most expensive place to ask. Each layer you answer from is a trip you did not make.'))
    body += one('A cache keeps a copy of an answer closer to whoever asks, so the slow, expensive place — usually the database — is asked far less often.')
    body += why([
      'You have copies of your app, a load balancer and Auto Scaling. But look at what every copy does: for the same product page, every request asks the <b>same database</b> the <b>same question</b>. Adding more app servers makes it worse, because now more servers ask the database.',
      'A cache fixes that by remembering recent answers. The result is faster pages and less load on the database. The price: a cached copy can be <b>out of date</b>. So caching is always a decision about <i>what</i> to copy, <i>where</i> to keep it, and <i>how long</i> it may stay.'])
    body += block('🧰 Where to cache', pick_cards([
      dict(icon='🌐', name='Browser cache', tag='on the visitor\'s device', color='#22d3ee',
           use=['Images, scripts and style files that rarely change', 'Controlled by the response headers your app or origin sends'],
           skip=['Anything private or fast-changing that must be fresh on every visit']),
      dict(icon='🌍', name='Amazon CloudFront', tag='a copy near the visitor', color='#34d399',
           use=['Static files and responses that are the same for everyone', 'Visitors spread across the world', 'You control expiry with Cache-Control headers or TTL settings, and can invalidate early'],
           skip=['Personal data that is different for every user']),
      dict(icon='⚡', name='Amazon ElastiCache', tag='a shared in-memory cache', color='#fbbf24',
           use=['Data many app copies read again and again', 'Results of slow database queries, sessions', 'Engines such as Valkey and Memcached'],
           skip=['Data you cannot afford to lose — a cache is a copy, not the source of truth']),
      dict(icon='🧠', name='In-app memory cache', tag='inside one app instance', color='#a78bfa',
           use=['Tiny, hot data that is the same everywhere', 'The fastest possible reads, with no network trip'],
           skip=['Several instances need to agree — each has its own private copy; use a shared cache']),
    ]), label_cls='see')
    body += block('🔁 The most common pattern: lazy loading', figure(d_aside(),
        'AWS calls it <b>lazy loading</b> (also known as cache-aside). <b>1</b> The app looks in the cache first. <b>2</b> On a miss, it reads the database. <b>3</b> It saves a copy in the cache for next time. '
        'Its weakness is <em>staleness</em>: if data changes in the database, the cached copy does not know. Fixes: set a <b>TTL</b> (time to live) on each item, or delete the cached item when you write.'), label_cls='see')
    body += block('🌍 Caching at the edge', figure(d_edge(),
        'with CloudFront, each visitor talks to an <b>edge location</b> near them. If it holds a copy (a <i>hit</i>), it answers at once. If not (a <i>miss</i>), it fetches from your origin and keeps the copy until it expires. '
        'CloudFront also has <b>regional edge caches</b> between the origin and the edge locations. You can remove content early with an <b>invalidation</b>, which takes a few minutes to complete; versioned file names avoid the need.'), label_cls='see')
    body += block('📊 Side by side', table(['','Where it lives','Shared?','Best for','Watch out for'], [
      ['🌐 Browser','Visitor\'s device','No — one per visitor','Static files','You cannot clear it remotely'],
      ['🌍 CloudFront','Edge locations near visitors','Yes, for people near that edge','Static and public content','Stale copies until they expire or are invalidated'],
      ['⚡ ElastiCache','Beside your app','Yes, for all app copies','Query results, sessions','Out-of-date data; it is only a copy'],
      ['🧠 In-app','Inside one instance','No — private to the instance','Tiny hot lookups','Each copy can hold different data'],
    ]), label_cls='see')
    body += proscons('⚖️ Lazy loading: the trade-offs',
      ['Only data that is actually asked for gets cached', 'If a cache node fails or is empty, the app still works — it just reads the database'],
      ['A miss costs three trips: cache, database, write back', 'Data can go stale; add a TTL or invalidate on write', 'A newly started cache is empty, so the first requests are slower'])
    body += block('🎬 Real-world scenarios', scenarios([
      ('🛍️','Product pages, read a lot, changed rarely','Every visit asks the database the same question.','ElastiCache, lazy loading with a TTL'),
      ('🖼️','Logo, images and style files','The same bytes for every visitor, everywhere.','CloudFront + browser cache'),
      ('🧾','A "my account balance" page','Different for every user and must be correct.','Do not cache — or only briefly'),
      ('🔑','Login sessions with many app copies','Any copy must recognise the user.','A shared cache'),
      ('📰','A news homepage hit by a spike','Many see the same page at once.','CloudFront with a short TTL'),
      ('📦','A deploy changes a stylesheet','Visitors still get the old file.','Versioned file names, or an invalidation'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — freshness and write strategies', '''      <p><b>Freshness is the whole game.</b> Every cached item needs an expiry time, and a way to throw it away when the source changes. A short TTL is fresher but misses more; a long one is faster but staler.</p>
      <p><b>Write-through</b> writes to the database and the cache together, so the cache stays current — but a new empty node has no data, and much of what is cached may never be read. AWS commonly recommends combining lazy loading with write-through, and adding a TTL to each write to get the benefits of both.</p>
      <p><b>Invalidate rather than update.</b> A simple guide for writes is to delete the cached entry rather than update it; a narrow race remains, so strict consistency may need locks or versioned writes.</p>
      <p><b>CloudFront TTLs.</b> Caching is governed by the origin\'s Cache-Control headers; without them the behaviour\'s default TTL applies, bounded by the minimum and maximum TTL. Invalidation requests are not immediate and can be charged beyond a free allowance; versioned names avoid that. Origins can also tag objects so you invalidate by tag.</p>
      <p><b>Engines and names change.</b> Check the ElastiCache documentation for the engines and node options available today.</p>''')
    body += recall([
      'A cache keeps copies closer to the asker so the slow source is asked less. The price is possible staleness.',
      'Layers: browser → CloudFront edge → ElastiCache → database.',
      'Lazy loading: check cache; on miss read the database and save a copy. Weakness: stale data — use a TTL or delete on write.',
      'Write-through keeps the cache fresh but fills it with data that may never be read; combine with lazy loading and a TTL.',
      'CloudFront serves from the edge until expiry; invalidations take minutes; versioned file names avoid them.'])
    body += saythis('"A cache trades freshness for speed. I cache in layers: the browser, CloudFront at the edge for content that is the same for everyone, and ElastiCache in front of the database. '
      'I use lazy loading with a TTL, sometimes combined with write-through, and I invalidate or version content when it changes. I never treat the cache as the source of truth."')
    body += trap([
      '<b>Do not treat the cache as the source of truth.</b> It is a copy and can disappear or go stale. Your app must still work, and recover, from the database alone.',
      'Second trap: <b>caching personal data in a shared place.</b> An edge or shared cache that stores one user\'s page and serves it to another is a serious bug. Cache only what is the same for everyone, or key the cache carefully.'])
    body += confuse('⚡ ElastiCache', 'Sits next to your app and holds data and query results, shared by all your app copies.', '🌍 CloudFront', 'Sits near the visitor and holds whole responses and files. Saves the trip across the world.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># lazy loading in plain pseudo-code</span>
item = cache.get(key)
if item is None:               <span class="cmt"># miss</span>
    item = database.read(key)  <span class="cmt"># slow path</span>
    cache.set(key, item, ttl=minutes)  <span class="cmt"># save a copy, with an expiry</span>
return item''',
      'Illustrative pseudo-code only — real client libraries have their own method names and options.'))
    body += next_box('Your app is now fast and can take heavier load. But some work should not happen while a user waits — it should be handed off and done in the background. Next: Messaging &amp; Events.', 'messaging.html', 'Messaging &amp; Events')
    body += fact_note(FOOT, [DOCS_CF, DOCS_EXP, DOCS_INV, DOCS_EC, DOCS_STR])
    return page('caching-edge', 'Caching & Edge Delivery', 'Concept 10 of 19 · ⚙️ Handling load',
        'A cache keeps a copy of an answer close to whoever asks — <span class="grad-text">so the slow, expensive place is asked far less often.</span>',
        'The layers of caching on AWS — browser, CloudFront, ElastiCache — lazy loading, write-through and the freshness trade-off.',
        'What is caching, where would you cache on AWS, and what is lazy loading?',
        body, CR + ['<span class="cur">Caching &amp; Edge</span>'], '', search_title='Caching & Edge Delivery')
