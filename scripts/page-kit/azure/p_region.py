from kit import *
from p_storage import CR

DOCS_REL = ('Azure reliability documentation', 'https://learn.microsoft.com/en-us/azure/reliability/')
DOCS_WAF = ('Azure Well-Architected Framework', 'https://learn.microsoft.com/en-us/azure/well-architected/')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official docs.'

def d_geo():
    d = Diagram('rg1', 640, 308, 'A region contains three availability zones, each with its own power, cooling and networking; a second region holds a copy for disaster recovery')
    d.zone(10, 8, 620, 176, 'cyan', 'REGION A · datacenters close together, joined by fast links')
    for i, x in enumerate((24, 226, 428)):
        d.box(x, 40, 188, 110, [(f'🏭 Zone {i+1}','t'),('its own power','s'),('its own cooling','s'),('its own network','s')], 'cyan')
    d.text(320, 172, 'Far enough apart to fail separately, close enough to stay fast.', size=9.5)
    d.zone(10, 224, 620, 76, 'violet', 'REGION B · somewhere else, often a different part of the world')
    d.box(330, 250, 290, 40, [('🏭 Another set of datacenters','t')], 'violet')
    d.arrow([(522,150),(522,250)], 'violet', label='a copy for disaster recovery', at=(425,200), flow=True)
    return d

def d_zonal():
    d = Diagram('rg2', 640, 256, 'A zonal resource is pinned to one zone and goes down with it; a zone-redundant resource runs in several zones and keeps running when one zone fails')
    d.zone(10, 8, 305, 240, 'rose', 'ZONAL · pinned to one zone')
    d.box(24, 48, 84, 110, [('Zone 1','t'),('💥 outage','s'),('🖥️ your VM','s')], 'rose')
    d.box(118, 48, 84, 110, [('Zone 2','t'),('(not used)','s')], 'n')
    d.box(212, 48, 84, 110, [('Zone 3','t'),('(not used)','s')], 'n')
    d.text(162, 184, 'Zonal resources are pinned to one zone.', size=9.5)
    d.text(162, 200, 'If that zone fails, they go down —', size=9.5)
    d.text(162, 216, 'multi-zone resilience is your job.', size=9.5, weight=700)
    d.zone(325, 8, 305, 240, 'emerald', 'ZONE-REDUNDANT · spread across zones')
    d.box(339, 48, 84, 110, [('Zone 1','t'),('💥 outage','s'),('copy lost','s')], 'rose')
    d.box(433, 48, 84, 110, [('Zone 2','t'),('✅ copy runs','s')], 'emerald')
    d.box(527, 48, 84, 110, [('Zone 3','t'),('✅ copy runs','s')], 'emerald')
    d.text(477, 184, 'Zone-redundant resources run in several zones.', size=9.5)
    d.text(477, 200, 'Azure handles the failover between zones.', size=9.5)
    d.text(477, 216, 'The usual recommendation, unless you have a reason.', size=9.5, weight=700)
    return d

def d_mapping():
    d = Diagram('rg3', 640, 266, 'The zone number you pick is a logical name: two subscriptions can map the same logical Zone 1 to different physical zones')
    d.box(10, 40, 180, 56, [('Subscription A','t'),('asks for "Zone 1"','s')], 'amber')
    d.box(10, 150, 180, 56, [('Subscription B','t'),('asks for "Zone 1"','s')], 'amber')
    d.box(470, 20, 160, 50, [('Physical zone 1','t'),('(not used here)','s')], 'n')
    d.box(470, 96, 160, 50, [('Physical zone 2','t'),("serves A's Zone 1",'s')], 'cyan')
    d.box(470, 172, 160, 50, [('Physical zone 3','t'),("serves B's Zone 1",'s')], 'cyan')
    d.arrow([(190,68),(330,68),(330,121),(470,121)], 'cyan', label='is really zone 2', at=(400,121))
    d.arrow([(190,178),(330,178),(330,197),(470,197)], 'cyan', label='is really zone 3', at=(400,197))
    d.text(320, 250, 'Same name, different datacenters — check the mapping when you use more than one subscription.', size=9.5)
    return d

def build_regions_availability_zones():
    body = ''
    body += see(figure(d_geo(),
        'a <b>region</b> is a place with datacenters in it. Inside many regions are <b>availability zones</b> — separate groups of datacenters, each with its own power, cooling and networking, so one zone can fail without taking the others down. '
        'Zones are linked by fast connections, so spreading an app across them stays quick. A <b>second region</b>, far away, can hold a copy for disaster recovery.'))
    body += one('A region is a place. Availability zones are separate groups of datacenters inside it. Spread across zones to survive one failing; use a second region to survive a whole area failing.')
    body += why([
      'You now know how to organize resources. But every resource must be created <b>somewhere real</b> — and a single datacenter is a single point of failure. A power cut, a cooling fault or a network problem there takes your whole app down. '
      'Far-away users also feel the distance: a request to the other side of the world is slower than one next door.',
      'So Azure gives you <b>regions</b> to put things near your users and under the right laws, and <b>availability zones</b> to survive a datacenter-level failure without leaving the region. Choosing well is one of the cheapest reliability decisions you will ever make.'])
    body += block('📖 The words you need', '''    <div class="taxonomy-strip">
      <div class="tax-item"><h5>🌍 Region</h5><p>A place in the world where Azure has datacenters. You choose a region when you create most resources.</p></div>
      <div class="tax-item"><h5>🏭 Availability zone</h5><p>A separate group of datacenters inside a region, with its own power, cooling and networking. Regions that support zones have at least three.</p></div>
      <div class="tax-item"><h5>🤝 Paired region</h5><p>Some regions are paired with another one for disaster-recovery features. Microsoft decides the pairs — you cannot choose your own. Many regions are not paired at all and rely on zones.</p></div>
      <div class="tax-item"><h5>📌 Zonal</h5><p>A resource pinned to one specific zone, like a VM you place in zone 1.</p></div>
      <div class="tax-item"><h5>🔀 Zone-redundant</h5><p>A resource that Azure spreads across zones for you, and fails over if one zone is lost.</p></div>
    </div>''', label_cls='see')
    body += block('🛡️ Zonal or zone-redundant?', figure(d_zonal(),
        '<b>Left — zonal:</b> your VM lives in zone 1. When zone 1 has an outage, the VM goes down with it, and keeping the app alive is your job. '
        '<b>Right — zone-redundant:</b> copies run in every zone, so when zone 1 fails the others carry on and Azure handles the failover. '
        'Microsoft recommends zone-redundant deployments unless you have a strong reason to pin a resource to one zone. Support differs by service — some are zone-redundant by default, others need you to switch it on.'), label_cls='see')
    body += block('🧭 How to choose a region — five questions', '''    <div class="taxonomy-strip">
      <div class="tax-item"><h5>1 · Where are my users?</h5><p>The closer the region, the faster the response. Put the app near the people who use it.</p></div>
      <div class="tax-item"><h5>2 · Are there rules about my data?</h5><p>Laws or company policy may say where data may live. Check this before you build, not after.</p></div>
      <div class="tax-item"><h5>3 · Is the service there?</h5><p>Not every service or feature is available in every region. Check the region list for the services you need.</p></div>
      <div class="tax-item"><h5>4 · Does it have zones?</h5><p>Not every region supports availability zones. If you need zone resilience, pick a region that does.</p></div>
      <div class="tax-item"><h5>5 · What does it cost?</h5><p>Prices can differ between regions, so compare for big workloads.</p></div>
    </div>''', label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🏢','Internal tool, one office','Used 9 to 5 by one team. A short outage is annoying, not costly.','One region, one zone is fine'),
      ('💳','Payments API','Every minute of downtime loses money.','Zone-redundant, in a region with zones'),
      ('🌐','Global SaaS product','Customers on three continents expect fast pages and survive a region outage.','Several regions'),
      ('📜','Data must stay in one country','A law forbids storing customer records abroad.','A region inside that country'),
      ('🧪','Dev and test','Cheap, disposable, nobody is waiting on it.','One region, no zone redundancy'),
      ('💾','Backups','If the primary region is lost, the backups must survive.','A copy in another region'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — the zone number is a label, not a place', figure(d_mapping(),
        'when you ask for "Zone 1", that is a <b>logical</b> name. Azure maps each subscription\'s logical zones to physical zones separately, so Zone 1 in subscription A can be a different group of datacenters than Zone 1 in subscription B. '
        'It matters when two subscriptions must sit in the <em>same</em> physical zone (to keep latency low) — check the mapping instead of assuming the numbers match.'))
    body += recall([
      'Region = a place with datacenters. Availability zone = a separate group of datacenters inside a region (own power, cooling, networking); zone-enabled regions have at least three.',
      'Zonal = pinned to one zone (you handle failover). Zone-redundant = spread across zones (Azure handles failover). Prefer zone-redundant.',
      'Region pairs are assigned by Microsoft, and many regions are unpaired. Zones protect against a zone failure, not a whole-region failure.',
      'Choose a region by: users, data rules, service availability, zone support, price.',
      'Zone numbers are logical and mapped per subscription.'])
    body += saythis('"A region is a geographic area with datacenters; availability zones are physically separate groups of datacenters inside a region, each with independent power, cooling and networking. '
      'I prefer zone-redundant services so Azure handles failover across zones, use a second region when I must survive a regional outage, and choose the region by user latency, data-residency rules, service availability and zone support."')
    body += trap([
      '<b>Availability zones do not protect you from a whole-region outage.</b> They protect against a zone failing. If losing the entire region would be a disaster, you also need a second region — that is a later concept, but you must design for it from the start.',
      'Second trap: <b>you cannot pick a region pair.</b> Microsoft assigns them, and many regions have no pair — they rely on zones instead. Do not plan around a pairing you assumed.'])
    body += confuse('🏭 Availability zone', 'A separate group of datacenters inside one region. Protects against a datacenter-level failure, with fast links between zones.', '🌍 Region', 'A whole geographic area. A second region protects against a regional outage and puts data nearer other users.')
    body += zoom('💻 Tiny illustrative examples', code_block(
'''<span class="cmt"># a zonal VM: pinned to zone 1 (if zone 1 fails, this VM is down)</span>
az vm create --resource-group rg-shop-prod --name vm-web1 --image Ubuntu2204 --zone 1

<span class="cmt"># a zone-redundant storage account: copies are spread across zones</span>
az storage account create --name stshopprod001 --resource-group rg-shop-prod \\
    --location westeurope --sku Standard_ZRS''',
      'Illustrative shape only — the storage account name must be globally unique, and VM images and sizes vary by region.'))
    body += next_box('Your resources now live in the right place and survive a zone failing. But <b>who</b> is allowed to create, change and delete them — people <em>and</em> apps? Next: identity and access.', 'identity-access.html', 'Identity &amp; Access')
    body += fact_note(FOOT, [DOCS_REL, DOCS_WAF])
    return page('regions-availability-zones', 'Regions & Availability Zones', 'Concept 2 of 19 · 🏗️ Foundations',
        'Where you place resources decides <span class="grad-text">how fast and how safe</span> your app is.',
        'A single datacenter is a single point of failure, and distance means delay. Learn what regions and availability zones are, how zonal and zone-redundant resources behave when something breaks, and how to choose a region.',
        'What is the difference between an Azure region and an availability zone, and when do you use each?',
        body, CR + ['<span class="cur">Regions &amp; Availability Zones</span>'], '', search_title='Regions & Availability Zones')
