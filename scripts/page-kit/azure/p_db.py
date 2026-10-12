from kit import *
from p_storage import CR

DOCS_SQL = ('Azure SQL documentation', 'https://learn.microsoft.com/en-us/azure/azure-sql/')
DOCS_COS = ('Azure Cosmos DB documentation', 'https://learn.microsoft.com/en-us/azure/cosmos-db/')
DOCS_ARCH = ('Azure Architecture Center', 'https://learn.microsoft.com/en-us/azure/architecture/')

def d_map():
    d = Diagram('db1', 640, 404, 'Decision map: relational data goes to Azure SQL or PostgreSQL/MySQL, flexible global-scale items to Cosmos DB, plain files to Storage')
    d.box(190, 8, 260, 34, [('🤔 What does your data look like?','t')], 'cyan')
    d.box(10, 130, 320, 70, [('🔗 Tables that relate to each other','t'),('joins · constraints · all-or-nothing transactions','s')], 'violet')
    d.box(350, 130, 140, 70, [('🧩 Flexible items','t'),('JSON · huge scale','s'),('users worldwide','s')], 'cyan')
    d.box(510, 130, 120, 70, [('📄 Just files','t'),('photos · backups','s')], 'amber')
    d.arrow([(320,42),(320,60),(170,60),(170,130)], 'violet', label='tables, joins', at=(170,96))
    d.arrow([(320,42),(320,60),(420,60),(420,130)], 'cyan', label='scale-out + JSON', at=(420,96))
    d.arrow([(320,42),(320,60),(570,60),(570,130)], 'amber', label='files, not rows', at=(570,96))
    d.box(10, 300, 150, 84, [('🟦 Azure SQL','t'),('SQL Database','s'),('Managed Instance','s'),('SQL Server on a VM','s')], 'violet')
    d.box(180, 300, 150, 84, [('🐘 Open source','t'),('PostgreSQL ·','s'),('MySQL','s'),('Flexible Server','s')], 'violet')
    d.box(350, 300, 140, 84, [('🌍 Cosmos DB','t'),('NoSQL API (JSON)','s'),('plus other APIs','s')], 'cyan')
    d.box(510, 300, 120, 84, [('📦 Storage','t'),('Blob / Files','s'),('not a database','s')], 'amber')
    d.arrow([(85,200),(85,300)], 'violet', label='SQL Server skills', at=(85,252))
    d.arrow([(255,200),(255,300)], 'violet', label='open-source engine', at=(255,252))
    d.arrow([(420,200),(420,300)], 'cyan', label='global · low latency', at=(420,252))
    d.arrow([(570,200),(570,300)], 'amber', label='not a database', at=(570,252))
    return d

def d_sql_ladder():
    d = Diagram('db2', 640, 236, 'Azure SQL options from most control to most managed: SQL Server on a VM, SQL Managed Instance, SQL Database')
    d.text(10, 30, 'more control, more admin work', anchor='start', size=10, weight=600)
    d.text(630, 30, 'less admin work, fewer options', anchor='end', size=10, weight=600)
    d.box(10, 50, 190, 100, [('🖥️ SQL Server on a VM','t'),('you patch the OS and SQL','s'),('full control','s'),('any version you choose','s')], 'n')
    d.box(225, 50, 190, 100, [('🏢 SQL Managed Instance','t'),('Microsoft runs the server','s'),('keeps SQL Server features','s'),('(SQL Agent, linked servers)','s')], 'violet')
    d.box(440, 50, 190, 100, [('🗄️ Azure SQL Database','t'),('Microsoft runs everything','s'),('you manage just the data','s'),('serverless option available','s')], 'cyan')
    d.arrow([(105,150),(105,190),(535,190),(535,150)], 'cyan', label='you hand more work to Microsoft', at=(320,190))
    return d

def d_scale():
    d = Diagram('db3', 640, 392, 'Two ways to scale: Azure SQL has one writable primary with readable copies; Cosmos DB splits data by partition key across partitions and regions')
    d.zone(10, 8, 305, 376, 'violet', 'AZURE SQL · one writer, copies for reading')
    d.box(100, 44, 120, 36, [('💻 App','t')], 'n')
    d.box(90, 120, 140, 62, [('🟦 Primary database','t'),('reads + writes','s')], 'violet')
    d.arrow([(160,80),(160,120)], 'violet', label='all requests', at=(240,100))
    d.box(26, 244, 130, 44, [('Readable copy','t'),('reads only','s')], 'n')
    d.box(164, 244, 130, 44, [('Readable copy','t'),('reads only','s')], 'n')
    d.arrow([(100,182),(100,244)], 'violet', label='copies data', at=(100,213))
    d.arrow([(220,182),(220,244)], 'violet', label='copies data', at=(220,213))
    d.text(162, 318, 'Writes go to one place. Reads can use the copies.', size=9.5)
    d.text(162, 336, 'Mostly scales UP — a bigger machine —', size=9.5)
    d.text(162, 352, 'and the copies add read capacity.', size=9.5)
    d.zone(325, 8, 305, 376, 'cyan', 'COSMOS DB · data split by partition key')
    d.box(420, 44, 120, 36, [('💻 App','t')], 'n')
    d.box(360, 112, 240, 46, [('🔑 Partition key','t'),('its hash picks the partition','s')], 'cyan')
    d.arrow([(480,80),(480,112)], 'cyan', label='item + key', at=(556,96))
    d.zone(345, 196, 272, 92, 'n', 'PARTITIONS (managed for you)')
    for i, x in enumerate((360, 424, 488, 552)):
        d.box(x, 226, 50, 44, [(f'P{i+1}','t')], 'cyan')
    d.arrow([(480,158),(480,196)], 'cyan', label='hash picks one', at=(556,177))
    d.box(360, 332, 240, 40, [('🌍 Same data in other regions','t')], 'violet')
    d.arrow([(480,288),(480,332)], 'violet', label='replicated', at=(547,310))
    return d

def build_databases():
    body = ''
    body += see(figure(d_map(),
        'start with the shape of your data, then follow the arrow. <b>Tables that relate to each other</b> (customers → orders → items) point to a relational engine: the Azure SQL family if you want the SQL Server world, '
        'or PostgreSQL/MySQL Flexible Server if you prefer open source. <b>Flexible JSON items at world scale</b> point to Azure Cosmos DB. And if it is really just files, it never needed a database — that is Storage.'))
    body += one('Pick a database by the shape of your data and the questions you will ask — not by what is popular. Related tables → Azure SQL (or Postgres/MySQL). Flexible items at world scale → Cosmos DB.')
    body += why([
      'Storage keeps files and simple records safe. But imagine this question: <i>"Show customer 42\'s orders from last month over $100 — and when they buy, reduce the stock <b>and</b> save the order, or do neither."</i> '
      'A storage account cannot search across records, join related data, or promise that two changes happen together.',
      'A <b>database</b> adds exactly those three things: fast queries (indexes), relationships between data, and <b>transactions</b> — all-or-nothing changes. '
      'Azure offers several databases because data comes in different shapes, and forcing every shape into one engine means paying for it later in speed, cost or complexity.'])
    body += block('🧰 The Azure database family', pick_cards([
      dict(icon='🗄️', name='Azure SQL Database', tag='the fully managed SQL Server engine, for new cloud apps', color='#a78bfa',
           use=['A new app with related tables', 'You want Microsoft to patch, back up and run it', 'Spiky or idle workloads (serverless option can pause when idle)', 'Very large databases (Hyperscale tier)'],
           skip=['You need instance-level SQL Server features → Managed Instance', 'You need the operating system itself → SQL on a VM']),
      dict(icon='🏢', name='SQL Managed Instance', tag='nearly all SQL Server features, still managed', color='#c4b5fd',
           use=['Moving an existing SQL Server app with minimal changes', 'You rely on SQL Agent, linked servers, cross-database queries or CLR'],
           skip=['A brand-new app that needs none of those → SQL Database is simpler']),
      dict(icon='🖥️', name='SQL Server on an Azure VM', tag='your own SQL Server, running on a virtual machine', color='#93a0b8',
           use=['You need access to the operating system or file system', 'You must stay on one exact SQL Server version', 'You already own licenses you want to reuse'],
           skip=['You do not want to patch and look after a VM → use a managed option']),
      dict(icon='🐘', name='PostgreSQL / MySQL Flexible Server', tag='managed open-source relational databases', color='#8b9eff',
           use=['Your app is built for PostgreSQL or MySQL', 'You want open-source tools and extensions', 'You want a managed service without rewriting the app'],
           skip=['You are an SQL Server shop with T-SQL code → Azure SQL', 'You need flexible JSON at world scale → Cosmos DB']),
      dict(icon='🌍', name='Azure Cosmos DB', tag='a globally distributed NoSQL database', color='#22d3ee',
           use=['Flexible JSON items and a schema that keeps changing', 'Users all over the world who need fast reads and writes', 'Huge scale by spreading data over partitions'],
           skip=['Many joins and strict relationships between tables → relational', 'You cannot choose a good partition key yet']),
    ]))
    body += block('🪜 Azure SQL: how much do you want to manage?', figure(d_sql_ladder(),
        'the three Azure SQL options sit on a ladder. On the left you get <b>full control</b> — your own SQL Server on a virtual machine — but you patch and look after it. '
        'In the middle, <b>Managed Instance</b> keeps almost every SQL Server feature while Microsoft runs the server. On the right, <b>SQL Database</b> is the most managed: you look after your data and nothing else. '
        'A good rule: start on the right, and move left only if you have a hard reason.'), label_cls='see')
    body += block('📐 Two ways to grow — see the difference', figure(d_scale(),
        '<b>Left — Azure SQL:</b> every change goes to one primary database; copies of the data can serve reads. You grow mostly by using a bigger machine. '
        '<b>Right — Cosmos DB:</b> every item carries a <b>partition key</b>; its hash decides which partition stores the item, so the data (and the load) is spread across many partitions and can be copied to other regions. '
        'That is why Cosmos DB grows by spreading out, and why choosing the partition key well is the most important decision there.') +
        '\n' + table(['','Relational (Azure SQL, PostgreSQL, MySQL)','Azure Cosmos DB (NoSQL)'], [
          ['Data shape','Tables with rows and columns, a fixed schema','JSON items in containers, flexible schema'],
          ['Relationships','Foreign keys and joins between tables','Usually embedded inside one item, or linked by id'],
          ['All-or-nothing changes','Transactions across many tables','Transactions inside one partition key'],
          ['Growing','Mostly bigger machine, plus read copies','Spread data across partitions and regions'],
          ['Queries','Powerful ad-hoc SQL: joins, grouping, reports','Fast when the query includes the partition key'],
        ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🛒','Online shop orders','Customers, orders and stock must stay consistent. Money is involved.','Azure SQL Database'),
      ('🏭','Old ERP on SQL Server','Uses SQL Agent jobs and cross-database queries. Rewriting it is not possible this year.','SQL Managed Instance'),
      ('🐘','App built on PostgreSQL','The team already knows Postgres and uses its extensions.','PostgreSQL Flexible Server'),
      ('🎮','Game player profiles','Millions of players worldwide, profile read on every login, schema changes each season.','Cosmos DB'),
      ('🏷️','Product catalog','Shoes have a size; laptops have RAM. Every product has different attributes.','Cosmos DB (or SQL with JSON)'),
      ('🏦','Bank ledger','Every transfer must be exact, auditable and all-or-nothing across accounts.','Azure SQL Database'),
    ]), label_cls='see')
    body += block('🔬 Go deeper', deep_cards([('Deep dive · Databases', 'Cosmos DB vs Azure SQL', 'The two you will be asked about most: side-by-side strengths and weaknesses, partition keys, request units, consistency levels and when to use both.', 'cosmos-db-vs-azure-sql.html')]), label_cls='next')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Two ways to buy Azure SQL.</b> The <b>vCore</b> model lets you pick compute and storage separately. The <b>DTU</b> model bundles them into simple packages.
      The <b>serverless</b> compute tier (vCore only) scales with load and can pause when idle, so you pay for storage only while it is paused.</p>
      <p><b>Hyperscale</b> is the service tier built for very large databases and fast scaling of storage and read copies.</p>
      <p><b>PostgreSQL and MySQL:</b> use <b>Flexible Server</b>. The older PostgreSQL "Single Server" has been retired, so new work should never start on it.</p>
      <p><b>Cosmos DB has several APIs</b> — NoSQL (its native one, recommended for new apps), MongoDB, Cassandra, Gremlin (graph) and Table — so you can often keep the tools you already know.</p>''')
    body += recall([
      'Choose by data shape and question shape: related tables → relational; flexible items at global scale → Cosmos DB; plain files → Storage.',
      'Azure SQL family: SQL Database (most managed, new apps) → Managed Instance (SQL Server features, easy migration) → SQL Server on a VM (full OS control).',
      'PostgreSQL / MySQL → use Flexible Server.',
      'Relational scales mostly up, with read copies. Cosmos DB scales out by partition key, and can replicate to other regions.',
      'A database adds queries, relationships and transactions — the things Storage cannot do.'])
    body += saythis('"I choose a database by the shape of the data and the queries. For related tables and transactions I start with Azure SQL Database, move to Managed Instance if I need instance-level SQL Server features, '
      'and only use SQL on a VM when I need the OS. For open-source apps I use PostgreSQL or MySQL Flexible Server. For flexible JSON data that must be fast worldwide I use Cosmos DB, where the partition key is the key design decision."')
    body += trap([
      '<b>"NoSQL" does not mean "better" or "faster for everything".</b> Cosmos DB is excellent when your queries match your partition key, and painful when they do not. Relational databases are not "old" — for related data and transactions they are still the right default.',
      'Also watch the names: <i>Azure SQL Database</i> is one product, <i>Azure SQL</i> is the whole family, and <i>Azure Database for PostgreSQL</i> is a different service again.'])
    body += confuse('🗄️ Azure SQL Database', 'Fully managed. You get a database, not a server. Best for new apps.', '🏢 SQL Managed Instance', 'A whole managed SQL Server instance, with features like SQL Agent. Best for moving existing apps with few changes.')
    body += zoom('💻 Tiny illustrative examples', code_block(
'''<span class="cmt">-- Azure SQL: related tables + an all-or-nothing change</span>
<span class="kw">BEGIN TRANSACTION</span>;
  <span class="kw">UPDATE</span> Stock <span class="kw">SET</span> Qty = Qty - <span class="num">1</span> <span class="kw">WHERE</span> ProductId = <span class="num">7</span>;
  <span class="kw">INSERT INTO</span> Orders (CustomerId, ProductId) <span class="kw">VALUES</span> (<span class="num">42</span>, <span class="num">7</span>);
<span class="kw">COMMIT</span>;   <span class="cmt">-- both happen, or neither does</span>

<span class="cmt">// Cosmos DB (NoSQL API): one order = one JSON item, read fast by id + partition key</span>
<span class="kw">const</span> { resource } = <span class="kw">await</span> container.item(<span class="str">"order-1001"</span>, <span class="str">"customer-42"</span>).read();''',
      'Illustrative shapes only — real code adds error handling, retries and connection setup.'))
    body += next_box('One database plus one app server is a working instance. But what happens when one instance is not enough? Next: spreading traffic across many.', None)
    body = body.replace('One database plus one app server is a working instance. But what happens when one instance is not enough? Next: spreading traffic across many.',
                        'One database plus one app server is one working instance — but one instance is a single point of failure. Next: Load Balancing &amp; Traffic Routing <i>(coming soon)</i>.')
    body += fact_note('Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official docs.', [DOCS_SQL, DOCS_COS])
    return page('databases', 'Databases', 'Concept 7 of 19 · 🧱 Building blocks',
        'Pick a database by <span class="grad-text">the shape of your data</span> and the questions you will ask — not by what is popular.',
        'Tables that relate to each other, flexible JSON items at world scale, and plain files all need different homes. Azure has a family of databases for this. '
        'Learn the map, then learn when each one wins.',
        'When would you choose Azure SQL, PostgreSQL/MySQL or Cosmos DB for a new application?',
        body, CR + ['<span class="cur">Databases</span>'], '')
