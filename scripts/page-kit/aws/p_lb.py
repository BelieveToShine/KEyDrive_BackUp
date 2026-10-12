from kit import *
from p_common import CR

DOCS_ELB = ('Elastic Load Balancing documentation', 'https://docs.aws.amazon.com/elasticloadbalancing/')
DOCS_HOW = ('How Elastic Load Balancing works', 'https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html')
DOCS_R53 = ('Choosing a Route 53 routing policy', 'https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html')
DOCS_FO = ('Route 53 failover types', 'https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-types.html')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official AWS docs.'

def d_grid():
    d = Diagram('lb1', 640, 300, 'AWS traffic tools by what they understand and how far they reach: ALB for web traffic in a Region, NLB for TCP and UDP, Gateway Load Balancer for appliances, Route 53 for DNS across Regions')
    d.text(335, 22, 'INSIDE ONE REGION', size=9.5, mono=True)
    d.text(555, 22, 'ACROSS REGIONS', size=9.5, mono=True)
    d.text(95, 100, 'Web traffic', size=10.5, weight=700)
    d.text(95, 116, '(HTTP and HTTPS)', size=9.5)
    d.text(95, 224, 'Any traffic', size=10.5, weight=700)
    d.text(95, 240, '(TCP and UDP)', size=9.5)
    d.box(210, 40, 250, 110, [('🚪 Application Load Balancer','t'),('layer 7 · one Region','s'),('reads the web request','s'),('path and host routing','s')], 'emerald')
    d.box(480, 40, 150, 240, [('🧭 Route 53','t'),('DNS · global','s'),('answers "which Region?"','s'),('health-checked','s'),('the only one here','s'),('that spans Regions','s')], 'amber')
    d.box(210, 170, 120, 110, [('⚖️ Network LB','t'),('layer 4','s'),('TCP and UDP','s'),('bursts, fixed IP','s')], 'violet')
    d.box(340, 170, 120, 110, [('🧱 Gateway LB','t'),('for virtual','s'),('appliances like','s'),('firewalls','s')], 'cyan')
    return d

def d_choose():
    d = Diagram('lb2', 640, 428, 'Decision tree: web traffic in one Region use an Application Load Balancer; TCP or UDP use a Network Load Balancer; appliances use a Gateway Load Balancer; several Regions add Route 53')
    d.box(190, 8, 260, 34, [('🤔 What is the traffic?','t')], 'cyan')
    qs = [
     ('🌐 A web app or API (HTTP or HTTPS)?', 'path and host routing', 'Application LB', 'layer 7, one Region', 'emerald'),
     ('🔌 TCP or UDP, bursts, fixed IPs?', 'games, voice, databases', 'Network LB', 'layer 4, very fast', 'violet'),
     ('🧱 Traffic through a firewall appliance?', 'third-party virtual appliances', 'Gateway LB', 'scales the appliances', 'cyan'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 366
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 366, 330, 52, [('🧭 More than one Region?','t'),('put Route 53 in front','s')], 'amber')
    return d

def d_r53():
    d = Diagram('lb3', 640, 312, 'Route 53 answers DNS with the address of a healthy Region and the client connects to it directly, so failover depends on how long DNS answers are cached')
    d.box(10, 110, 110, 64, [('👤 Client','t')], 'n')
    d.box(250, 110, 140, 64, [('🧭 Route 53','t'),('health checks','s')], 'amber')
    d.box(510, 20, 120, 56, [('🌍 Region A','t'),('healthy','s')], 'emerald')
    d.box(510, 208, 120, 56, [('🌍 Region B','t'),('unhealthy','s')], 'rose')
    d.arrow([(120,142),(250,142)], 'amber', label='DNS lookup', at=(185,142), both=True)
    d.arrow([(390,128),(450,128),(450,48),(510,48)], 'emerald', label='answers with', at=(450,88))
    d.arrow([(390,156),(450,156),(450,236),(510,236)], 'rose', label='skipped', at=(450,196), dash=True)
    d.text(320, 296, 'After the answer, the client talks to the Region directly; a cached answer can lag a failover.', size=9.5, weight=700)
    return d

def build_load_balancing():
    body = ''
    body += see(figure(d_grid(),
        'AWS has a small family of traffic tools, arranged by two questions. <b>Across</b>: inside one Region, or spread across Regions? <b>Down</b>: does it read the web request (HTTP and HTTPS), or just move connections (TCP and UDP)? '
        'The <b>Application Load Balancer</b> reads the web request; the <b>Network Load Balancer</b> moves raw connections; the <b>Gateway Load Balancer</b> fronts firewall-style appliances; <b>Route 53</b> works at the DNS level across Regions.'))
    body += one('A load balancer spreads traffic across healthy copies — and the real choice is how much of the request it should understand, and how far it should reach.')
    body += why([
      'Compute, storage and a database make one working instance. But one instance is a <b>single point of failure</b> and a ceiling on throughput. The obvious fix is more copies. The new problem: <b>who decides which copy gets each request?</b>',
      'That is what a load balancer does. It sits in front, spreads requests across targets, and <b>stops sending traffic to a target that is unhealthy</b>. On AWS the tools differ in what layer they work at and how far they reach — and "spread the traffic" inside a Region is a different job from sending a visitor to the nearest healthy Region.'])
    body += block('🧰 The tools', pick_cards([
      dict(icon='🚪', name='Application Load Balancer (ALB)', tag='layer 7 · HTTP and HTTPS', color='#34d399',
           use=['Web apps and APIs in one Region', 'Route by URL path or host name', 'Targets can be instances, containers and Lambda functions'],
           skip=['Raw TCP or UDP traffic → Network Load Balancer']),
      dict(icon='⚖️', name='Network Load Balancer (NLB)', tag='layer 4 · TCP and UDP', color='#a78bfa',
           use=['Handling sudden traffic bursts', 'Keeping the client\'s source IP', 'A fixed IP for the life of the load balancer'],
           skip=['You need to route by URL — that is an ALB']),
      dict(icon='🧱', name='Gateway Load Balancer (GWLB)', tag='for third-party virtual appliances', color='#22d3ee',
           use=['Send traffic through firewalls or inspection appliances and scale them', 'Needs extra integration — read the guide first'],
           skip=['Ordinary application load balancing']),
      dict(icon='🧭', name='Amazon Route 53', tag='DNS routing and health checks', color='#fbbf24',
           use=['Send users to the right Region: failover, weighted, latency, geolocation and other policies', 'Health checks decide which answers are used'],
           skip=['You need instant failover — DNS answers can be cached by clients']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'ask in order. <b>A web app or API?</b> An Application Load Balancer. <b>TCP or UDP, bursts, fixed IPs?</b> A Network Load Balancer. <b>Traffic through a firewall appliance?</b> A Gateway Load Balancer. '
        'And if the app runs in more than one Region, put <b>Route 53</b> in front to send people to the right one. The older <b>Classic Load Balancer</b> is the previous generation; AWS recommends migrating to the current types.'), label_cls='see')
    body += block('🧭 How Route 53 routes', figure(d_r53(),
        'Route 53 is a <b>DNS</b> service: the client asks "where is the app?", Route 53 answers with the address of a healthy Region, and the client then connects <em>directly</em>. '
        'Its routing policies decide the answer — <b>failover</b> (active-passive), <b>weighted</b> (split by proportion), <b>latency</b> (lowest delay), <b>geolocation</b> (by user location). Health checks take unhealthy answers out. Because answers can be cached, failover is not instant.'), label_cls='see')
    body += block('📊 Side by side', table(['','Layer','Reach','Reads the web request?','Good first use'], [
      ['🚪 ALB','7 (HTTP/HTTPS)','One Region','Yes — path, host','Web apps and APIs'],
      ['⚖️ NLB','4 (TCP/UDP)','One Region','No','Bursty or non-web traffic, fixed IPs'],
      ['🧱 GWLB','3 (network)','One Region','No','Firewall and inspection appliances'],
      ['🧭 Route 53','DNS','Global','No — it only answers DNS','Routing between Regions, failover'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🛒','A shop with /api and /images paths','Different targets per path.','Application Load Balancer'),
      ('🎮','Game servers over UDP','Not web traffic, many bursts.','Network Load Balancer'),
      ('🛡️','All traffic must pass a third-party firewall','Scale the appliances with demand.','Gateway Load Balancer'),
      ('🌍','Users in two continents','Send each to the closest healthy Region.','Route 53 latency routing'),
      ('🆘','The primary Region fails','Move users to the standby.','Route 53 failover with health checks'),
      ('🧪','Try a new version on a few users','Send a small share first.','Weighted records or weighted target groups'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — health, targets and the old one', '''      <p><b>Health checks decide where traffic goes.</b> A load balancer sends requests only to healthy targets, and Route 53 uses health checks to decide which answers to give. Make the health check meaningful: it should test what the app really needs, not just "the process is up".</p>
      <p><b>Weighted records:</b> a weight of 0 stops routing to that resource. If you use weighted records for failover, zero-weight records get traffic only when all non-zero records are unhealthy.</p>
      <p><b>Other Route 53 policies:</b> geoproximity, IP-based and multivalue answer also exist.</p>
      <p><b>Classic Load Balancer:</b> the previous generation. ALB and NLB are the purpose-built replacements and AWS offers a migration wizard that creates an equivalent new load balancer; you then redirect traffic yourself.</p>
      <p><b>Edge:</b> content delivery and edge caching (CloudFront) are in the Caching &amp; Edge concept.</p>''')
    body += recall([
      'ALB = layer 7, HTTP/HTTPS, path and host routing. NLB = layer 4, TCP/UDP, bursts, fixed IP. GWLB = third-party appliances. Route 53 = DNS across Regions.',
      'Load balancers send traffic only to healthy targets; health checks should test real dependencies.',
      'Route 53 policies: failover, weighted, latency, geolocation (and more). DNS answers can be cached, so failover is not instant.',
      'Classic Load Balancer is the previous generation — migrate to ALB or NLB.',
      'A load balancer does not make a single database highly available.'])
    body += saythis('"For web traffic in a Region I use an Application Load Balancer with path and host routing; for TCP or UDP and bursts I use a Network Load Balancer; for firewall appliances a Gateway Load Balancer. '
      'Across Regions I put Route 53 in front with latency or failover policies and health checks, remembering that DNS caching means failover is not instant."')
    body += trap([
      '<b>Expecting Route 53 failover to be instant.</b> It answers DNS; clients and resolvers may keep the old answer for a while.',
      'Second trap: <b>a load balancer is not high availability for the data tier.</b> It spreads traffic to the copies you have; if all copies depend on one database, that database is still your single point of failure.'])
    body += confuse('🚪 ALB', 'Understands the web request (layer 7): routes by path and host.', '⚖️ NLB', 'Moves connections (layer 4): TCP and UDP, bursts, fixed IPs. Cannot see the URL.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># create an internet-facing Application Load Balancer across two subnets</span>
aws elbv2 create-load-balancer --name shop-alb --type application \\
    --subnets &lt;subnet-a&gt; &lt;subnet-b&gt; --security-groups &lt;sg-id&gt;''',
      'Illustrative shape only — real setups also add a target group, a listener and health checks.'))
    body += next_box('Traffic now reaches many copies. But how many copies do you need — and what happens when a server, a datacenter or a Region fails? Next: Scaling &amp; Resilience.', 'scaling-resilience.html', 'Scaling &amp; Resilience')
    body += fact_note(FOOT, [DOCS_ELB, DOCS_HOW, DOCS_R53, DOCS_FO])
    return page('load-balancing', 'Load Balancing & Traffic Routing', 'Concept 8 of 19 · ⚙️ Handling load',
        'A load balancer spreads traffic across healthy copies — and the real choice is <span class="grad-text">how much of the request it should understand, and how far it should reach.</span>',
        'Application, Network and Gateway Load Balancers and Route 53: what each sees, how far it reaches and when to pick it.',
        'When would you use an Application Load Balancer, a Network Load Balancer or Route 53?',
        body, CR + ['<span class="cur">Load Balancing</span>'], '', search_title='Load Balancing & Traffic Routing')
