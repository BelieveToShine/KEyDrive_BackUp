from kit import *
from p_common import CR

DOCS_GI = ('AWS Global Infrastructure: Regions and Availability Zones', 'https://aws.amazon.com/about-aws/global-infrastructure/regions_az/')
DOCS_REG = ('AWS Regions and Availability Zones user guide', 'https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html')
DOCS_ZONES = ('AWS Local Zones', 'https://aws.amazon.com/about-aws/global-infrastructure/localzones/')
FOOT = 'Cloud services change often — the number of Regions and zones grows every year, so this page uses no counts. For the current list and service availability per Region, check the official AWS docs.'

def d_region():
    d = Diagram('rg1', 640, 312, 'An AWS Region contains several Availability Zones joined by fast links; resources are not copied to another Region unless you set that up')
    d.zone(10, 8, 620, 186, 'cyan', 'ONE REGION · a geographic area, isolated from other Regions')
    for i,(x,t) in enumerate([(30,'a'),(250,'b'),(470,'c')]):
        d.box(x, 50, 140, 118, [(f'🏢 AZ {t}','t'),('own power','s'),('own cooling','s'),('own network','s')], 'emerald')
    d.arrow([(170,109),(250,109)], 'cyan', label='link', at=(210,109), both=True)
    d.arrow([(390,109),(470,109)], 'cyan', label='link', at=(430,109), both=True)
    d.box(210, 246, 220, 54, [('🌐 Another Region','t'),('a separate, far-away copy','s')], 'n')
    d.arrow([(320,194),(320,246)], 'amber', label='only if you set it up', at=(400,220), dash=True)
    return d

def d_choose():
    d = Diagram('rg2', 640, 428, 'Decision tree for picking a Region: law first, then distance to users, then service availability')
    d.box(190, 8, 260, 34, [('🤔 Where should it run?','t')], 'cyan')
    qs = [
     ('📜 Must data stay in a country or area?', 'law, contracts or company rules', 'Pick by law', 'the Region is where data lives', 'rose'),
     ('⚡ Are most users in one area?', 'less distance means less delay', 'Closest Region', 'lower latency', 'cyan'),
     ('🧩 Do you need one specific service?', 'not every service is in every Region', 'Check the list', 'service support per Region', 'amber'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 366
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 366, 330, 50, [('🏢 Then, always','t'),('spread across zones inside the Region','s')], 'emerald')
    return d

def d_failure():
    d = Diagram('rg3', 640, 270, 'A load balancer sends traffic to healthy zones and skips the zone that lost power, so the app keeps running')
    d.box(250, 10, 140, 40, [('⚖️ Load balancer','t')], 'violet')
    d.box(30, 120, 170, 96, [('🏢 AZ a','t'),('a copy of the app','s'),('power lost','s')], 'rose')
    d.box(235, 120, 170, 96, [('🏢 AZ b','t'),('a copy of the app','s'),('running','s')], 'emerald')
    d.box(440, 120, 170, 96, [('🏢 AZ c','t'),('a copy of the app','s'),('running','s')], 'emerald')
    d.arrow([(280,50),(280,84),(115,84),(115,120)], 'rose', label='skipped', at=(200,84), dash=True)
    d.arrow([(320,50),(320,120)], 'emerald', label='serves', at=(320,96))
    d.arrow([(360,50),(360,84),(525,84),(525,120)], 'emerald', label='serves', at=(440,84))
    d.text(320, 246, 'Spread across zones and one datacenter failing is a non-event. A whole Region needs more (concept 9).', size=9.5, weight=700)
    return d

def build_regions_availability_zones():
    body = ''
    body += see(figure(d_region(),
        'a <b>Region</b> is a geographic area. Inside it are several <b>Availability Zones</b> (AZs) — separate datacenter groups, each with its own power, cooling and network, joined to each other by fast links. '
        'Regions are isolated from each other, and your resources live in <b>one Region</b> unless you deliberately copy them to another. So you choose two things: <i>which Region</i>, and <i>how many zones inside it</i>.'))
    body += one('Where you place resources decides how fast users are served and what happens when a datacenter fails — pick a Region for law and distance, and spread across zones for resilience.')
    body += why([
      'You have accounts to put things in. But a single datacenter is a single failure domain: one power cut and everything is gone. And users who are far away feel the distance in every click. <b>Where</b> you place resources decides both resilience and speed.',
      'AWS answers with a two-level map. <b>Regions</b> let you be near your users and keep data in the right country. <b>Availability Zones</b> let you survive the loss of one datacenter group without leaving the Region. The skill is knowing which problem each level solves — and not confusing them.'])
    body += block('🧰 The pieces', pick_cards([
      dict(icon='🌍', name='Region', tag='a geographic area', color='#22d3ee',
           use=['Choose where your data and compute live', 'Meet data-residency rules', 'Be close to your users for lower latency'],
           skip=['Expecting data to move between Regions on its own — it does not']),
      dict(icon='🏢', name='Availability Zone (AZ)', tag='an isolated datacenter group in a Region', color='#34d399',
           use=['Survive a datacenter-level failure', 'Spread copies of an app or database across zones', 'Fast links let you replicate between zones'],
           skip=['Treating one AZ as "the Region" — a single AZ is a single failure domain']),
      dict(icon='📍', name='Local Zones and Wavelength Zones', tag='edge placements near users', color='#a78bfa',
           use=['Put compute and storage closer to users in specific cities (Local Zones)', 'Ultra-low-latency apps on 5G networks (Wavelength Zones)'],
           skip=['A normal app — start with a Region and its AZs']),
      dict(icon='🔓', name='Opt-in Regions', tag='newer Regions you must enable', color='#fbbf24',
           use=['Regions launched after 2019 need to be enabled before you can use them', 'Older Regions are on by default'],
           skip=['Assuming every Region is available in a new account']),
    ]), label_cls='see')
    body += block('🧭 How to pick', figure(d_choose(),
        'ask in order. <b>Must the data stay in a country or area?</b> Then the law picks your Region. <b>Are most users in one area?</b> Pick the closest Region. <b>Need one specific service?</b> Check that it exists in that Region. '
        'Whatever you choose, <b>spread across Availability Zones</b> inside it. Price can differ between Regions too, but check the pricing pages rather than guess.'), label_cls='see')
    body += block('🔌 What a zone failure looks like', figure(d_failure(),
        'a copy of the app runs in each of three zones behind a load balancer (concept 8). Zone a loses power. The load balancer stops sending it traffic and the other two carry on. '
        'This is why "multi-AZ" is the first step of resilience. It does <em>not</em> protect against a whole Region failing, or against someone deleting data — those need more (Scaling &amp; Resilience, concept 9).'), label_cls='see')
    body += block('📊 Region, AZ and edge', table(['','Scope','Protects against','Cost of using it'], [
      ['🏢 One AZ','One datacenter group','Nothing — it is a single failure domain','Lowest, but riskiest'],
      ['🏢🏢 Several AZs','One Region','A datacenter-level failure','Some extra copies and cross-zone traffic'],
      ['🌍 Several Regions','A whole geography','A Region-level failure, and distance for users','Most complexity; data is replicated on purpose'],
      ['📍 Local or Wavelength Zone','A city or a telecom network','Latency, not failures','Only for special needs'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🇪🇺','A bank must keep customer data in Europe','Law decides.','Choose a Region in Europe'),
      ('🎮','Most players are in one country','They feel every millisecond.','The Region closest to them'),
      ('🛒','Shop must survive a datacenter outage','No manual work at 3 AM.','Copies in at least two zones, behind a load balancer'),
      ('🧩','A service you want is not in your Region yet','The docs list it for other Regions.','Check support first, then decide'),
      ('🌋','"The whole Region must be able to fail"','A rare, costly requirement.','Multi-Region design (concept 9)'),
      ('🎬','Video editing close to a city\'s studios','Needs very low latency to one city.','A Local Zone'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — how AWS describes the map', '''      <p>AWS describes each Region as a separate geographic area designed to be isolated from the other Regions. Each Region has multiple Availability Zones — a minimum of three — and each zone has independent power, cooling and physical security, linked by redundant, very-low-latency networks. AWS says its zones are far enough apart (up to about 100 km) to avoid common local disasters but close enough for fast replication between them.</p>
      <p><b>Resources are regional by default.</b> You can replicate some types of resources across Regions, but AWS does not do it for you automatically.</p>
      <p><b>Zone names differ per account.</b> The letters (a, b, c) you see in your account are mapped to physical zones per account, so "zone a" in one account is not always the same building as "zone a" in another. Use zone IDs when two accounts must line up. <i>(General AWS behaviour; check the docs for the details.)</i></p>
      <p><b>Some services are zonal, some regional.</b> A virtual server lives in one zone; a managed service may spread across zones for you. Always check which it is — this decides what "multi-AZ" takes from you.</p>''')
    body += recall([
      'Region = isolated geographic area. AZ = isolated datacenter group inside a Region, joined by fast links.',
      'Resources are regional by default; cross-Region copies are something you set up.',
      'Pick a Region by law (data residency), then distance to users, then service availability. Always spread across AZs.',
      'Multi-AZ survives a datacenter failure; a Region failure needs multi-Region (concept 9).',
      'Local Zones and Wavelength Zones put compute near specific cities or 5G networks; newer Regions need opt-in.'])
    body += saythis('"A Region is an isolated geographic area; inside it are Availability Zones — separate datacenter groups with their own power and cooling, joined by fast links. '
      'I pick the Region by data-residency law, then by distance to users, then by service availability, and I spread across at least two zones so a datacenter failure is a non-event. Surviving a whole Region needs a deliberate multi-Region design."')
    body += trap([
      '<b>Running everything in one AZ and calling it highly available.</b> One zone is one failure domain. Highly available means copies in more than one zone.',
      'Second trap: <b>expecting data to follow you across Regions.</b> Data stays in the Region you put it in. Moving or copying it is a choice you make, with its own cost.'])
    body += confuse('🌍 Region', 'Where your resources live: a geographic area. You choose it for law, latency and services.', '🏢 Availability Zone', 'A datacenter group inside the Region. You spread across zones to survive local failures.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># list the Availability Zones available in a Region</span>
aws ec2 describe-availability-zones --region eu-west-1''',
      'Illustrative shape only — the Region name is an example; output differs per account and Region.'))
    body += next_box('Resources now have a place and a map. Next question: once things exist in many places, <b>who or what is allowed to create, read or change each one</b>? Next: Identity &amp; Access (IAM).', 'identity-access.html', 'Identity &amp; Access (IAM)')
    body += fact_note(FOOT, [DOCS_GI, DOCS_REG, DOCS_ZONES])
    return page('regions-availability-zones', 'Regions & Availability Zones', 'Concept 2 of 19 · 🏗️ Foundations',
        'Where you place resources decides speed and survival — <span class="grad-text">pick a Region for law and distance, and spread across zones for resilience.</span>',
        'Regions, Availability Zones, Local Zones and opt-in Regions: how AWS is laid out, what each level protects against, and how to choose.',
        'What is the difference between an AWS Region and an Availability Zone?',
        body, CR + ['<span class="cur">Regions &amp; Availability Zones</span>'], '', search_title='Regions & Availability Zones')
