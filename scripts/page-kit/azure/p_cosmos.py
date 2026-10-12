from kit import *
from p_storage import CR
from p_db import DOCS_SQL, DOCS_COS, DOCS_ARCH

def d_shapes():
    d = Diagram('cs1', 640, 336, 'The same order stored two ways: three related tables in Azure SQL, one JSON item in Cosmos DB')
    d.zone(10, 8, 305, 320, 'violet', 'AZURE SQL · related tables')
    d.box(30, 40, 120, 60, [('👤 Customers','t'),('Id · Name','s')], 'violet')
    d.box(30, 140, 120, 60, [('🧾 Orders','t'),('Id · CustomerId','s')], 'violet')
    d.box(30, 240, 120, 60, [('📦 OrderItems','t'),('OrderId · Product','s')], 'violet')
    d.arrow([(90,140),(90,100)], 'violet', label='FK: CustomerId', at=(210,120))
    d.arrow([(90,240),(90,200)], 'violet', label='FK: OrderId', at=(204,220))
    d.text(172, 174, 'To read one order,', anchor='start', size=9.5)
    d.text(172, 190, 'JOIN the tables.', anchor='start', size=9.5)
    d.zone(325, 8, 305, 320, 'cyan', 'COSMOS DB · one JSON item')
    d.code_box(345, 40, 265, 164, [
        (0,'{','') , (12,'"id": "order-1001",',''), (12,'"customerId": "c-42",','k'),
        (12,'"customer": { "name": "Asha" },',''), (12,'"items": [',''),
        (24,'{ "product": "Shoes", "qty": 1 },',''), (24,'{ "product": "Socks", "qty": 2 }',''),
        (12,'],',''), (12,'"total": 59.0',''), (0,'}','')], 'cyan')
    d.text(480, 234, 'Everything about the order is stored together,', size=9.5)
    d.text(480, 250, 'so one read returns it — no join needed.', size=9.5)
    d.text(480, 282, '"customerId" (highlighted) is the partition key.', size=9.5, weight=700)
    return d

def d_key():
    d = Diagram('cs2', 640, 316, 'A good partition key spreads items evenly across partitions; a bad one piles most items on one hot partition')
    for px, title, good in ((10,'GOOD KEY · customerId', True), (325,'BAD KEY · status = "open"', False)):
        d.zone(px, 8, 305, 300, 'emerald' if good else 'rose', title)
        d.box(px+92, 38, 120, 34, [('📥 New items','t')], 'n')
        d.zone(px+16, 112, 273, 134, 'n', 'LOAD ON EACH PARTITION')
        d.arrow([(px+152,72),(px+152,112)], 'emerald' if good else 'rose', label='the key decides', at=(px+232,92))
        heights = (62, 66, 58, 64) if good else (84, 10, 8, 6)
        for i, h in enumerate(heights):
            bx = px + 40 + i*62
            d.add(f'<rect x="{bx}" y="{232-h}" width="40" height="{h}" rx="5" fill="{"#34d399" if good else ("#fb7185" if i==0 else "#5b6577")}" opacity=".8"/>')
            d.text(bx+20, 243, f'P{i+1}', size=8.5, mono=True)
        d.text(px+152, 270, '✅ load is spread out — fast and cheap' if good else '⚠️ one partition does most of the work', size=9.5, weight=700)
        d.text(px+152, 288, 'every partition shares the load' if good else 'slow, throttled and more expensive', size=9.5)
    return d

def d_consistency():
    d = Diagram('cs3', 640, 232, 'The five Cosmos DB consistency levels from strongest (Strong) to weakest (Eventual); Session is the default')
    d.text(10, 34, 'STRONGEST promise', anchor='start', size=9.5, mono=True)
    d.text(630, 34, 'WEAKEST promise', anchor='end', size=9.5, mono=True)
    lv = [('Strong',['always the','latest write'],'rose'), ('Bounded',['staleness','lag has a limit'],'amber'),
          ('⭐ Session',['(the default)','you read your','own writes'],'cyan'), ('Consistent',['prefix','never out of','order'],'violet'), ('Eventual',['may be behind,','catches up later'],'n')]
    for i, (t, ls, col) in enumerate(lv):
        d.box(11 + i*128, 52, 116, 88, [(t,'t')] + [(l,'s') for l in ls], col)
    d.arrow([(69,140),(69,186),(581,186),(581,140)], 'n', label='weaker promise  →  more speed and availability', at=(320,186))
    return d

def d_both():
    d = Diagram('cs4', 640, 286, 'One shop app using Azure SQL for orders, Cosmos DB for the catalog and Blob Storage for photos')
    d.box(10, 112, 92, 60, [('🛒 Shop app','t')], 'n')
    rows = [(20,'violet','🟦 Azure SQL','orders · payments · stock — must be exact','all-or-nothing'),
            (112,'cyan','🌍 Cosmos DB','catalog · sessions · profiles — flexible and fast','flexible, fast reads'),
            (204,'amber','📦 Blob Storage','product photos and invoice PDFs','big files')]
    for y, col, t, s, lab in rows:
        d.box(330, y, 300, 62, [(t,'t'),(s,'s')], col)
        d.arrow([(102,142),(126,142),(126,y+31),(330,y+31)], col, label=lab, at=(228,y+31))
    return d

def build_cosmos_db_vs_azure_sql():
    body = ''
    body += see(figure(d_shapes(),
        'the same order, stored in two different ways. In <b>Azure SQL</b> the order is split into related tables (customers, orders, order items) that point at each other with <b>foreign keys</b>; to read the whole order you <b>JOIN</b> them. '
        'In <b>Cosmos DB</b> the same order is <b>one JSON item</b> with everything inside it, so one read returns the lot. The highlighted <code>customerId</code> is the <b>partition key</b> — the label Cosmos DB uses to decide where the item lives.'))
    body += one('Azure SQL keeps data correct by relating tables. Cosmos DB keeps data fast by storing things together and spreading them out. Neither is "better" — they answer different questions.')
    body += why([
      'The Databases page gave you the map. This page exists because people still mix these two up — both can store "an order", both are fully managed, and both are popular. '
      'The real difference is what each one is <b>built to be good at</b>.',
      '<b>Azure SQL</b> is built for <i>correctness across related data</i>: strict tables, relationships and transactions. <b>Cosmos DB</b> is built for <i>speed and scale for access patterns you know in advance</i>: flexible items, spread over partitions and regions. '
      'If you know which one your problem looks like, the choice is easy. This page shows you how to tell.'])
    body += block('⚡ The quick comparison', table(['','Azure SQL (relational)','Azure Cosmos DB (NoSQL)'], [
      ['Data model','Tables, rows and columns','JSON items inside containers'],
      ['Relationships','Foreign keys and joins across tables','Embed related data in the item, or link by id. A JOIN works only inside one item'],
      ['Transactions','All-or-nothing across many tables','All-or-nothing inside one partition key (transactional batch)'],
      ['Schema','Fixed. Changes need a migration','Flexible. Each item can look different'],
      ['Growing','Mostly a bigger machine, plus readable copies','Spread out across partitions'],
      ['Worldwide','Copies in other regions for reading and failover; one writable primary','Replicate to many regions; can be set up to accept writes in more than one'],
      ['Queries','Rich ad-hoc SQL: joins, grouping, reports','Fast when the query includes the partition key. Queries across partitions cost more'],
      ['You pay for','Compute (vCores or DTUs) and storage. Serverless can pause when idle','Request Units per second (set, autoscaled, or pay-per-use serverless) and storage. Each extra region adds cost'],
      ['Think of it as','A smart system with strict rules','A very fast filing cabinet sorted by one label (the key)'],
    ]), label_cls='see')
    body += block('⚖️ Strengths and watch-outs', proscons('🟦 Azure SQL',
      ['Relationships and constraints keep data correct', 'Powerful SQL for reports and questions nobody planned for', 'All-or-nothing transactions across many tables', 'Mature tools, and many people already know T-SQL', 'Managed backups and high availability; serverless and Hyperscale options'],
      ['Writes mostly scale by using a bigger machine', 'One writable primary — worldwide multi-writer is not built in', 'Schema changes need planning and migrations', 'Very high worldwide traffic gets expensive and complex']) +
      proscons('🌍 Cosmos DB',
      ['Designed for single-digit-millisecond reads and writes', 'Scales out by partition key', 'Replicates to many regions, with multi-region writes available', 'Flexible items — the schema can change freely', 'Indexes all properties by default', 'Five consistency levels let you trade freshness for speed'],
      ['The partition key is a big early decision — hard to change later', 'No foreign keys; a JOIN works only inside one item', 'Transactions stay inside one partition key', 'Cost is measured in Request Units — an expensive query burns many', 'Cross-partition queries fan out and cost more', 'You model the data around your queries, which is a new habit']), label_cls='see')
    body += block('🔑 The partition key — the one decision that matters', figure(d_key(),
        'every Cosmos DB item has a <b>partition key</b>. Cosmos DB uses it to decide which partition stores the item. A <b>good key</b> has many different values and appears in most of your queries — <code>customerId</code> spreads orders across partitions evenly. '
        'A <b>bad key</b> has few values — if most orders are "open", they all pile onto one <b>hot partition</b> while the others sit idle. One logical partition can hold only about 20 GB, so a key with plenty of values also protects you from running out of room.') +
        '\n    <div class="kd-card" style="margin-top:16px"><b>Rule of thumb:</b> pick a key that (1) has <b>many</b> different values, (2) shows up in <b>most</b> of your queries, and (3) spreads reads and writes <b>evenly</b>. '
        'And remember the unit of cost: a <b>Request Unit (RU)</b> is Cosmos DB\'s currency for work — reading one small item by its id and partition key is the cheapest thing you can ask for.</div>', label_cls='see')
    body += block('🎚️ Consistency — how fresh must a read be?', figure(d_consistency(),
        'when data is copied to several places, a read might hit a copy that is slightly behind. Cosmos DB lets you choose how strict to be. <b>Strong</b> always returns the latest write. <b>Eventual</b> may be behind but catches up. '
        'In between, <b>Session</b> — the default — promises that <em>you</em> always see your own writes. Example: you post a comment and refresh. With Session you see your comment right away; with Eventual you might not, for a moment. '
        'The stronger the promise, the more the copies must coordinate — so you give up some speed and availability.'), label_cls='see')
    body += block('🤝 You do not have to pick one — use both', figure(d_both(),
        'real systems often use several stores. This shop keeps <b>orders, payments and stock</b> in Azure SQL, where exactness matters; the <b>catalog, sessions and profiles</b> in Cosmos DB, where flexibility and speed matter; and <b>photos and invoices</b> in Blob Storage. '
        'This idea is called <b>polyglot persistence</b>: use the right store for each kind of data.'), label_cls='see')
    body += block('✅ Decide in 30 seconds', pick_cards([
      dict(icon='🟦', name='Choose Azure SQL when…', tag='correctness across related data is the job', color='#a78bfa',
           use=['Your data is naturally tables that relate to each other', 'You need all-or-nothing transactions across several tables', 'People will ask new questions you cannot predict (reports, analytics)', 'Your team already knows SQL Server / T-SQL'],
           skip=['You need fast writes in many regions at once', 'Your data shape changes every week']),
      dict(icon='🌍', name='Choose Cosmos DB when…', tag='speed and scale for known access patterns is the job', color='#22d3ee',
           use=['You can name the main queries up front', 'Users are spread across the world and need low latency', 'Items vary in shape (a catalog, profiles, events)', 'Traffic is huge or unpredictable and must scale out'],
           skip=['You need many joins between lots of different entities', 'You cannot pick a good partition key', 'Strict multi-table transactions are the core of the app']),
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🏦','Bank transfers','Debit one account, credit another — both or neither, always auditable.','Azure SQL'),
      ('🛍️','Product catalog','Shoes have sizes, TVs have screen types. New product kinds appear weekly.','Cosmos DB'),
      ('🎮','Live leaderboard','Millions of players, constant tiny updates, readers worldwide.','Cosmos DB'),
      ('📈','Monthly sales report','"Revenue by region by month" — a question nobody planned for.','Azure SQL'),
      ('🧺','Shopping cart / session','Read and written on every click, needs to be fast anywhere.','Cosmos DB'),
      ('🏪','The whole shop','Orders exact, catalog flexible, photos large.','All three'),
    ]), label_cls='see')
    body += recall([
      'Azure SQL = related tables, joins, multi-table transactions; Cosmos DB = JSON items, spread by partition key, fast at scale.',
      'Cosmos DB: choose a partition key with many values that appears in most queries. A bad key creates a hot partition.',
      'A JOIN in Cosmos DB works only inside one item; transactions stay inside one partition key.',
      'Cost: Azure SQL = compute + storage. Cosmos DB = Request Units + storage (+ each extra region).',
      'Cosmos DB has five consistency levels — Strong, Bounded staleness, Session (default), Consistent prefix, Eventual.',
      'Using both together is normal (polyglot persistence).'])
    body += saythis('"Azure SQL is my default when data is relational and correctness across tables matters — it gives me joins, constraints and transactions, and scales mostly up with read replicas. '
      'Cosmos DB is for known access patterns at global scale: flexible JSON items, partitioned by key, replicated across regions, with tunable consistency and cost measured in Request Units. '
      'The partition key is the critical design choice. Many real systems use both — SQL for orders and payments, Cosmos for catalog and sessions."')
    body += trap([
      '<b>Cosmos DB is not "SQL Server with JSON".</b> If you design its data like a relational database — many small items that you JOIN together — you will fight it. Model the data around the questions you ask.',
      'The opposite trap: choosing Azure SQL "because we know it" when the real need is writes in many regions at once, or choosing Cosmos DB "because it sounds modern" when the real need is reports across related tables.'])
    body += confuse('🔑 Primary key (SQL)', 'Uniquely identifies a row in one table. The database enforces it.', '🔑 Partition key (Cosmos DB)', 'Decides which partition stores the item. It is about <i>where data lives and how load spreads</i>, not only about uniqueness.')
    body += zoom('💻 Tiny illustrative examples', code_block(
'''<span class="cmt">-- Azure SQL: relationships are enforced by the database</span>
<span class="kw">CREATE TABLE</span> Orders (
  Id <span class="kw">INT PRIMARY KEY</span>,
  CustomerId <span class="kw">INT NOT NULL REFERENCES</span> Customers(Id)   <span class="cmt">-- a foreign key</span>
);

<span class="cmt"># Cosmos DB (Python SDK): the partition key is chosen when the container is created</span>
container = database.create_container_if_not_exists(
    id=<span class="str">"orders"</span>, partition_key=PartitionKey(path=<span class="str">"/customerId"</span>))''',
      'Illustrative shapes only — real setups also choose throughput (or serverless), indexing and security settings.'))
    body += next_box('That is the Cosmos DB vs Azure SQL decision. Back to the Databases page for the full map — and on to the next concept in the journey.', 'databases.html', 'Back to Databases')
    body += fact_note('Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official docs.',
        [DOCS_COS, DOCS_SQL, DOCS_ARCH])
    return page('cosmos-db-vs-azure-sql', 'Cosmos DB vs Azure SQL', 'Deep dive · Databases · ⚖️ Choosing',
        'Cosmos DB and Azure SQL are both great — they answer <span class="grad-text">different questions</span>.',
        'Choosing between them is one of the most common architecture questions. Here is a plain-English comparison with pictures, strengths, weaknesses and real examples — '
        'so you can decide in minutes, not meetings.',
        'When would you choose Azure Cosmos DB over Azure SQL Database, and what are the trade-offs?',
        body, CR + ['<a href="databases.html">Databases</a>', '<span class="cur">Cosmos DB vs Azure SQL</span>'], '', search_title='Cosmos DB vs Azure SQL')
