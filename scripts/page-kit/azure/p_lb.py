from kit import *
from p_storage import CR

DOCS_LBO = ('Load-balancing options (Architecture Center)', 'https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/load-balancing-overview')
DOCS_LB = ('Azure Load Balancer documentation', 'https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-overview')
DOCS_AG = ('Azure Application Gateway documentation', 'https://learn.microsoft.com/en-us/azure/application-gateway/overview')
DOCS_FD = ('Azure Front Door documentation', 'https://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview')
DOCS_TM = ('Azure Traffic Manager documentation', 'https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-overview')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices, SKUs and new features, check the official docs.'

def d_grid():
    d = Diagram('lb1', 640, 300, 'The four Azure traffic tools arranged by what they understand (web traffic or any traffic) and how far they reach (one region or many)')
    d.text(335, 22, 'ONE REGION', size=9.5, mono=True)
    d.text(555, 22, 'MANY REGIONS', size=9.5, mono=True)
    # rows
    d.text(95, 100, 'Web traffic', size=10.5, weight=700)
    d.text(95, 116, '(HTTP and HTTPS)', size=9.5)
    d.text(95, 224, 'Any traffic', size=10.5, weight=700)
    d.text(95, 240, '(TCP and UDP)', size=9.5)
    d.box(210, 40, 250, 110, [('🚪 Application Gateway','t'),('layer 7 · one region','s'),('reads the web request','s'),('URL paths · TLS · optional WAF','s')], 'emerald')
    d.box(480, 40, 150, 110, [('🌍 Front Door','t'),('layer 7 · global','s'),('edge entry point','s'),('WAF · caching','s')], 'cyan')
    d.box(210, 170, 250, 110, [('⚖️ Load Balancer','t'),('layer 4 · one region','s'),('spreads TCP and UDP flows','s'),('does not read the web request','s')], 'violet')
    d.box(480, 170, 150, 110, [('🧭 Traffic Manager','t'),('DNS · global','s'),('answers "which region?"','s'),('any protocol','s')], 'amber')
    return d

def d_layers():
    d = Diagram('lb2', 640, 332, 'One way the tools stack: Front Door picks a region, Application Gateway routes by URL, an internal Load Balancer spreads work inside')
    d.box(10, 130, 80, 56, [('👤 Users','t'),('anywhere','s')], 'n')
    d.box(170, 130, 112, 56, [('🌍 Front Door','t'),('global entry','s')], 'cyan')
    d.zone(318, 8, 312, 166, 'n', 'REGION 1 · healthy')
    d.zone(318, 186, 312, 138, 'rose', 'REGION 2 · unhealthy')
    d.box(332, 36, 116, 56, [('🚪 App Gateway','t'),('routes by path','s')], 'emerald')
    d.box(516, 36, 104, 34, [('🖥️ Web VMs','t')], 'n')
    d.box(516, 124, 104, 34, [('⚖️ Internal LB','t')], 'violet')
    d.box(332, 232, 116, 56, [('🚪 App Gateway','t'),('probe failed','s')], 'rose')
    d.box(516, 232, 104, 56, [('🖥️ Web VMs','t'),('not answering','s')], 'rose')
    d.arrow([(90,158),(170,158)], 'cyan', label='HTTPS', at=(130,158))
    d.arrow([(226,130),(226,64),(332,64)], 'emerald', label='nearest', at=(272,64))
    d.arrow([(448,53),(516,53)], 'emerald', label='path', at=(482,53))
    d.arrow([(568,70),(568,124)], 'violet', label='then spreads', at=(568,97))
    d.arrow([(226,186),(226,260),(332,260)], 'rose', label='skipped', at=(280,260), dash=True)
    return d

def d_choose():
    d = Diagram('lb3', 640, 340, 'Decision tree: web traffic or not, then one region or many, leads to Application Gateway, Front Door, Load Balancer or Traffic Manager')
    d.box(200, 8, 240, 44, [('🤔 Is it web traffic?','t'),('HTTP or HTTPS','s')], 'cyan')
    d.arrow([(250,52),(250,80),(160,80),(160,104)], 'emerald', label='yes', at=(205,80))
    d.arrow([(390,52),(390,80),(480,80),(480,104)], 'violet', label='no', at=(435,80))
    d.box(20, 104, 280, 52, [('More than one region?','t'),('for a web app or API','s')], 'n')
    d.box(340, 104, 280, 52, [('More than one region?','t'),('TCP, UDP or other traffic','s')], 'n')
    d.arrow([(90,156),(90,236)], 'emerald', label='one region', at=(90,196))
    d.arrow([(230,156),(230,236)], 'cyan', label='many regions', at=(230,196))
    d.arrow([(410,156),(410,236)], 'violet', label='one region', at=(410,196))
    d.arrow([(550,156),(550,236)], 'amber', label='many regions', at=(550,196))
    d.box(20, 236, 140, 64, [('🚪 Application','t'),('Gateway','t')], 'emerald')
    d.box(170, 236, 130, 64, [('🌍 Front Door','t')], 'cyan')
    d.box(340, 236, 140, 64, [('⚖️ Load','t'),('Balancer','t')], 'violet')
    d.box(490, 236, 130, 64, [('🧭 Traffic','t'),('Manager','t')], 'amber')
    d.text(320, 326, 'Real systems often combine them — each answer above is the starting point.', size=9.5, weight=700)
    return d

def d_dns():
    d = Diagram('lb4', 640, 308, 'Traffic Manager only answers a DNS question and steps aside, while Front Door stays in the path of every request')
    d.zone(10, 8, 620, 134, 'amber', 'TRAFFIC MANAGER · answers DNS, then steps aside')
    d.box(24, 42, 100, 56, [('👤 Client','t')], 'n')
    d.box(268, 42, 132, 56, [('🧭 Traffic','t'),('Manager','t')], 'amber')
    d.box(512, 42, 104, 56, [('🌐 A region','t')], 'n')
    d.arrow([(124,70),(268,70)], 'amber', label='DNS lookup', at=(196,70), both=True)
    d.arrow([(74,98),(74,124),(564,124),(564,98)], 'n', label='then connects directly', at=(319,124))
    d.zone(10, 160, 620, 106, 'cyan', 'FRONT DOOR · stays in the path of every request')
    d.box(24, 192, 100, 56, [('👤 Client','t')], 'n')
    d.box(268, 192, 132, 56, [('🌍 Front Door','t')], 'cyan')
    d.box(512, 192, 104, 56, [('🌐 A region','t')], 'n')
    d.arrow([(124,220),(268,220)], 'cyan', label='every request', at=(196,220))
    d.arrow([(400,220),(512,220)], 'cyan', label='forwards', at=(456,220))
    d.text(320, 292, 'A DNS answer can be cached, so a failover reaches clients only after the cached answer expires.', size=9.5, weight=700)
    return d

def build_load_balancing():
    body = ''
    body += see(figure(d_grid(),
        'four tools, arranged by two questions. <b>Across</b>: how far do you need to reach — one region, or many? <b>Down</b>: how much of the traffic does the tool understand — the web request itself (HTTP and HTTPS), or just connections (TCP and UDP)? '
        'The two at the top read the web request. The two at the bottom do not. The two on the right work across regions.'))
    body += one('A load balancer is a front door that spreads traffic across healthy copies of your app — and the real choice is how much of the request it should understand, and how far it should reach.')
    body += why([
      'The last concept ended with one app server and one database — a working instance. But one instance is a <b>single point of failure</b>, and it can only handle so much traffic. The obvious fix is more copies. The new problem: <b>who decides which copy gets each request?</b>',
      'That is what a load balancer does. It sits in front, spreads requests across the copies, and <b>stops sending traffic to a copy that is unhealthy</b> (it checks with health probes). Azure has four tools for this, because "spread the traffic" means different things: spreading raw connections inside one region is not the same job as sending a visitor on another continent to the nearest healthy region.'])
    body += block('🧰 The four tools', pick_cards([
      dict(icon='⚖️', name='Azure Load Balancer', tag='layer 4 · TCP and UDP · one region', color='#a78bfa',
           use=['Any TCP or UDP traffic, not just web traffic', 'Spreading connections across VMs inside one region', 'Zone-redundant setups that survive a datacenter failure'],
           skip=['You need URL routing, TLS termination or a WAF → Application Gateway', 'You need to reach several regions']),
      dict(icon='🚪', name='Application Gateway', tag='layer 7 · web traffic · one region', color='#34d399',
           use=['HTTP and HTTPS apps in one region', 'Route by URL path or by host name (several sites behind one gateway)', 'Terminate TLS at the gateway; add a web application firewall (WAF)'],
           skip=['Non-web traffic → Load Balancer', 'Users in many regions → Front Door']),
      dict(icon='🌍', name='Azure Front Door', tag='layer 7 · web traffic · global', color='#22d3ee',
           use=['A web app with users in many places', 'Fast routing to the nearest healthy region, with failover', 'Edge features: a WAF and caching at the edge'],
           skip=['Non-HTTP traffic', 'A small app that lives in a single region']),
      dict(icon='🧭', name='Azure Traffic Manager', tag='DNS-based · global · any protocol', color='#fbbf24',
           use=['Non-web traffic that must be spread across regions', 'Routing by priority, weight, performance or geography', 'You want a simple DNS-level switch between regions'],
           skip=['You need fast failover — DNS answers can be cached by clients', 'You need to read or change web requests']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'two questions are enough to land on a starting point. <b>First</b>: is it web traffic (HTTP or HTTPS)? <b>Second</b>: do you need more than one region? '
        'Web traffic in one region → <b>Application Gateway</b>. Web traffic across regions → <b>Front Door</b>. Other traffic in one region → <b>Load Balancer</b>. Other traffic across regions → <b>Traffic Manager</b>. This is Microsoft\'s own rule of thumb.'), label_cls='see')
    body += block('🔬 Why Traffic Manager and Front Door fail over differently', figure(d_dns(),
        '<b>Traffic Manager</b> (top) works at the DNS level. The client asks "where is the app?", gets an address, and then connects <em>directly</em> — Traffic Manager is no longer involved. '
        'That is why a failover can lag: clients and resolvers may keep the old DNS answer until it expires. <b>Front Door</b> (bottom) sits in the path of every request, so it can stop using an unhealthy origin right away.'), label_cls='see')
    body += block('🧱 How they fit together', figure(d_layers(),
        'one common shape, shown as an example rather than a rule. <b>Front Door</b> picks the nearest <em>healthy</em> region. Inside that region, <b>Application Gateway</b> routes by URL path, and an <b>internal Load Balancer</b> spreads work among the servers of the next tier. '
        'Region 2 failed its health probes, so Front Door never sends traffic there. The tools are different layers, not competitors.'), label_cls='see')
    body += block('📊 Side by side', table(['','Works on','Reach','Reads the web request?','Good first use'], [
      ['⚖️ Load Balancer','TCP and UDP connections (layer 4)','One region','No','VMs behind a private or public IP'],
      ['🚪 Application Gateway','HTTP and HTTPS (layer 7)','One region','Yes — URL, host, cookies','Web app with path routing and a WAF'],
      ['🌍 Front Door','HTTP and HTTPS (layer 7)','Global, at the edge','Yes','Global web app with fast failover'],
      ['🧭 Traffic Manager','DNS answers','Global','No — it only answers DNS','Spreading non-web traffic across regions'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🛒','Shop website in one region','Pages, an API and images. Path <code>/api</code> goes to one pool, the rest to another.','Application Gateway'),
      ('🌐','Global news site','Readers on every continent. It must stay up if one region fails.','Front Door'),
      ('🎮','Game servers over UDP','Not web traffic. Many VMs in one region share the load.','Load Balancer'),
      ('📞','Voice service in two regions','Not HTTP. Send callers to the nearest working region.','Traffic Manager'),
      ('🗄️','Database cluster inside a VNet','Private traffic between tiers. Nothing is exposed to the internet.','Internal Load Balancer'),
      ('🛡️','Public API that needs a firewall','Block common web attacks before they reach the app.','Application Gateway or Front Door with a WAF'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — health probes and what "unhealthy" means', '''      <p>Every tool above decides where to send traffic <b>based on health</b>. Load Balancer uses health probes (TCP, HTTP or HTTPS) and stops sending new connections to an instance that fails them. The others have their own health checks as well.</p>
      <p><b>Make the health check honest.</b> A probe that only checks "is the server on?" will say "healthy" while the database is down. A good health endpoint checks the things the app really needs.</p>
      <p><b>Sticky sessions.</b> Application Gateway can keep one user on one server with cookie-based affinity. It works, but it makes scaling and failover harder — storing session data outside the server (see the next concept, and Caching) is usually better.</p>
      <p><b>SKUs and retirements.</b> Use the current ones: Load Balancer <b>Standard</b> (the Basic SKU has been retired) and Application Gateway <b>V2</b> (V1 has been retired). Front Door <b>Standard and Premium</b> are the current offerings.</p>''')
    body += recall([
      'Four tools, two questions: web traffic or not, one region or many.',
      'Load Balancer = layer 4 (TCP/UDP), one region. It does not read web requests.',
      'Application Gateway = layer 7 for one region: URL routing, TLS termination, optional WAF.',
      'Front Door = layer 7, global, at the edge: WAF, caching, fast failover. Traffic Manager = DNS-based, any protocol, slower failover because of DNS caching.',
      'Every one of them relies on health checks — a bad health check hides real failures.'])
    body += saythis('"Azure has four ways to spread traffic. Load Balancer works at layer 4 for TCP and UDP inside a region. Application Gateway works at layer 7 for web traffic in one region, with URL routing, TLS termination and an optional WAF. '
      'Front Door is the global layer-7 entry point with WAF, caching and fast failover. Traffic Manager is DNS-based, works for any protocol, and fails over more slowly because clients cache DNS answers. I pick by two questions — web traffic or not, one region or many."')
    body += trap([
      '<b>Do not choose Traffic Manager for a web app that needs fast failover.</b> It only answers DNS, and clients may keep an old answer. For web traffic across regions, Front Door is usually the better fit.',
      'Second trap: <b>a load balancer is not a firewall and does not make a single database highly available.</b> It spreads traffic to the copies that you have. If every copy depends on one database, that database is still your single point of failure.'])
    body += confuse('⚖️ Load Balancer', 'Spreads connections (layer 4). Cannot see the URL. Works for any TCP or UDP traffic.', '🚪 Application Gateway', 'Understands the web request (layer 7). Can route by path and host, and terminate TLS.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># create a Standard public Load Balancer — it needs a public IP, backends and a health probe to be useful</span>
az network lb create --name lb-shop --resource-group rg-shop-prod \\
    --sku Standard --public-ip-address pip-shop --frontend-ip-name fe \\
    --backend-pool-name be''',
      'Illustrative shape only — real setups also add a health probe and load-balancing rules, and the flags can change.'))
    body += next_box('Traffic now reaches many copies of your app. But how many copies do you need — and what happens when a server, or a whole datacenter, fails? Next: Scaling &amp; Resilience.', 'scaling-resilience.html', 'Scaling &amp; Resilience')
    body += fact_note(FOOT, [DOCS_LBO, DOCS_LB, DOCS_AG, DOCS_FD, DOCS_TM])
    return page('load-balancing', 'Load Balancing & Traffic Routing', 'Concept 8 of 19 · ⚙️ Handling load',
        'A load balancer spreads traffic across healthy copies — and the real choice is <span class="grad-text">how much of the request it should understand, and how far it should reach.</span>',
        'Azure has four tools for sending traffic where it should go: Load Balancer, Application Gateway, Front Door and Traffic Manager. Learn what each one sees, how far it reaches and when to pick it.',
        'When would you use Azure Load Balancer, Application Gateway, Front Door or Traffic Manager?',
        body, CR + ['<span class="cur">Load Balancing</span>'], '', search_title='Load Balancing & Traffic Routing')
