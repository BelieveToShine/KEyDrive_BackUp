from kit import *
from p_storage import CR

DOCS_AUTO = ('Autoscale overview (Azure Monitor)', 'https://learn.microsoft.com/en-us/azure/azure-monitor/autoscale/autoscale-overview')
DOCS_VMSS = ('Virtual Machine Scale Sets documentation', 'https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview')
DOCS_REL = ('Well-Architected: Reliability design principles', 'https://learn.microsoft.com/en-us/azure/well-architected/reliability/principles')
DOCS_TF = ('Well-Architected: handling transient faults', 'https://learn.microsoft.com/en-us/azure/well-architected/design-guides/handle-transient-faults')
DOCS_DR = ('Well-Architected: disaster recovery strategies', 'https://learn.microsoft.com/en-us/azure/well-architected/reliability/disaster-recovery')
DOCS_ASR = ('Azure Site Recovery documentation', 'https://learn.microsoft.com/en-us/azure/site-recovery/')
DOCS_BK = ('Azure Backup documentation', 'https://learn.microsoft.com/en-us/azure/backup/backup-overview')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official docs.'

def d_ladder():
    d = Diagram('sc1', 640, 300, 'Three sizes of failure — one server, one datacenter, one region — and the protection that covers each')
    d.text(130, 22, 'WHAT FAILS', size=9.5, mono=True)
    d.text(510, 22, 'WHAT KEEPS YOU UP', size=9.5, mono=True)
    rows = [
      ('🖥️ One server','a crash or a bad update','Several copies','behind a load balancer'),
      ('🏢 One datacenter','power, cooling or network','Copies in several zones','one in each datacenter'),
      ('🌍 A whole region','every zone in the area','A second region','with backups and failover'),
    ]
    for i,(a,b,c,e) in enumerate(rows):
        y = 40 + i*86
        d.box(20, y, 220, 62, [(a,'t'),(b,'s')], 'rose')
        d.box(400, y, 220, 62, [(c,'t'),(e,'s')], 'emerald')
        d.arrow([(240,y+31),(400,y+31)], 'emerald', label='is covered by', at=(320,y+31))
    return d

def d_updown():
    d = Diagram('sc2', 640, 250, 'Scale up makes one machine bigger; scale out adds more copies of it')
    d.zone(10, 8, 305, 234, 'amber', 'SCALE UP · a bigger machine')
    d.box(30, 84, 80, 56, [('🖥️ Small','t'),('one VM','s')], 'n')
    d.box(190, 64, 100, 96, [('🖥️ Big','t'),('one VM','s')], 'amber')
    d.arrow([(110,112),(190,112)], 'amber', label='resize', at=(150,112))
    d.text(162, 196, 'Still one machine: it has a ceiling', size=9.5)
    d.text(162, 212, 'and is still one point of failure.', size=9.5)
    d.zone(325, 8, 305, 234, 'emerald', 'SCALE OUT · more copies')
    d.box(335, 84, 64, 56, [('🖥️ VM','t'),('one copy','s')], 'n')
    d.zone(470, 36, 150, 150, 'emerald', 'COPIES')
    for i in range(3):
        d.box(484, 62 + i*40, 122, 34, [(f'🖥️ Copy {i+1}','t')], 'emerald')
    d.arrow([(399,112),(470,112)], 'emerald', label='more', at=(435,112))
    d.text(477, 212, 'No single ceiling, and one copy can fail', size=9.5)
    d.text(477, 228, 'while the others carry on.', size=9.5)
    return d

def d_autoscale():
    d = Diagram('sc3', 640, 310, 'Autoscale loop: a metric feeds the rules, the rules add or remove instances, and the load per instance changes the metric')
    d.box(20, 50, 130, 64, [('📊 Metric','t'),('CPU, queue length','s')], 'cyan')
    d.box(255, 50, 130, 64, [('📏 Rules','t'),('scale out · scale in','s')], 'amber')
    d.box(490, 50, 130, 64, [('🖥️ Instances','t'),('how many copies','s')], 'emerald')
    d.arrow([(150,82),(255,82)], 'cyan', label='time window', at=(202,82))
    d.arrow([(385,82),(490,82)], 'amber', label='scales', at=(437,82))
    d.arrow([(555,114),(555,164),(85,164),(85,114)], 'n', label='load per copy changes the metric', at=(320,164))
    d.text(320, 218, '⬆️ Scale out when the metric is above the HIGH line', color='emerald', size=10.5, weight=700)
    d.text(320, 242, '⬇️ Scale in when the metric is below the LOW line', color='cyan', size=10.5, weight=700)
    d.text(320, 284, 'Keep a gap between the two lines, or the system flaps: out, in, out, in.', size=9.5, weight=700)
    return d

def build_scaling_resilience():
    body = ''
    body += see(figure(d_ladder(),
        'failures come in three sizes, and each one needs its own protection. A <b>server</b> can crash — keep several copies behind a load balancer. A whole <b>datacenter</b> can go dark — spread those copies across availability zones. '
        'A whole <b>region</b> can go down — keep a second region ready, with backups and a plan to fail over. The bigger the failure you survive, the more it costs, so you choose how far to go.'))
    body += one('Scaling adds copies when load grows. Resilience keeps the app running when a copy, a datacenter or a region fails. They use the same trick: never rely on just one of anything.')
    body += why([
      'The last concept put a load balancer in front of several copies of your app. Two questions follow at once. <b>How many copies do you need?</b> Too few and the app is slow at peak; too many and you pay for idle machines. <b>What if a copy — or the whole building — fails?</b>',
      'Azure answers the first with <b>autoscale</b>: add copies when load rises, remove them when it falls. It answers the second with <b>redundancy</b>: copies in separate zones and, for the worst day, a second region. Microsoft\'s reliability guidance says it plainly: use layers of redundancy so there is no single point of failure, and start by working out how each part can fail.'])
    body += block('📏 Scale up or scale out?', figure(d_updown(),
        '<b>Scale up</b> (left) means a bigger machine: easy, but it has a ceiling and is still one point of failure. <b>Scale out</b> (right) means more copies behind a load balancer: no single ceiling, and one copy can fail while the rest carry on. '
        'Autoscale in Azure is <em>horizontal</em> — it adds and removes copies — which is why your app should be happy running as several identical copies.'), label_cls='see')
    body += block('🔁 How autoscale decides', figure(d_autoscale(),
        'autoscale watches a <b>metric</b> such as CPU or queue length, looks at it over a <b>time window</b> (so one short spike does not trigger it), and follows your <b>rules</b> to add or remove instances. Or you can scale on a <b>schedule</b>, for a rush you know is coming. '
        'Always write a scale-in rule next to each scale-out rule, and keep a gap between the two thresholds — otherwise the system keeps adding and removing copies, which is called <em>flapping</em>.'), label_cls='see')
    body += block('🧰 The tools', pick_cards([
      dict(icon='📈', name='Autoscale', tag='add and remove copies automatically', color='#34d399',
           use=['Traffic that rises and falls', 'Metric rules (CPU, queue length, memory) or a schedule', 'App Service, scale sets and Container Apps each have their own way to scale'],
           skip=['A single database server — it is not a pool of identical copies']),
      dict(icon='🧱', name='Virtual Machine Scale Sets', tag='a group of load-balanced VMs', color='#22d3ee',
           use=['Many identical VMs managed as one group', 'The group should autoscale', 'Microsoft recommends the Flexible orchestration mode'],
           skip=['A web app that App Service can host for you with less to manage']),
      dict(icon='🏢', name='Availability zones', tag='copies in separate datacenters', color='#a78bfa',
           use=['Survive the loss of one datacenter', 'Spread VMs or use zone-redundant services'],
           skip=['Do not expect data to copy itself — spreading VMs across zones does not replicate your data']),
      dict(icon='🛟', name='A second region', tag='for the biggest failures', color='#fbbf24',
           use=['The business cannot stop if a whole region fails', 'Backups and failover for a real disaster'],
           skip=['The cost is not justified by the app → zones are often enough']),
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🎟️','Ticket sales open at noon','A huge spike, then quiet. Add copies before it starts.','Scale on a schedule, plus metric rules'),
      ('📬','A queue of jobs piles up','Workers should grow with the backlog and shrink when it clears.','Scale on queue length'),
      ('🛍️','Weekend shopping peak','Traffic doubles every Saturday and drops on Monday.','Autoscale with a scale-in rule'),
      ('🏢','One datacenter loses power','The site must stay up with no one waking up.','Copies spread across zones'),
      ('🌪️','A whole region is unavailable','Rare, but the business cannot be offline for long.','A second region and a failover plan'),
      ('🔌','A call to a dependency fails once','The next try would succeed.','Retry with a growing delay'),
    ]), label_cls='see')
    body += block('🔬 Go deeper', deep_cards([('Deep dive · Scaling &amp; Resilience', 'Disaster Recovery: RPO, RTO and backups', 'What to do on the worst day: how much data you can lose, how long you can be down, and when to use Backup, Site Recovery or a second region.', 'disaster-recovery.html')]), label_cls='next')
    body += zoom('Go one level deeper (60 seconds) — build the app so it survives failure', '''      <p><b>Retry, but wisely.</b> A <i>transient fault</i> is a short failure that fixes itself, so trying again after a short wait often works. Microsoft recommends exponential back-off (wait longer each time) plus a little random jitter, so thousands of clients do not all retry at the same instant.</p>
      <p><b>Add a circuit breaker.</b> If a dependency is really down, endless retries make things worse. A circuit breaker stops calling it for a while and lets it recover.</p>
      <p><b>Make health checks honest.</b> A health endpoint should check what the app really needs — the database, the cache, the queue — not just "the process is running".</p>
      <p><b>Make work safe to repeat.</b> If a function can be retried, design it to be <i>idempotent</i>: doing it twice has the same result as doing it once.</p>
      <p><b>Zones are not backups.</b> Spreading VMs across zones protects against a datacenter failure, but it does not copy your data and it does not recover from a deletion. That is the job of replication and backup (see the deep dive).</p>''')
    body += recall([
      'Scale up = bigger machine (has a ceiling). Scale out = more copies (autoscale works this way).',
      'Autoscale uses a metric or a schedule, a time window, and rules. Pair every scale-out rule with a scale-in rule and keep a gap between thresholds to avoid flapping.',
      'Scale sets run a group of load-balanced VMs that can autoscale; Flexible mode is the recommended one.',
      'Zones survive a datacenter failure; a second region survives a regional one. Zones do not replicate data for you.',
      'Retry with exponential back-off and jitter, add a circuit breaker, and make operations idempotent.'])
    body += saythis('"I design for failure at three sizes: a server, a datacenter and a region. Several copies behind a load balancer cover a server, zones cover a datacenter, and a second region with backups covers a region. '
      'For load I scale out with autoscale rules on a metric or a schedule, always with a scale-in rule and a gap between thresholds so it does not flap. In code I use retries with back-off and jitter, a circuit breaker, and idempotent operations."')
    body += trap([
      '<b>Autoscale only helps if the app can run as many copies.</b> If it keeps session data or files on one server, a new copy will not know about them. Keep state outside the copies (a database, a cache, storage).',
      'Second trap: <b>"we are in two zones, so we have backups".</b> Zones keep the app running; they do not protect you from someone deleting data or from corruption. Redundancy and backup are different things.'])
    body += confuse('📈 Scaling', 'Match the number of copies to the load, in both directions. Mostly about performance and cost.', '🛟 Resilience', 'Keep working when something fails. Mostly about availability and recovery.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># add an autoscale rule: more copies when average CPU is high (pair it with a scale-in rule!)</span>
az monitor autoscale rule create --resource-group rg-shop-prod --autoscale-name as-shop \\
    --condition "Percentage CPU > 70 avg 10m" --scale out 1''',
      'Illustrative shape only — the number and thresholds are examples, a real setup also needs the scale-in rule, and flags can change.'))
    body += next_box('You now know how to match capacity to load and survive failures. But even a fast app is slow if every request goes all the way to the database. Next: Caching &amp; Edge Delivery.', 'caching-edge.html', 'Caching &amp; Edge Delivery')
    body += fact_note(FOOT, [DOCS_AUTO, DOCS_VMSS, DOCS_REL, DOCS_TF, DOCS_DR])
    return page('scaling-resilience', 'Scaling & Resilience', 'Concept 9 of 19 · ⚙️ Handling load',
        'Scaling adds copies when load grows; resilience keeps you running when something fails — <span class="grad-text">both come from never relying on just one of anything.</span>',
        'Learn how autoscale decides, how zones and regions protect you at different sizes of failure, and the coding habits that make an app survive trouble.',
        'How do you scale an Azure app and keep it available when a server, a datacenter or a region fails?',
        body, CR + ['<span class="cur">Scaling &amp; Resilience</span>'], '', search_title='Scaling & Resilience')

# ---------------------------------------------------------------- deep dive: disaster recovery
def d_rpo():
    d = Diagram('sc4', 640, 230, 'Timeline of a disaster: the last good copy, the outage, and being back online, with RPO and RTO as the two gaps')
    d.box(10, 40, 110, 60, [('💾 Last good','t'),('copy of data','s')], 'cyan')
    d.box(265, 40, 110, 60, [('💥 Outage','t'),('it all stops','s')], 'rose')
    d.box(520, 40, 110, 60, [('✅ Back online','t'),('running again','s')], 'emerald')
    d.arrow([(120,70),(265,70)], 'cyan', label='RPO: data lost', at=(192,70))
    d.arrow([(375,70),(520,70)], 'emerald', label='RTO: time down', at=(447,70))
    d.text(320, 150, 'RPO (recovery point objective): how much data you can afford to lose, measured in time.', size=9.5, weight=700)
    d.text(320, 170, 'RTO (recovery time objective): how long you can afford to be down.', size=9.5, weight=700)
    d.text(320, 200, 'The business sets both numbers. Your design and your budget must meet them.', size=9.5)
    return d

def d_patterns():
    d = Diagram('sc5', 640, 276, 'Three multi-region patterns from cold standby to active-active, trading cost for faster recovery')
    d.box(10, 34, 200, 150, [('🧊 Cold standby','t'),('little or nothing runs','s'),('in the second region','s'),('you deploy after a disaster','s'),('cheapest · slowest','b')], 'cyan')
    d.box(220, 34, 200, 150, [('🔥 Warm standby','t'),('a small copy already runs','s'),('and scales up on failover','s'),('a balance of cost and speed','s'),('faster than cold','b')], 'amber')
    d.box(430, 34, 200, 150, [('⚡ Active-active','t'),('both regions serve users','s'),('one carries on if the other fails','s'),('roughly doubles the spend','s'),('fastest · costliest','b')], 'emerald')
    d.arrow([(110,184),(110,214),(530,214),(530,184)], 'n', label='faster recovery, higher cost', at=(320,214))
    d.text(320, 256, 'Pick the cheapest pattern that still meets the RPO and RTO.', size=9.5, weight=700)
    return d

def d_which():
    d = Diagram('sc6', 640, 276, 'What went wrong decides the tool: a VM outage uses Site Recovery, damaged data uses Backup, a database uses its own replication')
    d.box(10, 20, 200, 62, [('🖥️ A VM is unavailable','t'),('zone or region outage','s')], 'rose')
    d.box(220, 20, 200, 62, [('🗑️ Data is damaged','t'),('deleted or ransomware','s')], 'rose')
    d.box(430, 20, 200, 62, [('🗄️ A database','t'),('has its own tools','s')], 'rose')
    d.box(10, 150, 200, 62, [('🔁 Site Recovery','t'),('replicates and fails over','s')], 'emerald')
    d.box(220, 150, 200, 62, [('📦 Azure Backup','t'),('restores earlier copies','s')], 'cyan')
    d.box(430, 150, 200, 62, [('🧬 Database replicas','t'),('built-in replication','s')], 'violet')
    d.arrow([(110,82),(110,150)], 'emerald', label='fail over with', at=(185,116))
    d.arrow([(320,82),(320,150)], 'cyan', label='restore with', at=(385,116))
    d.arrow([(530,82),(530,150)], 'violet', label='copy with', at=(590,116))
    d.text(320, 246, 'Do not use Site Recovery for databases — use the database\'s own replication.', size=9.5, weight=700)
    return d

def build_disaster_recovery():
    body = ''
    body += see(figure(d_rpo(),
        'a disaster on a timeline. The <b>RPO</b> is the gap between the last good copy of your data and the outage — the data you would lose. The <b>RTO</b> is the gap between the outage and being back online — the time you would be down. '
        'Every disaster-recovery choice on this page is a way to make those two gaps small enough, at a price you can pay.'))
    body += one('Disaster recovery starts with two questions — how much data can we lose, and how long can we be down? — and then buys exactly that much protection, no more.')
    body += why([
      'Autoscale and zones keep the app running through everyday failures. They do <b>not</b> help if someone deletes the wrong data, ransomware encrypts it, or a whole region is unavailable. For those days you need <b>copies of the data and a plan to run somewhere else</b>.',
      'The trap is buying too much or too little. Protection that survives anything costs a fortune; protection that is too cheap fails on the day you need it. RPO and RTO turn that argument into numbers the business can agree to.'])
    body += block('🎚️ Choose a pattern', figure(d_patterns(),
        'Microsoft describes three ways to run in more than one region. <b>Cold standby</b> costs the least but needs a full deployment after a disaster, so recovery is slowest. <b>Warm standby</b> keeps a small copy running and scales it up on failover — a balance. '
        '<b>Active-active</b> serves users from both regions, so a failure causes little or no interruption, but it roughly doubles the spend. Tight RPO and RTO push you right; a small budget pushes you left.'), label_cls='see')
    body += block('🧭 Which tool for which problem', figure(d_which(),
        'start from what went wrong. A VM that is unavailable because of a zone or region outage → <b>Azure Site Recovery</b> replicates it and lets you fail over. Data that is deleted, corrupted or encrypted → <b>Azure Backup</b>, because a replica would copy the damage too. '
        'A database → use its <b>own replication</b> features, and not Site Recovery.'), label_cls='see')
    body += block('📊 Side by side', table(['','Protects against','Gives you','Not enough for'], [
      ['🔁 Site Recovery','Zone or region outage of VMs','Replication and failover of VMs','Damaged or deleted data; databases'],
      ['📦 Azure Backup','Deleted, corrupted or ransomware-hit data','Restore points you can go back to','A fast failover on its own'],
      ['🧬 Database replication','A database server or region failing','A live copy of the data elsewhere','Mistaken deletes — the replica copies them'],
      ['🌍 A second region','A full regional outage','Somewhere else to run the app','Nothing, if data is not copied there too'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🧑‍💻','Someone deletes a customer table','A replica would delete it too. Go back to a point before the mistake.','Backup (restore)'),
      ('🔐','Ransomware encrypts the files','Restore from a copy the attacker could not change.','Backup with protected vaults'),
      ('🏗️','A region is unavailable','The VM-based app must run elsewhere.','Site Recovery and failover'),
      ('🧾','Payment system, almost no downtime allowed','Tiny RPO and RTO. The budget exists.','Active-active'),
      ('📰','Internal tool, a day of downtime is fine','Low priority and a low budget.','Cold standby plus backups'),
      ('🧪','Nobody has ever tried the plan','Most failures hide in untested steps.','Run a disaster-recovery drill'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — failover, failback and backups done well', '''      <p><b>Failover</b> moves production traffic from a region that is unavailable to one that works. <b>Failback</b> moves it back when the first region has recovered. Plan both.</p>
      <p><b>Keep backups separate from what they protect.</b> Store them somewhere an attacker or a regional failure cannot reach with the same stroke — typically in another region. Azure Backup offers soft delete (you can recover deleted backups for a period you set), immutable vaults that block deleting recovery points, and Cross Region Restore.</p>
      <p><b>Make the second region easy to build.</b> Define your environment as code (a later concept in this journey) so you can create it quickly, and keep identity and settings in step between regions.</p>
      <p><b>Test it.</b> Microsoft recommends regular drills, because they find hidden dependencies on one region that nobody remembered.</p>''')
    body += recall([
      'RPO = how much data you can lose. RTO = how long you can be down. The business sets them.',
      'Cold standby (cheapest, slowest) → warm standby (a balance) → active-active (fastest, costliest).',
      'Site Recovery = replicate and fail over VMs. Backup = restore earlier copies after damage. Databases use their own replication.',
      'A replica copies mistakes; a backup lets you go back in time. Keep backups separate, often in another region.',
      'A plan that was never tested is a guess — run drills.'])
    body += saythis('"I start from the recovery objectives: RPO is how much data we can lose, RTO is how long we can be down. Then I choose the cheapest pattern that meets them — cold standby, warm standby or active-active. '
      'For VMs I use Site Recovery to replicate and fail over, for damaged data I use Backup and keep it separate, and for databases I use their own replication. And I test the plan with drills."')
    body += trap([
      '<b>A replica is not a backup.</b> If someone deletes a table, replication copies the deletion within moments. You need a restore point from before the mistake.',
      'Second trap: <b>using Site Recovery for a database.</b> Microsoft\'s guidance is to use the database\'s native replication instead.'])
    body += confuse('🔁 Failover', 'Shift production traffic from the region that is unavailable to the one that works.', '↩️ Failback', 'Shift traffic back to the original region once it has recovered.')
    body += next_box('That is disaster recovery. Back to Scaling &amp; Resilience for the big picture — and on to the next concept: Caching &amp; Edge Delivery.', 'scaling-resilience.html', 'Back to Scaling &amp; Resilience')
    body += fact_note(FOOT, [DOCS_DR, DOCS_ASR, DOCS_BK, DOCS_REL])
    return page('disaster-recovery', 'Disaster Recovery', 'Deep dive · Scaling & Resilience · 🛟 Disaster recovery',
        'Disaster recovery starts with two numbers — <span class="grad-text">how much data you can lose, and how long you can be down.</span>',
        'RPO and RTO, the three multi-region patterns, and when to use Site Recovery, Azure Backup or a database\'s own replication.',
        'What are RPO and RTO, and how would you design disaster recovery on Azure?',
        body, CR + ['<a href="scaling-resilience.html">Scaling &amp; Resilience</a>', '<span class="cur">Disaster Recovery</span>'], '', search_title='Disaster Recovery')
