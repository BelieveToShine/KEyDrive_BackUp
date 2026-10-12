from kit import *
from p_common import CR

DOCS_ASG = ('Amazon EC2 Auto Scaling user guide', 'https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html')
DOCS_DYN = ('Dynamic scaling for EC2 Auto Scaling', 'https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scale-based-on-demand.html')
DOCS_WARM = ('Default instance warmup', 'https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-default-instance-warmup.html')
DOCS_REL = ('Well-Architected Reliability Pillar', 'https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html')
DOCS_DR = ('Disaster recovery of workloads on AWS', 'https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html')
DOCS_OPT = ('Disaster recovery options in the cloud', 'https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html')
DOCS_BK = ('AWS Backup', 'https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html')
DOCS_DRS = ('AWS Elastic Disaster Recovery', 'https://docs.aws.amazon.com/drs/latest/userguide/what-is-drs.html')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official AWS docs.'

def d_ladder():
    d = Diagram('sc1', 640, 300, 'Three sizes of failure — one server, one zone, one Region — and the protection that covers each')
    d.text(130, 22, 'WHAT FAILS', size=9.5, mono=True)
    d.text(510, 22, 'WHAT KEEPS YOU UP', size=9.5, mono=True)
    rows = [
      ('🖥️ One server','a crash or a bad update','Several copies','in an Auto Scaling group'),
      ('🏢 One Availability Zone','power, cooling or network','Copies in several zones','one in each zone'),
      ('🌍 A whole Region','every zone in the area','A second Region','with backups and failover'),
    ]
    for i,(a,b,c,e) in enumerate(rows):
        y = 40 + i*86
        d.box(20, y, 220, 62, [(a,'t'),(b,'s')], 'rose')
        d.box(400, y, 220, 62, [(c,'t'),(e,'s')], 'emerald')
        d.arrow([(240,y+31),(400,y+31)], 'emerald', label='is covered by', at=(320,y+31))
    return d

def d_policies():
    d = Diagram('sc2', 640, 290, 'Auto Scaling watches a metric and a policy adds or removes instances; target tracking keeps a metric near a target value')
    d.box(10, 50, 130, 64, [('📊 Metric','t'),('CPU, requests','s')], 'cyan')
    d.box(255, 50, 130, 64, [('📏 Scaling policy','t'),('target tracking','s')], 'amber')
    d.box(490, 50, 140, 64, [('🖥️ Group','t'),('how many copies','s')], 'emerald')
    d.arrow([(140,82),(255,82)], 'cyan', label='watched', at=(197,82))
    d.arrow([(385,82),(490,82)], 'amber', label='scales', at=(437,82))
    d.arrow([(560,114),(560,164),(75,164),(75,114)], 'n', label='load per copy changes the metric', at=(320,164))
    d.text(320, 214, 'Target tracking: pick a target (say, average CPU) and AWS adds or removes copies to hold it.', size=9.5)
    d.text(320, 234, 'Warm-up: a new instance is ignored in the metrics until it is ready to serve.', size=9.5)
    d.text(320, 266, 'AWS recommends target tracking over simple scaling and cooldowns.', size=9.5, weight=700)
    return d

def d_updown():
    d = Diagram('sc3', 640, 250, 'Scale up makes one machine bigger; scale out adds more copies of it')
    d.zone(10, 8, 305, 234, 'amber', 'SCALE UP · a bigger machine')
    d.box(30, 84, 80, 56, [('🖥️ Small','t'),('one server','s')], 'n')
    d.box(190, 64, 100, 96, [('🖥️ Big','t'),('one server','s')], 'amber')
    d.arrow([(110,112),(190,112)], 'amber', label='resize', at=(150,112))
    d.text(162, 196, 'Still one machine: it has a ceiling', size=9.5)
    d.text(162, 212, 'and is still one point of failure.', size=9.5)
    d.zone(325, 8, 305, 234, 'emerald', 'SCALE OUT · more copies')
    d.box(335, 84, 64, 56, [('🖥️ One','t'),('copy','s')], 'n')
    d.zone(470, 36, 150, 150, 'emerald', 'COPIES')
    for i in range(3):
        d.box(484, 62 + i*40, 122, 34, [(f'🖥️ Copy {i+1}','t')], 'emerald')
    d.arrow([(399,112),(470,112)], 'emerald', label='more', at=(435,112))
    d.text(477, 212, 'No single ceiling; one copy can fail', size=9.5)
    d.text(477, 228, 'while the others carry on.', size=9.5)
    return d

def build_scaling_resilience():
    body = ''
    body += see(figure(d_ladder(),
        'failures come in three sizes, and each needs its own protection. A <b>server</b> can crash — keep several copies in an Auto Scaling group. A whole <b>Availability Zone</b> can go dark — spread those copies across zones. '
        'A whole <b>Region</b> can go down — keep a second Region ready, with backups and a plan to fail over. The bigger the failure you survive, the more it costs, so you choose how far to go.'))
    body += one('Scaling adds copies when load grows. Resilience keeps the app running when a copy, a zone or a Region fails. They use the same trick: never rely on just one of anything.')
    body += why([
      'The last concept put a load balancer in front of several copies. Two questions follow at once. <b>How many copies do you need?</b> Too few and the app is slow at peak; too many and you pay for idle servers. <b>What if a copy — or a whole zone — fails?</b>',
      'AWS answers the first with <b>Auto Scaling</b>: add copies when load rises, remove them when it falls. It answers the second with <b>redundancy</b>: copies in several Availability Zones and, for the worst day, a second Region. AWS\'s reliability guidance is to plan recovery before the failure, not after.'])
    body += block('📏 Scale up or scale out?', figure(d_updown(),
        '<b>Scale up</b> (left) means a bigger machine: easy, but it has a ceiling and is still one point of failure. <b>Scale out</b> (right) means more copies behind a load balancer: no single ceiling, and one copy can fail while the rest carry on. '
        'Auto Scaling is <em>horizontal</em> — it adds and removes copies — so your app should be happy running as several identical copies.'), label_cls='see')
    body += block('🔁 How Auto Scaling decides', figure(d_policies(),
        'an <b>Auto Scaling group</b> keeps a set of copies, spread across zones. A <b>scaling policy</b> watches a metric and changes the group size. The simplest good choice is <b>target tracking</b>: you choose a target for a metric, such as average CPU, and AWS adds or removes copies to hold it. '
        '<b>Step scaling</b> fits metrics that do not move in proportion to capacity, and <b>scheduled scaling</b> handles a rush you know is coming. Set a default <b>instance warm-up</b> so brand-new copies are not counted before they are ready.'), label_cls='see')
    body += block('🧰 The tools', pick_cards([
      dict(icon='📈', name='EC2 Auto Scaling', tag='add and remove copies automatically', color='#34d399',
           use=['Traffic that rises and falls', 'Target tracking, step scaling or a schedule', 'Spread across zones; replaces unhealthy instances'],
           skip=['A single database server — it is not a pool of identical copies']),
      dict(icon='🏢', name='Multiple Availability Zones', tag='copies in separate zones', color='#a78bfa',
           use=['Survive the loss of one zone', 'Put each tier\'s copies in at least two zones'],
           skip=['Expecting zones to protect against deletion or corruption']),
      dict(icon='📦', name='Service-level scaling', tag='each service scales its own way', color='#22d3ee',
           use=['ECS services, DynamoDB capacity and Aurora readers have their own autoscaling', 'Lambda scales per event'],
           skip=['Assuming one setting scales everything']),
      dict(icon='🛟', name='A second Region', tag='for the biggest failures', color='#fbbf24',
           use=['The business cannot stop if a Region fails', 'Backups and failover for a real disaster'],
           skip=['The cost is not justified by the app → zones are often enough']),
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🎟️','Ticket sales open at noon','A huge spike, then quiet.','Scheduled scaling plus target tracking'),
      ('📬','A queue of jobs piles up','Workers should grow with the backlog.','Scale on queue depth'),
      ('🛍️','Weekend shopping peak','Traffic doubles on Saturday, drops Monday.','Target tracking with scale-in'),
      ('🏢','One Availability Zone loses power','Nobody wakes up at 3 AM.','Copies spread across zones'),
      ('🌪️','A whole Region is unavailable','Rare, but costly.','A second Region and a recovery plan'),
      ('🔌','A call to a dependency fails once','The next try would succeed.','Retry with back-off and jitter'),
    ]), label_cls='see')
    body += block('🔬 Go deeper', deep_cards([('Deep dive · Scaling &amp; Resilience', 'Disaster Recovery: RPO, RTO and the four strategies', 'What to do on the worst day: how much data you can lose, how long you can be down, and the four AWS strategies from backup and restore to multi-site active/active.', 'disaster-recovery.html')]), label_cls='next')
    body += zoom('Go one level deeper (60 seconds) — details that matter', '''      <p><b>Policy types.</b> AWS describes target tracking, step and simple scaling as dynamic scaling types, and strongly recommends target tracking where it fits. It recommends against simple scaling policies and scaling cooldowns in favour of target tracking or step scaling. Mixing target tracking and step policies on the same metric can conflict.</p>
      <p><b>Warm-up.</b> The default instance warm-up sets how long after an instance is in service it waits before contributing metrics, so scaling does not react to instances that are not yet serving. AWS strongly recommends configuring it; it is not set by default.</p>
      <p><b>Retry wisely.</b> Retrying a transient failure with growing waits and some random jitter stops clients from all retrying at once. Add a circuit breaker so a truly dead dependency is not hammered, and make operations idempotent.</p>
      <p><b>Zones are not backups.</b> Spreading copies across zones keeps the app up; it does not recover deleted or corrupted data. That is the job of replication and backup (see the deep dive).</p>''')
    body += recall([
      'Scale up = bigger machine (ceiling). Scale out = more copies (Auto Scaling works this way).',
      'Prefer target tracking: pick a metric target and AWS holds it. Step scaling for non-proportional metrics; scheduled scaling for known rushes.',
      'Configure the default instance warm-up; avoid simple scaling and cooldowns.',
      'Zones survive a zone failure; a second Region survives a Region failure. Zones do not replace backups.',
      'Retry with back-off and jitter, add a circuit breaker, make operations idempotent.'])
    body += saythis('"I design for failure at three sizes: a server, a zone and a Region. An Auto Scaling group spread across zones covers the first two, a second Region with backups covers the third. '
      'For load I use target tracking on a metric like CPU, scheduled scaling for known rushes and a configured warm-up. In code I retry with back-off and jitter, and keep operations idempotent."')
    body += trap([
      '<b>Autoscale only helps if the app runs as many copies.</b> If it keeps sessions or files on one server, a new copy will not know about them. Keep state outside the copies.',
      'Second trap: <b>"we are in two zones, so we have backups".</b> Zones keep the app running; they do not protect against deletion or corruption. Redundancy and backup are different things.'])
    body += confuse('📈 Scaling', 'Match the number of copies to the load, both ways. Mostly performance and cost.', '🛟 Resilience', 'Keep working when something fails. Mostly availability and recovery.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># target tracking: keep average CPU of the group near a target value</span>
aws autoscaling put-scaling-policy --auto-scaling-group-name shop-asg --policy-name cpu-target \\
    --policy-type TargetTrackingScaling --target-tracking-configuration file://target.json''',
      'Illustrative shape only — the group name is an example and target.json would hold the metric and target value you choose.'))
    body += next_box('You can now match capacity to load and survive failures. But even a fast app is slow if every request goes all the way to the database. Next: Caching &amp; Edge Delivery.', 'caching-edge.html', 'Caching &amp; Edge Delivery')
    body += fact_note(FOOT, [DOCS_ASG, DOCS_DYN, DOCS_WARM, DOCS_REL, DOCS_DR])
    return page('scaling-resilience', 'Scaling & Resilience', 'Concept 9 of 19 · ⚙️ Handling load',
        'Scaling adds copies when load grows; resilience keeps you running when something fails — <span class="grad-text">both come from never relying on just one of anything.</span>',
        'Auto Scaling, zones and Regions: how scaling decides, what each size of failure needs, and the coding habits that survive trouble.',
        'How do you scale an AWS app and keep it available when a server, a zone or a Region fails?',
        body, CR + ['<span class="cur">Scaling &amp; Resilience</span>'], '', search_title='Scaling & Resilience')

# ---------------------------------------------------------------- deep dive: disaster recovery
def d_rpo():
    d = Diagram('dr1', 640, 230, 'Timeline of a disaster: the last good copy, the outage, and being back online, with RPO and RTO as the two gaps')
    d.box(10, 40, 110, 60, [('💾 Last good','t'),('copy of data','s')], 'cyan')
    d.box(265, 40, 110, 60, [('💥 Outage','t'),('it all stops','s')], 'rose')
    d.box(520, 40, 110, 60, [('✅ Back online','t'),('running again','s')], 'emerald')
    d.arrow([(120,70),(265,70)], 'cyan', label='RPO: data lost', at=(192,70))
    d.arrow([(375,70),(520,70)], 'emerald', label='RTO: time down', at=(447,70))
    d.text(320, 150, 'RPO (recovery point objective): how much data you can afford to lose, measured in time.', size=9.5, weight=700)
    d.text(320, 170, 'RTO (recovery time objective): how long you can afford to be down.', size=9.5, weight=700)
    d.text(320, 200, 'The business sets both numbers. Your design and your budget must meet them.', size=9.5)
    return d

def d_four():
    d = Diagram('dr2', 640, 290, 'AWS four disaster recovery strategies from backup and restore to multi-site active/active, trading cost for faster recovery')
    boxes = [
      (10,  'cyan',    [('🧊 Backup','t'),('and restore','t'),('copy backups to','s'),('another Region;','s'),('build on demand','s')]),
      (168, 'violet',  [('💡 Pilot light','t'),('data always on,','s'),('compute off until','s'),('you need it','s')]),
      (326, 'amber',   [('🔥 Warm standby','t'),('a scaled-down','s'),('working copy that','s'),('can serve reduced','s'),('traffic','s')]),
      (484, 'emerald', [('⚡ Multi-site','t'),('active/active','t'),('all Regions','s'),('serve traffic','s')]),
    ]
    for x,col,lines in boxes: d.box(x, 30, 146, 140, lines, col)
    d.arrow([(83,170),(83,212),(557,212),(557,170)], 'n', label='faster recovery, higher cost', at=(320,212))
    d.text(320, 266, 'Pick the cheapest strategy that still meets your RPO and RTO.', size=9.5, weight=700)
    return d

def d_which():
    d = Diagram('dr3', 640, 276, 'What went wrong decides the tool: a server or Region outage uses Elastic Disaster Recovery, damaged data uses AWS Backup, a database uses its own replication')
    d.box(10, 20, 200, 62, [('🖥️ Servers are down','t'),('zone or Region outage','s')], 'rose')
    d.box(220, 20, 200, 62, [('🗑️ Data is damaged','t'),('deleted or ransomware','s')], 'rose')
    d.box(430, 20, 200, 62, [('🗄️ A database','t'),('has its own tools','s')], 'rose')
    d.box(10, 150, 200, 62, [('🔁 Elastic DR','t'),('replicates, then fails over','s')], 'emerald')
    d.box(220, 150, 200, 62, [('📦 AWS Backup','t'),('restores earlier copies','s')], 'cyan')
    d.box(430, 150, 200, 62, [('🧬 DB replication','t'),('replicas, global tables','s')], 'violet')
    d.arrow([(110,82),(110,150)], 'emerald', label='fail over with', at=(185,116))
    d.arrow([(320,82),(320,150)], 'cyan', label='restore with', at=(385,116))
    d.arrow([(530,82),(530,150)], 'violet', label='copy with', at=(590,116))
    d.text(320, 246, 'A replica copies mistakes; a backup lets you go back in time.', size=9.5, weight=700)
    return d

def build_disaster_recovery():
    body = ''
    body += see(figure(d_rpo(),
        'a disaster on a timeline. The <b>RPO</b> is the gap between the last good copy of your data and the outage — the data you would lose. The <b>RTO</b> is the gap between the outage and being back online — the time you would be down. '
        'Every strategy on this page is a way to make those two gaps small enough, at a price you can pay.'))
    body += one('Disaster recovery starts with two questions — how much data can we lose, and how long can we be down? — and then buys exactly that much protection, no more.')
    body += why([
      'Auto Scaling and zones keep the app running through everyday failures. They do <b>not</b> help if someone deletes the wrong data, ransomware encrypts it, or a whole Region is unavailable. For those days you need <b>copies of the data and a plan to run somewhere else</b>.',
      'The trap is buying too much or too little. RPO and RTO turn that argument into numbers the business can agree to. AWS then describes four strategies, in order of speed and cost.'])
    body += block('🎚️ The four strategies', figure(d_four(),
        'AWS names four strategies. <b>Backup and restore</b>: copy backups to another Region and build the environment when needed — cheapest, slowest. <b>Pilot light</b>: data is replicated and always on, but application servers are not running until you need them. '
        '<b>Warm standby</b>: a scaled-down but fully working copy always runs and can serve reduced traffic at once. <b>Multi-site active/active</b>: every Region serves traffic — fastest and costliest. '
        'All strategies need your data backed up in its Region, and those backups copied to the recovery Region.'), label_cls='see')
    body += block('🧭 Which tool for which problem', figure(d_which(),
        'start from what went wrong. Servers are down because of a zone or Region outage → <b>AWS Elastic Disaster Recovery</b> replicates them and lets you fail over. Data that is deleted, corrupted or encrypted → <b>AWS Backup</b>, because a replica would copy the damage too. '
        'A database → its <b>own replication</b> features (replicas, cross-Region options, global tables).'), label_cls='see')
    body += block('📊 Side by side', table(['','Protects against','Gives you','Not enough for'], [
      ['🔁 Elastic Disaster Recovery','Server or Region outage','Continuous replication and a recovery environment','Damaged or deleted data'],
      ['📦 AWS Backup','Deleted, corrupted or ransomware-hit data','Central scheduled backups and restore points','A fast failover on its own'],
      ['🧬 Database replication','A database server or Region failing','A live copy of the data elsewhere','Mistaken deletes — the replica copies them'],
      ['🌍 A second Region','A full Region outage','Somewhere else to run the app','Nothing, if data is not copied there too'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🧑‍💻','Someone deletes a customer table','A replica deletes it too. Go back before the mistake.','Backup (restore a point in time)'),
      ('🔐','Ransomware encrypts the files','Restore from a copy the attacker could not change.','Backup, kept separate'),
      ('🏗️','A Region is unavailable','The server-based app must run elsewhere.','Elastic Disaster Recovery and failover'),
      ('🧾','Payment system, almost no downtime allowed','Tiny RPO and RTO, and a budget.','Multi-site active/active'),
      ('📰','Internal tool, a day of downtime is fine','Low priority, low budget.','Backup and restore'),
      ('🧪','Nobody has ever tried the plan','Most failures hide in untested steps.','Run a recovery drill'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — what AWS says', '''      <p><b>Choose from your objectives.</b> AWS\'s Reliability Pillar says to use a defined recovery strategy that meets your recovery objectives. Published RTO and RPO ranges for each strategy differ slightly between AWS documents and are indicative targets, not guarantees, so this page quotes none of them.</p>
      <p><b>Pilot light vs warm standby.</b> The key difference: a pilot-light environment cannot process requests without additional action, while warm standby can handle reduced traffic immediately.</p>
      <p><b>Active/active still needs backups.</b> Data corruption can replicate everywhere, so a point-in-time backup is still needed, which means the recovery point is usually not exactly zero.</p>
      <p><b>Elastic Disaster Recovery</b> uses a pilot-light-style approach with continuous data replication; check its documentation for current targets. <b>AWS Backup</b> gives a central place to configure, schedule and monitor backups.</p>
      <p><b>Failover and failback.</b> Plan both: moving to the recovery Region, and moving back when the first Region has recovered. Define your environment as code (a later concept) and test the plan.</p>''')
    body += recall([
      'RPO = how much data you can lose. RTO = how long you can be down. The business sets them.',
      'Four AWS strategies: backup and restore → pilot light → warm standby → multi-site active/active (cheapest/slowest to costliest/fastest).',
      'Pilot light cannot serve requests without action; warm standby can serve reduced traffic immediately.',
      'Elastic Disaster Recovery = replicate and fail over servers. AWS Backup = restore earlier copies. Databases use their own replication.',
      'A replica copies mistakes; a backup lets you go back in time. Test the plan.'])
    body += saythis('"I start from RPO and RTO — how much data we can lose and how long we can be down — then pick the cheapest of AWS\'s four strategies that meets them: backup and restore, pilot light, warm standby or multi-site active/active. '
      'I use Elastic Disaster Recovery for servers, AWS Backup for damaged data, and database replication for databases, and I test the plan."')
    body += trap([
      '<b>A replica is not a backup.</b> If someone deletes a table, replication copies the deletion within moments. You need a restore point from before the mistake.',
      'Second trap: <b>backups only in the Region that failed.</b> Copy backups to the recovery Region, or you cannot restore when you need to.'])
    body += confuse('🔁 Failover', 'Move production traffic from the Region that is unavailable to the one that works.', '↩️ Failback', 'Move traffic back to the original Region once it has recovered.')
    body += next_box('That is disaster recovery. Back to Scaling &amp; Resilience for the big picture — and on to the next concept: Caching &amp; Edge Delivery.', 'scaling-resilience.html', 'Back to Scaling &amp; Resilience')
    body += fact_note(FOOT, [DOCS_DR, DOCS_OPT, DOCS_DRS, DOCS_BK, DOCS_REL])
    return page('disaster-recovery', 'Disaster Recovery', 'Deep dive · Scaling & Resilience · 🛟 Disaster recovery',
        'Disaster recovery starts with two numbers — <span class="grad-text">how much data you can lose, and how long you can be down.</span>',
        'RPO and RTO, AWS\'s four strategies, and when to use Elastic Disaster Recovery, AWS Backup or a database\'s own replication.',
        'What are RPO and RTO, and what are the AWS disaster recovery strategies?',
        body, CR + ['<a href="scaling-resilience.html">Scaling &amp; Resilience</a>', '<span class="cur">Disaster Recovery</span>'], '', search_title='Disaster Recovery')
