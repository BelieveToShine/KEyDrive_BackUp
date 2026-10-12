from kit import *
from p_storage import CR

DOCS_CA = ('Cache-Aside pattern (Architecture Center)', 'https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside')
DOCS_CG = ('Caching guidance (Architecture Center)', 'https://learn.microsoft.com/en-us/azure/architecture/best-practices/caching')
DOCS_AMR = ('Azure Managed Redis documentation', 'https://learn.microsoft.com/en-us/azure/redis/overview')
DOCS_AMRT = ('Choose a tier for Azure Managed Redis', 'https://learn.microsoft.com/en-us/azure/redis/plan-tiers-and-capacity')
DOCS_FD = ('Azure Front Door documentation', 'https://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview')
FOOT = 'Cloud services change often — caching products especially. This page teaches the ideas; for current product names, tiers and retirement dates, check the official docs.'

def d_layers():
    d = Diagram('ce1', 640, 372, 'Four places a copy can live between a visitor and the database: the browser, the edge, an app cache and the database itself')
    rows = [
      ('🌐 Browser cache','files kept on the visitor\'s own device','cyan'),
      ('🌍 Edge cache (Front Door)','a copy at a location near the visitor','emerald'),
      ('⚡ App cache (Azure Managed Redis)','shared, in memory, between the app and the database','amber'),
      ('🗄️ Database or origin','the source of truth — the slowest place to ask','n'),
    ]
    for i,(t,s_,c) in enumerate(rows):
        y = 10 + i*96
        d.box(20, y, 600, 58, [(t,'t'),(s_,'s')], c)
        if i < 3:
            d.arrow([(320,y+58),(320,y+96)], 'n', label='miss: ask the next layer', at=(450,y+77))
    return d

def d_aside():
    d = Diagram('ce2', 640, 262, 'Cache-aside: the app checks the cache first, reads the database on a miss, then saves a copy in the cache')
    d.box(20, 40, 110, 150, [('📱 App','t'),('your code','s')], 'n')
    d.box(300, 30, 150, 80, [('⚡ Cache','t'),('Azure Managed Redis','s')], 'amber')
    d.box(300, 150, 150, 80, [('🗄️ Database','t'),('source of truth','s')], 'violet')
    d.arrow([(130,66),(300,66)], 'amber', label='1 · check cache', at=(215,66))
    d.arrow([(130,98),(300,98)], 'amber', label='3 · save a copy', at=(215,98))
    d.arrow([(130,190),(300,190)], 'violet', label='2 · miss: read DB', at=(215,190))
    d.text(470, 58, 'Hit: the answer comes', anchor='start', size=9.5)
    d.text(470, 74, 'straight from the cache.', anchor='start', size=9.5)
    d.text(470, 170, 'Data changed? Write to the', anchor='start', size=9.5, weight=700)
    d.text(470, 186, 'database, then delete the', anchor='start', size=9.5, weight=700)
    d.text(470, 202, 'cached copy.', anchor='start', size=9.5, weight=700)
    return d

def d_edge():
    d = Diagram('ce3', 640, 246, 'Visitors reach a nearby edge location; only a cache miss travels on to the origin')
    d.box(10, 30, 110, 50, [('👤 Visitor A','t')], 'n')
    d.box(10, 150, 110, 50, [('👤 Visitor B','t')], 'n')
    d.box(270, 30, 120, 50, [('🌍 Edge','t'),('near A','s')], 'emerald')
    d.box(270, 150, 120, 50, [('🌍 Edge','t'),('near B','s')], 'emerald')
    d.box(510, 90, 120, 60, [('🏠 Origin','t'),('your app','s')], 'n')
    d.arrow([(120,55),(270,55)], 'emerald', label='short trip', at=(195,55))
    d.arrow([(120,175),(270,175)], 'emerald', label='short trip', at=(195,175))
    d.arrow([(390,55),(450,55),(450,110),(510,110)], 'amber', label='miss', at=(420,55))
    d.arrow([(390,175),(450,175),(450,130),(510,130)], 'amber', label='miss', at=(420,175))
    d.text(320, 230, 'A hit never leaves the edge; only a miss travels to the origin.', size=9.5, weight=700)
    return d

def build_caching_edge():
    body = ''
    body += see(figure(d_layers(),
        'a request travels down the layers until something has the answer. The <b>browser</b> may already hold the file. If not, a nearby <b>edge cache</b> may have a copy. If not, an <b>app cache</b> such as Azure Managed Redis may hold the data. '
        'Only if all of those miss does the request reach the <b>database</b> — the slowest and most expensive place to ask. Each layer you answer from is a trip you did not make.'))
    body += one('A cache keeps a copy of an answer closer to whoever asks, so the slow, expensive place — usually the database — is asked far less often.')
    body += why([
      'You have copies of your app, a load balancer and autoscale. But look at what every copy does: for the same product page, every request asks the <b>same database</b> the <b>same question</b>. Adding more app servers makes it worse, because now more servers ask the database.',
      'A cache fixes that by remembering recent answers. The result is faster pages for users and less load on the database. The price: a cached copy can be <b>out of date</b>. So caching is always a decision about <i>what</i> to copy, <i>where</i> to keep it, and <i>how long</i> it may stay.'])
    body += block('🧰 Where to cache', pick_cards([
      dict(icon='🌐', name='Browser cache', tag='on the visitor\'s device', color='#22d3ee',
           use=['Images, scripts and style files that rarely change', 'You control it with the response headers your app sends'],
           skip=['Anything private or fast-changing that must be fresh on every visit']),
      dict(icon='🌍', name='Edge cache (Front Door)', tag='a copy near the visitor', color='#34d399',
           use=['Static files and responses that are the same for everyone', 'Visitors spread across the world', 'You can purge it, set how long to keep things, and cache by query string'],
           skip=['Personal data that is different for every user']),
      dict(icon='⚡', name='Azure Managed Redis', tag='a shared in-memory cache', color='#fbbf24',
           use=['Data many app copies read again and again', 'Results of slow database queries', 'Sessions and other quick shared state'],
           skip=['Data you cannot afford to lose — it is a copy, not the source of truth']),
      dict(icon='🧠', name='In-app memory cache', tag='inside one app instance', color='#a78bfa',
           use=['Tiny, hot data that is the same everywhere', 'The fastest possible reads, with no network trip'],
           skip=['Several instances need to agree — each instance has its own private copy, so use a shared cache']),
    ]), label_cls='see')
    body += block('🔁 The most common pattern: cache-aside', figure(d_aside(),
        'the app talks to the cache <em>and</em> the database. <b>1</b> It looks in the cache first. <b>2</b> On a miss, it reads the database. <b>3</b> It saves a copy in the cache for next time. '
        'When data changes, write it to the database and then delete the cached copy, so the next read loads fresh data. Microsoft calls this the Cache-Aside pattern.'), label_cls='see')
    body += block('🌍 Caching at the edge', figure(d_edge(),
        'with an edge cache, each visitor talks to a location <b>near them</b>. If that location already holds a copy (a <i>hit</i>), it answers at once. If not (a <i>miss</i>), it fetches from your origin once and keeps the copy for the next visitor. '
        'Azure Front Door can cache like this, with expiry times, purging, query-string handling and compression.'), label_cls='see')
    body += block('📊 Side by side', table(['','Where it lives','Shared?','Best for','Watch out for'], [
      ['🌐 Browser','Visitor\'s device','No — one per visitor','Static files','You cannot clear it remotely'],
      ['🌍 Edge','Near the visitor','Yes, for people near that edge','Static and public content','Stale copies until they expire or you purge'],
      ['⚡ Managed Redis','Beside your app','Yes, for all app copies','Query results, sessions','Out-of-date data; it is only a copy'],
      ['🧠 In-app','Inside one instance','No — private to the instance','Tiny hot lookups','Each copy can hold different data'],
    ]), label_cls='see')
    body += proscons('⚖️ Cache-aside: the trade-offs',
      ['The cache holds only what is actually asked for', 'Works even when the cache has no built-in loading logic', 'If the cache is empty or gone, the app still works — it just reads the database'],
      ['It does not guarantee the cache and the database agree', 'Expire too early and you reload constantly; too late and you serve old data', 'A poor fit when most requests miss the cache anyway', 'Avoid caching sensitive data'])
    body += block('🎬 Real-world scenarios', scenarios([
      ('🛍️','Product pages, read a lot, changed rarely','Every visit asks the database the same question.','Managed Redis, cache-aside'),
      ('🖼️','Logo, images and style files','The same bytes for every visitor, everywhere.','Edge cache + browser cache'),
      ('🧾','A "my account balance" page','Different for every user and must be correct.','Do not cache — or only briefly'),
      ('🔑','Login sessions with many app copies','Any copy must recognise the user.','Shared cache (Redis)'),
      ('📰','A news homepage hit by a spike','Millions see the same page at once.','Edge cache with a short expiry'),
      ('🧮','One small settings list used everywhere','Tiny and almost never changes.','In-app memory cache'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — freshness, and the names to check', '''      <p><b>Freshness is the whole game.</b> Every cached item needs an expiry time, and you need a way to throw it away when the source changes (invalidate it). Short expiry = fresher but more misses. Long expiry = faster but staler.</p>
      <p><b>A cache can also help when the origin is down.</b> Microsoft notes that a cache can serve as a limited fallback if the data store is temporarily unavailable — one more reason to treat it as a layer, not just a speed-up.</p>
      <p><b>Product names are moving.</b> Azure Managed Redis is Microsoft\'s current recommendation for a Redis cache, with tiers such as Memory Optimized, Balanced, Compute Optimized and Flash Optimized (which moves less-used data to flash storage). The older Azure Cache for Redis tiers are being retired and Microsoft recommends migrating. On the edge side, use Azure Front Door <b>Standard or Premium</b>; Front Door (classic) and Azure CDN Standard (classic) are being retired. Always check the retirement pages for dates before planning.</p>
      <p>Because a look-aside cache only holds copies of database records, moving to a new cache is usually easy: create the new one, point the app at it, and let it refill.</p>''')
    body += recall([
      'A cache keeps copies close to the asker so the slow source is asked less. The price is possible staleness.',
      'Layers: browser → edge (Front Door) → app cache (Azure Managed Redis) → database.',
      'Cache-aside: check the cache; on a miss read the database and save a copy; when data changes, write to the database and delete the cached copy.',
      'Cache-aside does not guarantee consistency; expiry that is too short or too long both hurt. Avoid caching sensitive data.',
      'A per-instance memory cache is private to that instance; use a shared cache when several instances need the same data.'])
    body += saythis('"A cache trades freshness for speed. I cache in layers: the browser, an edge cache like Front Door for content that is the same for everyone, and a shared cache like Azure Managed Redis in front of the database. '
      'I use cache-aside — check the cache, on a miss read the database and save a copy, and on a change write to the database and delete the cached item. I set expiry times deliberately, and I do not cache sensitive or must-be-correct data."')
    body += trap([
      '<b>Do not treat the cache as the source of truth.</b> It is a copy and can disappear or go stale. Your app must still work, and recover, from the database alone.',
      'Second trap: <b>caching personal data in a shared place.</b> An edge or shared cache that stores one user\'s page and serves it to another is a serious bug. Cache only what is the same for everyone, or key the cache carefully.'])
    body += confuse('⚡ App cache (Redis)', 'Sits next to your app and holds data and query results. Shared by all your app copies.', '🌍 Edge cache (Front Door)', 'Sits near the visitor and holds whole responses and files. Saves the trip across the world.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># cache-aside in plain pseudo-code</span>
item = cache.get(key)
if item is None:               <span class="cmt"># miss</span>
    item = database.read(key)  <span class="cmt"># slow path</span>
    cache.set(key, item, expires_in=minutes)  <span class="cmt"># save a copy, with an expiry</span>
return item''',
      'Illustrative pseudo-code only — real clients (for example a Redis client library) have their own method names and options.'))
    body += next_box('Your app is now fast and can take heavier load. But some work should not happen while a user waits — it should be handed off and done in the background. Next: Messaging &amp; Events.', 'messaging.html', 'Messaging &amp; Events')
    body += fact_note(FOOT, [DOCS_CA, DOCS_CG, DOCS_AMR, DOCS_AMRT, DOCS_FD])
    return page('caching-edge', 'Caching & Edge Delivery', 'Concept 10 of 19 · ⚙️ Handling load',
        'A cache keeps a copy of an answer close to whoever asks — <span class="grad-text">so the slow, expensive place is asked far less often.</span>',
        'Learn the layers of caching on Azure — browser, edge, shared app cache — the cache-aside pattern, and the freshness trade-off that every cache brings.',
        'What is caching, where would you cache on Azure, and what is the cache-aside pattern?',
        body, CR + ['<span class="cur">Caching &amp; Edge</span>'], '', search_title='Caching & Edge Delivery')
