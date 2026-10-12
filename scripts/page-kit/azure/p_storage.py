from kit import *

# ---------------------------------------------------------------- D1: four doors
def d_doors():
    d = Diagram('st1', 640, 300, 'A storage account holds four services: containers (Blob), file shares, queues and tables')
    d.box(10, 110, 92, 60, [('💻 Your app','t'),('web · API · VM','s')], 'n')
    d.zone(238, 8, 392, 284, 'violet', '🗄️  ONE STORAGE ACCOUNT')
    cards = [
     (46,  'cyan',    '📦 Containers  (Blob)',       'files as objects: photos, video, backups', '<account>.blob.core.windows.net',  'HTTPS (REST)'),
     (104, 'violet',  '📁 File shares  (Azure Files)','a shared drive, like \\\\server\\share',    '<account>.file.core.windows.net',  'SMB / NFS'),
     (162, 'amber',   '📬 Queues',                    'small messages waiting to be handled',     '<account>.queue.core.windows.net', 'HTTPS (REST)'),
     (220, 'emerald', '🗒️ Tables',                    'simple key → value records',               '<account>.table.core.windows.net', 'HTTPS (REST)'),
    ]
    for y, col, t, s, ep, lab in cards:
        d.box(254, y, 360, 50, [(t,'t'),(s,'s'),(ep,'m')], col)
        d.arrow([(102,140),(125,140),(125,y+25),(254,y+25)], col, label=lab, at=(190, y+25))
    return d

# ---------------------------------------------------------------- D2: decision tree
def d_choose():
    d = Diagram('st2', 640, 540, 'Decision tree: which Azure storage service for which data')
    d.box(190, 8, 260, 34, [('🤔 What are you storing?','t')], 'cyan')
    qs = [
     (84,  '📦 Files, images, videos, backups or logs?',    'anything file-like that you read by name', 'Blob Storage',  'containers → blobs',                 'cyan'),
     (182, '📁 A shared drive many machines mount?',        'like \\\\server\\share or a Linux folder',  'Azure Files',   'SMB or NFS file shares',             'violet'),
     (280, '📬 Small jobs handed between app parts?',       'a simple to-do list for your code',        'Queue Storage', 'need ordering? → Service Bus',      'amber'),
     (378, '🗒️ Simple key → value records, very cheap?',   'no joins, no complex queries',             'Table Storage', 'need global scale? → Cosmos DB',    'emerald'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(y,q,qs_,a,as_,col) in enumerate(qs):
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(420, y, 210, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(420,y+27)], col, label='yes', at=(380,y+27))
        nxt = qs[i+1][0] if i+1 < len(qs) else 476
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 476, 330, 50, [('🛢️ None of these? Probably a database','t'),('needs queries, joins or transactions → Databases','s')], 'rose')
    return d

# ---------------------------------------------------------------- D3: redundancy
def d_redundancy():
    d = Diagram('st3', 640, 528, 'Redundancy options LRS, ZRS, GRS and GZRS shown as copies of data across datacenters, zones and regions')
    def dc(x, y, col='cyan'): d.box(x, y, 120, 48, [('Datacenter','t'),('● ● ●','d')], col)
    # row 1: LRS | ZRS
    d.zone(10, 10, 305, 150, 'n', 'LRS · 3 copies in 1 datacenter')
    d.zone(22, 38, 281, 82, 'cyan', 'PRIMARY REGION')
    d.box(102, 64, 120, 48, [('Datacenter','t'),('● ● ●','d')], 'cyan')
    d.text(162, 144, '✅ drive / rack failure  ·  ❌ datacenter loss', size=9)
    d.zone(325, 10, 305, 150, 'n', 'ZRS · 1 copy in each of 3 zones')
    d.zone(337, 38, 281, 82, 'cyan', 'PRIMARY REGION')
    for i in range(3):
        d.box(352 + i*88, 64, 78, 48, [(f'Zone {i+1}','t'),('●','d')], 'cyan')
    d.text(477, 144, '✅ one zone fails  ·  ❌ whole region lost', size=9)
    # row 2: GRS
    d.zone(10, 174, 620, 150, 'n', 'GRS · LRS in the primary region + a copy in a paired region')
    d.zone(22, 202, 250, 82, 'cyan', 'PRIMARY REGION')
    d.box(87, 228, 120, 48, [('Datacenter','t'),('● ● ●','d')], 'cyan')
    d.zone(368, 202, 250, 82, 'violet', 'SECONDARY (PAIRED) REGION')
    d.box(433, 228, 120, 48, [('Datacenter','t'),('● ● ●','d')], 'violet')
    d.arrow([(272,252),(433,252)], 'violet', label='copied asynchronously', at=(352,252), flow=True)
    d.text(320, 308, '✅ the whole primary region is lost  (recent writes may not have arrived yet)', size=9)
    # row 3: GZRS
    d.zone(10, 338, 620, 150, 'n', 'GZRS · ZRS in the primary region + a copy in a paired region')
    d.zone(22, 366, 250, 82, 'cyan', 'PRIMARY REGION')
    for i in range(3):
        d.box(32 + i*80, 392, 70, 48, [(f'Zone {i+1}','t'),('●','d')], 'cyan')
    d.zone(368, 366, 250, 82, 'violet', 'SECONDARY (PAIRED) REGION')
    d.box(433, 392, 120, 48, [('Datacenter','t'),('● ● ●','d')], 'violet')
    d.arrow([(272,416),(433,416)], 'violet', label='copied asynchronously', at=(352,416), flow=True)
    d.text(320, 472, '✅ a zone fails  ·  ✅ the whole primary region is lost', size=9)
    d.text(320, 512, '●  = one copy of your data', size=9, mono=True)
    return d

CR = ['<a href="../../index.html">KeyDrive</a>', '<a href="../index.html">🔷 Azure</a>']
DOCS_ST = ('Azure Storage documentation', 'https://learn.microsoft.com/en-us/azure/storage/')

def build_storage():
    body = ''
    body += see(figure(d_doors(),
        'one storage account holds four separate services. Each one has its own web address (an endpoint) and its own job. '
        'In the Azure portal you will find them under <b>Data storage</b>: Containers, (Classic) file shares, Queues and Tables. '
        'Your app picks the door that matches the shape of its data.'))
    body += one('A storage account is four doors — Blob, Files, Queues, Tables. Pick the door by what the data looks like and how your app reads it.')
    body += why([
      'In the last step you gave your code a place to <b>run</b>. But a place to run is not a place to <b>keep things</b>. '
      'A virtual machine can be replaced, a container is thrown away and rebuilt, a function disappears between calls — '
      'anything your code saved on its own disk can vanish with it.',
      'Real apps keep photos, invoices, backups and logs for years. Storage gives that data a safe home <b>outside</b> your compute, '
      'so your servers can come and go. And because "data" is not one shape — a photo, a shared folder, a job waiting to run and a '
      'simple record are all different — Azure gives you four doors instead of one.'])
    body += block('🚪 Meet the four doors', pick_cards([
      dict(icon='📦', name='Blob (Containers)', tag='a huge folder of files, each with a web address', color='#22d3ee',
           use=['Photos, videos, PDFs, backups, log files', 'Files that users download or your code reads by name', 'Data for analytics (a "data lake")', 'A static website'],
           skip=['You need a drive that machines "mount" like a normal folder → Files', 'You need to search rows with queries → a database']),
      dict(icon='📁', name='Azure Files (File shares)', tag='a shared drive in the cloud — SMB or NFS', color='#a78bfa',
           use=['An older app that expects a file path like <code>\\\\server\\share</code>', 'Many VMs or containers must see the same folder', 'Moving an on-premises file server to Azure'],
           skip=['Millions of files served to web users → Blob', 'Plain app data with no need for a mounted drive → Blob']),
      dict(icon='📬', name='Queues', tag='a to-do list for background work', color='#fbbf24',
           use=['Hand simple jobs from one part of your app to another', 'A very large backlog, kept cheap', 'You do not need strict order or advanced features'],
           skip=['You need ordering, retries with a "bad message" bin, or many subscribers → Service Bus (see Messaging)', 'Messages bigger than about 64 KB → send a link to a blob instead']),
      dict(icon='🗒️', name='Tables', tag='a simple, cheap key → value store', color='#34d399',
           use=['Lots of small records looked up by a key', 'Device settings, audit entries, simple lookups', 'Cheap and simple matters more than rich queries'],
           skip=['You need joins, transactions or rich queries → a database', 'You need worldwide low latency → Azure Cosmos DB (it even has a Table API)']),
    ]))
    body += block('🧭 When to pick what', figure(d_choose(),
        'start at the top and read the questions in order — the first "yes" is usually your door. Each answer also shows the usual upgrade path: '
        'a Queue that needs more power becomes Service Bus, a Table that needs global scale becomes Cosmos DB, and anything that needs real queries is a database. '
        'Real apps often use two or three doors at once.'))
    body += block('🎬 Real-world scenarios', scenarios([
      ('📸','Photo app','Users upload profile pictures. Thousands of small files, each shown by its web address.','Blob'),
      ('🏢','Old internal app','A company app expects a <code>Z:\\reports</code> drive on three servers. You cannot change the code.','Azure Files'),
      ('📧','Welcome emails','The website should answer fast and send the email later, in the background.','Queue (or Service Bus if retries matter)'),
      ('🌡️','10,000 devices','Each device has a tiny settings record, always looked up by <code>deviceId</code>.','Table (Cosmos DB if it must go global)'),
      ('🧾','Invoices for 7 years','PDFs that are almost never opened again, but must be kept.','Blob + a cheaper access tier'),
      ('🎬','Training videos','Big files streamed to customers all over the world.','Blob'),
    ]))
    body += block('🛡️ Keep your data safe: how many copies, and where?', figure(d_redundancy(),
        'four ways to keep copies of your data. <b>LRS</b> keeps three copies in one datacenter. <b>ZRS</b> spreads them across three zones. '
        '<b>GRS</b> and <b>GZRS</b> add a second, paired region — the copy is made in the background (asynchronously), so it can be a little behind. '
        'The "RA-" versions (RA-GRS, RA-GZRS) also let you <em>read</em> from that second region.') +
        '\n' + table(['Option','Copies live in','Survives','Does not survive'], [
          ['LRS','one datacenter','a drive or rack failure','losing the datacenter'],
          ['ZRS','three zones, one region','losing one zone','losing the whole region'],
          ['GRS','one datacenter + a paired region','losing the primary region','—  (recent writes may be missing)'],
          ['GZRS','three zones + a paired region','a zone <em>and</em> a region failure','—  (recent writes may be missing)'],
        ]), label_cls='see')
    body += block('🔑 Who is allowed to open the doors?', '''    <div class="taxonomy-strip">
      <div class="tax-item"><h5>✅ Microsoft Entra ID + RBAC</h5><p>Best choice. Your app or user signs in as an identity, and roles say what it may do. No secret to leak.</p></div>
      <div class="tax-item"><h5>⏱️ SAS link</h5><p>A temporary link with limited rights ("upload this one file in the next 10 minutes"). Great for browsers and partners.</p></div>
      <div class="tax-item"><h5>⚠️ Account key</h5><p>Opens everything in the account, like a master key. Avoid it in apps; prefer the two options above.</p></div>
    </div>''', label_cls='see')
    body += block('🔬 Go deeper', deep_cards([('Deep dive · Storage', 'Blob Storage in depth', 'How a blob gets its web address, the 3 blob types, a real upload flow with a SAS link, and access tiers that cut your bill.', 'blob-storage.html')]), label_cls='next')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Account types.</b> For most work you create a <b>general-purpose v2</b> storage account — the standard type that includes Blob, Files, Queues and Tables.
      <b>Premium</b> account types exist when you need very low latency for one specific job (block blobs, file shares or page blobs).</p>
      <p><b>Data Lake Storage Gen2</b> is not a separate product: it is the Blob service with the <b>hierarchical namespace</b> switched on. That gives real folders
      (rename a folder in one step) and file-style permissions — handy for big analytics jobs.</p>
      <p><b>Each service has its own endpoint</b>, like <code>myaccount.blob.core.windows.net</code>. That is why a storage account is "four doors": the same account name, four different addresses.</p>''')
    body += recall([
      'A storage account holds four services: Blob (Containers), Files (File shares), Queues and Tables.',
      'Blob = files as objects. Files = a mounted shared drive (SMB/NFS). Queue = simple background jobs. Table = simple key → value records.',
      'It exists because compute is disposable — data needs a home outside your servers.',
      'Redundancy: LRS (1 datacenter) → ZRS (3 zones) → GRS/GZRS (adds a paired region, copied asynchronously). RA- versions allow reading the second region.',
      'Prefer Entra ID + RBAC; use SAS for temporary limited access; avoid account keys.'])
    body += saythis('"A storage account is Azure\'s home for non-database data. It gives you four services under one account: Blob for objects like images and backups, '
      'Files for SMB/NFS shared drives, Queues for simple message passing and Tables for simple key-value data. I choose by the data\'s shape and how it is read, '
      'pick a redundancy level — LRS, ZRS, GRS or GZRS — to match how much failure I must survive, and I use Entra ID with RBAC for access instead of account keys."')
    body += trap([
      '<b>Redundancy is not a backup.</b> If someone deletes or overwrites a file, every copy is deleted or overwritten too — all those copies are kept in sync. '
      'To get a file back you need extra protection such as soft delete, versioning or a real backup.',
      'A second trap: using Queues or Tables for more than they are built for. If you start needing ordering, retries and subscribers, you wanted Service Bus; '
      'if you start needing joins and rich queries, you wanted a database.'])
    body += confuse('📦 Blob', 'An object (file) with a web address, in a container. Your code reads it by URL or SDK.', '📁 Azure Files', 'A real shared drive that machines mount and use like a normal folder, with SMB or NFS.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="kw">from</span> azure.identity <span class="kw">import</span> DefaultAzureCredential
<span class="kw">from</span> azure.storage.blob <span class="kw">import</span> BlobServiceClient

<span class="cmt"># sign in as the app's own identity — no account key in the code</span>
service = BlobServiceClient(<span class="str">"https://myaccount.blob.core.windows.net"</span>, credential=DefaultAzureCredential())
blob = service.get_blob_client(container=<span class="str">"photos"</span>, blob=<span class="str">"cat.jpg"</span>)

<span class="kw">with</span> open(<span class="str">"cat.jpg"</span>, <span class="str">"rb"</span>) <span class="kw">as</span> f:
    blob.upload_blob(f, overwrite=<span class="num">True</span>)   <span class="cmt"># the file now lives at .../photos/cat.jpg</span>''',
      'Illustrative shape only — a real app adds error handling, and the identity needs a role (such as Storage Blob Data Contributor) on the account.'))
    body += next_box('Files and messages now have a home. But when you need to <b>search</b>, <b>join</b> and <b>update records safely</b>, a storage account is not enough. Next: databases.', 'databases.html', 'Databases')
    body += fact_note('Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official docs.', [DOCS_ST])
    return page('storage', 'Storage', 'Concept 6 of 19 · 🧱 Building blocks',
        'An Azure storage account is <span class="grad-text">four doors</span> — you pick the door by the shape of your data.',
        'Photos, shared folders, jobs waiting to run and simple records are all different kinds of data. Azure keeps them in one place — the storage account — '
        'but each door works differently. Learn which door fits which data, and how many copies to keep.',
        'What lives inside an Azure storage account, and how do you choose between Blob, Files, Queues and Tables?',
        body, CR + ['<span class="cur">Storage</span>'], '')
