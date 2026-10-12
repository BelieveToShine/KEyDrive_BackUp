from kit import *
from p_common import CR

DOCS_RDS = ('Amazon RDS documentation', 'https://docs.aws.amazon.com/rds/')
DOCS_AUR = ('Amazon Aurora user guide', 'https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html')
DOCS_DDB = ('Amazon DynamoDB developer guide', 'https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html')
DOCS_MAZ = ('Multi-AZ DB instance deployments for Amazon RDS', 'https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html')
DOCS_RR = ('Working with DB instance read replicas', 'https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html')
DOCS_PK = ('Partition key design in DynamoDB', 'https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official AWS docs.'

def d_two():
    d = Diagram('db1', 640, 300, 'Relational databases on RDS and Aurora store tables you can join and query; DynamoDB stores items looked up by key at huge scale')
    d.box(10, 40, 290, 150, [('🛢️ RDS and Aurora','t'),('relational · tables and rows','s'),('SQL · joins · transactions','s'),('you design the schema first','s'),('scale up, add read copies','s')], 'violet')
    d.box(340, 40, 290, 150, [('⚡ DynamoDB','t'),('NoSQL · items by key','s'),('single-digit-millisecond reads','s'),('you design around your queries','s'),('scales out by partitioning','s')], 'amber')
    d.arrow([(155,190),(155,232),(485,232),(485,190)], 'n', label='pick by how you query', at=(320,232))
    d.text(320, 280, 'Many real systems use both — each where it fits.', size=9.5, weight=700)
    return d

def d_choose():
    d = Diagram('db2', 640, 436, 'Decision tree: need joins and strong SQL use RDS or Aurora; need huge scale with known key lookups use DynamoDB; need a cache use ElastiCache')
    d.box(190, 8, 260, 34, [('🤔 What does your data need?','t')], 'cyan')
    qs = [
     ('🔗 Joins, ad-hoc SQL, transactions?', 'a shape that may change in unplanned ways', 'RDS or Aurora', 'relational engines', 'violet'),
     ('🔑 Known key lookups, huge scale?', 'lookups by key', 'DynamoDB', 'key-value / document', 'amber'),
     ('⚡ Repeated reads you want in memory?', 'a cache in front of a database', 'ElastiCache', 'see Caching', 'cyan'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 372
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 372, 330, 54, [('🤔 Still unsure?','t'),('start relational — SQL answers more questions','s')], 'emerald')
    return d

def d_ha():
    d = Diagram('db3', 640, 300, 'RDS Multi-AZ keeps a standby copy in another zone for failover, while read replicas serve extra reads but are for scaling, not failover')
    d.zone(10, 8, 305, 284, 'emerald', 'MULTI-AZ · for availability')
    d.box(24, 70, 100, 56, [('🛢️ Primary','t'),('zone a','s')], 'violet')
    d.box(200, 70, 100, 56, [('🛢️ Standby','t'),('zone b','s')], 'n')
    d.arrow([(124,98),(200,98)], 'emerald', label='sync', at=(162,98))
    d.text(162, 168, 'Updated synchronously.', size=9.5)
    d.text(162, 184, 'Takes over if the primary fails.', size=9.5)
    d.text(162, 208, 'The standby does not serve reads.', size=9.5, weight=700)
    d.zone(325, 8, 305, 284, 'cyan', 'READ REPLICAS · for scaling reads')
    d.box(339, 70, 100, 56, [('🛢️ Primary','t'),('takes writes','s')], 'violet')
    d.box(515, 70, 100, 56, [('📖 Replica','t'),('serves reads','s')], 'cyan')
    d.arrow([(439,98),(515,98)], 'cyan', label='async', at=(477,98))
    d.text(477, 168, 'Updated asynchronously.', size=9.5)
    d.text(477, 184, 'Add them yourself — RDS does not', size=9.5)
    d.text(477, 200, 'autoscale read replicas.', size=9.5)
    d.text(477, 224, 'Replicas are not automatic failover targets.', size=9.5, weight=700)
    return d

def build_databases():
    body = ''
    body += see(figure(d_two(),
        'two big families. <b>Relational</b> databases (<b>RDS</b> and <b>Aurora</b>) keep tables of rows you can join and query with SQL, and handle multi-row transactions. <b>DynamoDB</b> keeps <b>items</b> you look up by key and scales out by spreading them across partitions. '
        'You pick by <em>how you will query</em>, and many real systems use both.'))
    body += one('A database is where structured data gets queried and updated safely — pick relational when questions are open-ended, and DynamoDB when access patterns are known and scale is huge.')
    body += why([
      'Storage keeps files. But when you must <b>search</b>, <b>join</b>, <b>count</b> and <b>update many related records without corrupting them</b>, you need a database engine. Different engines make different trades between consistency, scale and query power.',
      'On AWS the first split is <b>relational (RDS, Aurora)</b> versus <b>NoSQL (DynamoDB)</b>. The skill is choosing from the questions you will ask — not from fashion. Then you add the availability tools: Multi-AZ, read replicas, and replication across Regions.'])
    body += block('🧰 The database options', pick_cards([
      dict(icon='🛢️', name='Amazon RDS', tag='managed relational databases', color='#a78bfa',
           use=['Standard engines such as MySQL, PostgreSQL, MariaDB, SQL Server and Oracle, with AWS handling provisioning, patching and backups', 'Joins, SQL and multi-row transactions', 'Multi-AZ for availability; read replicas for read scaling'],
           skip=['Huge key-value scale with no joins — DynamoDB may fit better']),
      dict(icon='🌌', name='Amazon Aurora', tag='AWS-built relational (MySQL/PostgreSQL compatible)', color='#22d3ee',
           use=['High-performance, highly available relational workloads', 'Storage replicated across three zones, independent of the number of compute instances', 'Up to many read-only replicas with failover priority'],
           skip=['A tiny, simple database where plain RDS is enough']),
      dict(icon='⚡', name='Amazon DynamoDB', tag='NoSQL key-value and document', color='#fbbf24',
           use=['Known access patterns by key, at very large scale', 'Steady low latency', 'On-demand or provisioned capacity'],
           skip=['Ad-hoc queries and joins you cannot predict']),
      dict(icon='🧠', name='ElastiCache and friends', tag='in-memory and specialised', color='#34d399',
           use=['A cache in front of a database (see Caching & Edge)', 'Other purpose-built databases exist for graphs, search and analytics'],
           skip=['Treating a cache as your only copy of the data']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'ask in order. <b>Joins, ad-hoc SQL, multi-row transactions?</b> A relational engine. <b>Known lookups by key, huge scale?</b> DynamoDB. <b>Repeated reads you want in memory?</b> A cache in front. '
        'If unsure, start relational — SQL can answer questions you have not thought of yet. DynamoDB asks you to know your questions first.'), label_cls='see')
    body += block('🛡️ Availability: Multi-AZ vs read replicas', figure(d_ha(),
        'these are different tools. <b>Multi-AZ</b> (left) keeps a synchronous standby in another Availability Zone and fails over if the primary fails; the standby cannot serve reads. <b>Read replicas</b> (right) are updated asynchronously and serve extra reads — they scale reads and are not automatic failover targets. '
        'A <b>Multi-AZ DB cluster</b> and <b>Aurora</b> combine the ideas, with readers that are also failover targets.'), label_cls='see')
    body += block('📊 Side by side', table(['','Model','Query power','Scales by','Think about'], [
      ['🛢️ RDS','Relational','SQL, joins, transactions','Bigger instance, read replicas','Pick the engine you know; patch windows'],
      ['🌌 Aurora','Relational','SQL, joins, transactions','Shared storage, many readers','Cost vs plain RDS'],
      ['⚡ DynamoDB','Key-value / document','By key and index; no joins','Partitioning, on-demand capacity','Design the partition key first'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🧾','Orders, customers and invoices that join together','Reports change every quarter.','RDS or Aurora'),
      ('🛒','Shopping carts at flash-sale scale','Always looked up by user ID.','DynamoDB'),
      ('🎮','Game leaderboard that must never slow down','Simple lookups, huge traffic.','DynamoDB'),
      ('🏦','Money moves between two accounts','Multi-row consistency.','A relational database with transactions'),
      ('📖','A report page slows the main database','Many read queries.','Read replicas (or Aurora readers)'),
      ('🆘','The primary database server fails','The app must keep going.','Multi-AZ'),
    ]), label_cls='see')
    body += block('🔬 Go deeper', deep_cards([('Deep dive · Databases', 'DynamoDB vs RDS and Aurora', 'The two you will be asked about most: strengths and watch-outs, the DynamoDB partition key, capacity modes, consistency choices, and when to use both.', 'dynamodb-vs-rds-aurora.html')]), label_cls='next')
    body += zoom('Go one level deeper (60 seconds) — managed does not mean unattended', '''      <p><b>Managed.</b> RDS handles provisioning, patching and backups. You still choose engine, size, network placement and parameters, and you still own the data design and the queries.</p>
      <p><b>Aurora storage</b> keeps six copies of your data across three Availability Zones, and this does not depend on how many compute instances you run. Aurora can tolerate the loss of copies without losing write availability.</p>
      <p><b>Put databases in private subnets</b> (concept 4), use IAM and secrets (concepts 3 and 15) and back them up (concept 9).</p>''')
    body += recall([
      'Relational (RDS, Aurora): tables, SQL, joins, transactions. DynamoDB: items by key, scales out by partition.',
      'Pick by how you query; start relational when unsure.',
      'Multi-AZ = synchronous standby for failover, standby does not serve reads. Read replicas = asynchronous, scale reads, not automatic failover targets.',
      'Aurora storage spans three AZs with six copies, independent of instance count.',
      'Many systems use both a relational database and DynamoDB.'])
    body += saythis('"I choose a database from the questions I will ask. Joins, ad-hoc SQL and multi-row transactions point to RDS or Aurora; known key lookups at huge scale point to DynamoDB. '
      'For availability I use Multi-AZ, and read replicas only for scaling reads — they are not failover targets. Aurora spreads storage across three zones. Many real systems use both."')
    body += trap([
      '<b>Using a read replica as your high-availability plan.</b> It is asynchronous and not an automatic failover target on standard RDS. Use Multi-AZ for failover.',
      'Second trap: <b>choosing DynamoDB because it "scales" and then needing joins.</b> Without known access patterns you will fight the model. Decide your queries first.'])
    body += confuse('🛢️ Relational (RDS / Aurora)', 'Design the tables, then ask any question with SQL. Great when questions change.', '⚡ DynamoDB', 'Design for the questions first, then get predictable speed at huge scale.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># create a small PostgreSQL database on RDS, with a standby in another zone</span>
aws rds create-db-instance --db-instance-identifier shop-db --engine postgres \\
    --db-instance-class db.t3.micro --allocated-storage 20 --multi-az \\
    --master-username admin --manage-master-user-password''',
      'Illustrative shape only — the size, storage and flags are examples, and real databases also set a subnet group, security groups, backups and encryption.'))
    body += next_box('One database plus one app server is a working instance — but one instance is a single point of failure and a throughput ceiling. Next: spreading traffic across many with Load Balancing &amp; Traffic Routing.', 'load-balancing.html', 'Load Balancing &amp; Traffic Routing')
    body += fact_note(FOOT, [DOCS_RDS, DOCS_AUR, DOCS_DDB, DOCS_MAZ, DOCS_RR])
    return page('databases', 'Databases', 'Concept 7 of 19 · 🧱 Building blocks',
        'A database is where data is queried and updated safely — <span class="grad-text">pick by how you will ask questions, not by fashion.</span>',
        'RDS, Aurora and DynamoDB: relational versus NoSQL, Multi-AZ versus read replicas, and how to choose.',
        'When would you choose DynamoDB over RDS or Aurora?',
        body, CR + ['<span class="cur">Databases</span>'], '', search_title='Databases')

# ------------------------------------------------------- deep dive: DynamoDB vs RDS/Aurora
def d_key():
    d = Diagram('dd1', 640, 300, 'A good DynamoDB partition key has many distinct values so requests spread evenly; a low-variety key sends them all to one hot partition')
    d.zone(10, 8, 305, 284, 'emerald', 'GOOD KEY · many distinct values')
    d.box(24, 60, 90, 44, [('🔑 user_id','t')], 'emerald')
    for i in range(3):
        d.box(190, 44 + i*58, 110, 44, [(f'📦 Partition {i+1}','t')], 'n')
    d.arrow([(114,82),(150,82),(150,66),(190,66)], 'emerald')
    d.arrow([(114,82),(150,82),(150,124),(190,124)], 'emerald')
    d.arrow([(114,82),(150,82),(150,182),(190,182)], 'emerald', label='spread out', at=(150,150))
    d.text(162, 238, 'Load is even; no partition', size=9.5)
    d.text(162, 254, 'gets all the heat.', size=9.5, weight=700)
    d.zone(325, 8, 305, 284, 'rose', 'BAD KEY · few distinct values')
    d.box(339, 60, 90, 44, [('🏷️ status','t')], 'rose')
    d.box(515, 44, 100, 44, [('🔥 Hot','t'),('partition','s')], 'rose')
    d.box(515, 104, 100, 44, [('📦 Idle','t')], 'n')
    d.box(515, 164, 100, 44, [('📦 Idle','t')], 'n')
    d.arrow([(429,82),(515,66)], 'rose')
    d.text(477, 238, 'A few values take all traffic and', size=9.5)
    d.text(477, 254, 'throttle while others sit idle.', size=9.5, weight=700)
    return d

def d_both():
    d = Diagram('dd2', 640, 296, 'A typical system uses both: DynamoDB for fast key lookups like carts and sessions, and a relational database for orders and reports')
    d.box(10, 108, 110, 64, [('📱 App','t'),('your service','s')], 'n')
    d.box(250, 28, 160, 64, [('⚡ DynamoDB','t'),('carts, sessions','s')], 'amber')
    d.box(250, 196, 160, 64, [('🛢️ Aurora / RDS','t'),('orders, reports','s')], 'violet')
    d.arrow([(120,128),(185,128),(185,60),(250,60)], 'amber', label='by key', at=(185,94))
    d.arrow([(120,152),(185,152),(185,228),(250,228)], 'violet', label='SQL', at=(185,190))
    d.box(510, 108, 120, 64, [('📊 Reports','t'),('joins, totals','s')], 'cyan')
    d.arrow([(410,228),(570,228),(570,172)], 'cyan', label='queried by', at=(490,228))
    return d

def d_choose2():
    d = Diagram('dd3', 640, 346, 'Decision tree for the deep dive: unknown questions or joins mean relational; known key lookups at scale mean DynamoDB; a lot of both means use both')
    d.box(190, 8, 260, 34, [('🤔 Can you list your queries today?','t')], 'cyan')
    qs = [
     ('📋 Yes, and mostly lookups by key?', 'fixed access patterns, huge scale', 'DynamoDB', 'design the key first', 'amber'),
     ('🔗 No, or you need joins and reports?', 'questions will change', 'RDS or Aurora', 'SQL flexibility', 'violet'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 272
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 272, 330, 54, [('🤝 Both kinds of access?','t'),('use each where it fits','s')], 'emerald')
    return d

def build_dynamodb_vs_rds_aurora():
    body = ''
    body += see(figure(d_both(),
        'a typical system uses <b>both</b>. Carts and sessions are looked up by key, so they live in <b>DynamoDB</b>. Orders, invoices and the reports on them need joins, so they live in <b>Aurora or RDS</b>. The app talks to each in the way it is good at. This is called <em>polyglot persistence</em> — the right store for each job.'))
    body += one('DynamoDB and relational databases are not rivals — DynamoDB wins when you know your questions and need steady speed at scale; relational wins when your questions keep changing.')
    body += why([
      'The Databases page gave a rule of thumb. This page goes one level deeper on the pair you will be asked about most. They differ in how you <b>design</b> (tables first or queries first), how you <b>scale</b> (up and out with replicas, or out by partitioning) and what you give up.',
      'The single most important decision in DynamoDB is the <b>partition key</b>. A good one spreads load evenly. A poor one creates a hot partition and throttling. Understanding this one idea explains most of DynamoDB.'])
    body += block('⚖️ Strengths and watch-outs', proscons('🛢️ RDS and Aurora',
      ['SQL, joins and multi-row transactions', 'Open-ended questions: new reports need no redesign', 'Multi-AZ, read replicas and (Aurora) shared storage across three zones'],
      ['Scale mostly by a bigger instance and read replicas', 'You manage connections and schema changes', 'RDS does not autoscale read replicas — add them yourself'])
      + proscons('⚡ DynamoDB',
      ['Steady low latency at huge scale', 'On-demand mode or provisioned capacity; no servers to size', 'Replicates for resilience and can span Regions (global tables)'],
      ['No joins; ad-hoc queries are hard', 'You must design the keys and indexes around known queries', 'A poor partition key causes hot partitions and throttling']), label_cls='see')
    body += block('🔑 The partition key', figure(d_key(),
        'DynamoDB spreads items across <b>partitions</b> by their partition key. A key with <b>many distinct values</b> (such as a user ID) spreads requests evenly. A key with few values (such as a status) sends most traffic to a few partitions, which become <b>hot</b> and throttle while others sit idle. '
        'AWS advises choosing a high-cardinality, evenly used attribute; write sharding (adding a suffix) can help but makes reads harder because you must query every suffix.'), label_cls='see')
    body += block('🧭 Which one?', figure(d_choose2(),
        'start with a question: <b>can you list your queries today?</b> If yes, and they are mostly lookups by key at scale, design for DynamoDB. If not, or you need joins and reports, choose relational. If your system has both kinds of access, use both.'), label_cls='see')
    body += block('📊 Side by side', table(['','RDS / Aurora','DynamoDB'], [
      ['Model','Tables, rows, SQL','Items with keys; attributes'],
      ['Design starts from','The data and its relations','The queries you will run'],
      ['Joins and ad-hoc queries','Yes','No'],
      ['Scaling','Bigger instance, read replicas, Aurora storage','Partitioning; on-demand or provisioned capacity'],
      ['Consistency','Transactional (ACID)','Eventually consistent reads by default; strongly consistent reads available, at higher read cost'],
      ['Availability','Multi-AZ, replicas, Aurora across three zones','Replicated across zones; global tables for Regions'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🛒','Cart lookup by user ID at sale-time scale','Predictable key, huge bursts.','DynamoDB'),
      ('📈','Finance wants a new report every week','Questions keep changing.','RDS or Aurora'),
      ('🧾','Orders must join customers and products','Relational shape.','RDS or Aurora'),
      ('🪪','Session data with a short expiry','Key lookup, short life.','DynamoDB'),
      ('🧨','All writes use status = "ACTIVE" as the key','Three values only.','Redesign the key (hot partition)'),
      ('🤝','A shop with carts and orders','Two shapes of access.','Use both'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — capacity and consistency', '''      <p><b>Consistency.</b> A read unit covers one strongly consistent read per second, or two eventually consistent reads per second, for an item up to 4 KB. Eventually consistent reads cost half as much, which is why AWS suggests them as a quick fix for throttled key ranges when freshness allows.</p>
      <p><b>Capacity.</b> Each partition is designed for about 3,000 read units and 1,000 write units per second; table throughput is limited by provisioned capacity or, in on-demand mode, by table-level limits. Adaptive capacity and automatic partition splitting often help hot partitions.</p>
      <p><b>Indexes.</b> Global secondary indexes can have their own key distribution; low-variety index keys commonly cause write throttling.</p>
      <p><b>Relational scale.</b> Read replicas are updated asynchronously; Multi-AZ gives a synchronous standby for failover; Aurora readers use asynchronous replication with failover priorities.</p>''')
    body += recall([
      'DynamoDB: design for your queries; partition key with many distinct values; hot partitions throttle.',
      'Relational: design for the data, ask any question later; Multi-AZ for failover, replicas for reads.',
      'DynamoDB reads are eventually consistent by default; strongly consistent reads cost double.',
      'Write sharding spreads hot keys but complicates reads.',
      'Use both when a system has key lookups and relational reporting.'])
    body += saythis('"I choose DynamoDB when I know my access patterns and need steady speed at scale, and I spend my design effort on the partition key — many distinct values, evenly used — to avoid hot partitions. '
      'I choose RDS or Aurora when I need joins, transactions and questions that will change. Many systems use both, each for what it does best."')
    body += trap([
      '<b>A low-variety partition key.</b> Keys like a status or a date bucket that everyone writes to today create a hot partition; throughput that looked ample is wasted.',
      'Second trap: <b>using DynamoDB like a relational database.</b> If you keep wishing for joins, the access patterns were not known — choose relational.'])
    body += confuse('🛢️ Aurora', 'A relational engine with shared storage across three zones and many read replicas.', '⚡ DynamoDB', 'A key-value / document database that scales by partitioning, designed around known queries.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># read one item by its key</span>
aws dynamodb get-item --table-name Carts --key '{"user_id": {"S": "u-1001"}}\'''',
      'Illustrative shape only — the table name, key and value are examples; add --consistent-read for a strongly consistent read.'))
    body += next_box('That is DynamoDB versus relational. Back to the Databases page for the big picture — and on to the next concept: Load Balancing &amp; Traffic Routing.', 'databases.html', 'Back to Databases')
    body += fact_note(FOOT, [DOCS_DDB, DOCS_PK, DOCS_RDS, DOCS_AUR])
    return page('dynamodb-vs-rds-aurora', 'DynamoDB vs RDS and Aurora', 'Deep dive · Databases · ⚖️ Choosing',
        'DynamoDB and relational databases are not rivals — <span class="grad-text">the difference is whether you know your questions up front.</span>',
        'Strengths and watch-outs of each, the DynamoDB partition key, consistency and capacity, and when to use both.',
        'When would you pick DynamoDB, and when RDS or Aurora?',
        body, CR + ['<a href="databases.html">Databases</a>', '<span class="cur">DynamoDB vs RDS and Aurora</span>'], '', search_title='DynamoDB vs RDS and Aurora')
