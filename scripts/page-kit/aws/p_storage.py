from kit import *
from p_common import CR

DOCS_CH = ('Choosing an AWS storage service', 'https://docs.aws.amazon.com/decision-guides/latest/storage-on-aws-how-to-choose/choosing-aws-storage-service.html')
DOCS_S3 = ('What is Amazon S3?', 'https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html')
DOCS_CLS = ('Amazon S3 storage classes', 'https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html')
DOCS_EBS = ('Amazon EBS documentation', 'https://docs.aws.amazon.com/ebs/')
DOCS_EFS = ('Amazon EFS documentation', 'https://docs.aws.amazon.com/efs/')
DOCS_FSX = ('Amazon FSx documentation', 'https://docs.aws.amazon.com/fsx/')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official AWS docs.'

def d_doors():
    d = Diagram('st1', 640, 300, 'Three storage shapes on AWS: S3 for objects over an API, EBS for a disk attached to one server, EFS and FSx for shared file systems')
    d.box(10, 40, 200, 150, [('🪣 S3','t'),('object storage','s'),('files in buckets','s'),('reached over an API','s'),('web scale','s')], 'emerald')
    d.box(220, 40, 200, 150, [('💽 EBS','t'),('block storage','s'),('a disk for one server','s'),('inside one zone','s'),('fast and simple','s')], 'violet')
    d.box(430, 40, 200, 150, [('📂 EFS and FSx','t'),('file storage','s'),('shared folders','s'),('many servers at once','s'),('NFS, Windows, Lustre…','s')], 'cyan')
    d.arrow([(110,190),(110,230),(530,230),(530,190)], 'n', label='pick by the shape of your data', at=(320,230))
    d.text(320, 278, 'Compute is disposable; data is not — keep it somewhere durable and separate.', size=9.5, weight=700)
    return d

def d_choose():
    d = Diagram('st2', 640, 436, 'Decision tree: one server needs a disk use EBS; many servers need a shared folder use EFS or FSx; otherwise store objects in S3')
    d.box(190, 8, 260, 34, [('🤔 What are you storing?','t')], 'cyan')
    qs = [
     ('💽 A disk for one server?', 'its operating system or a database volume', 'EBS', 'block storage, one zone', 'violet'),
     ('📂 A shared folder many servers mount?', 'real file paths and permissions', 'EFS or FSx', 'shared file system', 'cyan'),
     ('🪣 Files, images, backups, data-lake files?', 'read by apps over a web API', 'S3', 'object storage', 'emerald'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 372
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 372, 330, 54, [('🤔 Still unsure?','t'),('start with S3 — it fits most things','s')], 'emerald')
    return d

def d_where():
    d = Diagram('st3', 640, 296, 'EBS data lives in one Availability Zone, S3 data is spread across zones in the Region, and EFS is a regional file system')
    d.zone(10, 8, 620, 214, 'cyan', 'ONE REGION')
    for x,t in [(24,'a'),(224,'b'),(424,'c')]:
        d.zone(x, 48, 180, 150, 'n', f'AZ {t}')
    d.box(36, 100, 156, 44, [('💽 An EBS volume','t'),('this zone only','s')], 'violet')
    d.box(236, 100, 156, 44, [('📂 EFS mount','t'),('same file system','s')], 'cyan')
    d.box(436, 100, 156, 44, [('📂 EFS mount','t'),('same file system','s')], 'cyan')
    d.text(320, 244, 'S3 stores each object redundantly across zones in the Region (except One Zone classes).', size=9.5)
    d.text(320, 262, 'An EBS volume stays in one zone — copy it with snapshots to survive a zone loss.', size=9.5, weight=700)
    return d

def build_storage():
    body = ''
    body += see(figure(d_doors(),
        'AWS gives you three shapes of storage. <b>S3</b> keeps <b>objects</b> — files plus their metadata — in buckets, reached over a web API. <b>EBS</b> is a <b>block</b> disk that attaches to one server. <b>EFS and FSx</b> are <b>file</b> systems that many servers can mount as a shared folder. '
        'You pick by the <em>shape of your data</em> and by how it is accessed.'))
    body += one('Compute is disposable but data is not — pick the storage shape (object, block or file) by how the data is read, and keep it somewhere durable.')
    body += why([
      'You have places to run code. But a server can be replaced at any time; the data on it cannot. Photos, invoices, logs, backups and the disk under a database all need <b>durable homes</b> that outlive any one server.',
      'AWS offers three shapes because data is accessed three ways: <b>by name over the web</b> (objects), <b>as a raw disk</b> for one machine (blocks), or <b>as shared folders</b> (files). A wrong pick costs money or speed — object storage is not a database disk, and a disk is not a shared folder.'])
    body += block('🧰 The storage services', pick_cards([
      dict(icon='🪣', name='Amazon S3', tag='object storage', color='#34d399',
           use=['Images, documents, backups, logs, data-lake files', 'Read by apps and people over a web API', 'Grows without planning; storage classes and lifecycle rules control cost'],
           skip=['Active write-heavy file workloads that need in-place edits and file locking']),
      dict(icon='💽', name='Amazon EBS', tag='block storage for one server', color='#a78bfa',
           use=['The operating-system disk of an EC2 instance', 'A database volume that needs a fast dedicated disk', 'Data is stored redundantly in a single Availability Zone'],
           skip=['Sharing one volume between many servers — use a file system']),
      dict(icon='📂', name='Amazon EFS', tag='shared file system (NFS)', color='#22d3ee',
           use=['A shared folder that many servers or containers mount', 'Traditional file permissions and a directory tree', 'A cheaper archive class for cold file data'],
           skip=['Plain web assets and media — S3 is simpler and cheaper']),
      dict(icon='🗄️', name='Amazon FSx', tag='managed file systems', color='#fbbf24',
           use=['Specific file systems: Windows File Server, Lustre, NetApp ONTAP, OpenZFS', 'Windows clients that need Windows-style shares'],
           skip=['A simple Linux shared folder — EFS is usually enough']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'ask in order. <b>A disk for one server?</b> EBS. <b>A shared folder many servers mount?</b> EFS or FSx. <b>Files that apps read over a web API?</b> S3 — and when unsure, S3 is the right default for most data. '
        'AWS\'s own guide uses the same split: block for a single host, file for shared access, object for web-scale access.'), label_cls='see')
    body += block('📍 Where the data lives', figure(d_where(),
        'where storage lives decides what it survives. An <b>EBS volume</b> sits in one Availability Zone, so if that zone is lost, so is the volume — protect it with snapshots. <b>S3</b> stores objects redundantly across zones in the Region (the One Zone classes are the exception). '
        '<b>EFS</b> is regional and can be mounted from servers in several zones.'), label_cls='see')
    body += block('📊 Side by side', table(['','Shape','Shared?','Scope','Use it for'], [
      ['🪣 S3','Object','Yes, over an API','Region','Files, media, backups, data lakes'],
      ['💽 EBS','Block','One server at a time','One zone','OS and database disks'],
      ['📂 EFS','File (NFS)','Yes, many servers','Region','Shared Linux folders'],
      ['🗄️ FSx','File (several kinds)','Yes','Depends on the type','Windows shares, high-performance computing'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🖼️','Users upload profile photos','Millions of small files, read by the web app.','S3'),
      ('🗃️','A database server needs a fast disk','One server, one volume.','EBS'),
      ('🧑‍🤝‍🧑','Ten web servers share uploaded themes','They all need the same folder.','EFS'),
      ('🪟','A Windows file share for an office app','Windows clients, SMB shares.','FSx for Windows File Server'),
      ('📦','Nightly backups kept for years','Rarely read, must be cheap.','S3 with a cold storage class'),
      ('💾','A server dies; its disk held the only copy','Data was tied to a machine.','Keep data in S3 or take EBS snapshots'),
    ]), label_cls='see')
    body += block('🔬 Go deeper', deep_cards([('Deep dive · Storage', 'S3 in Depth: classes, lifecycle, presigned URLs and safe access', 'Storage classes, lifecycle rules, versioning, presigned URLs, Block Public Access and how to keep a bucket safe and cheap.', 's3-in-depth.html')]), label_cls='next')
    body += zoom('Go one level deeper (60 seconds) — keep data safe, not just stored', '''      <p><b>Durable is not the same as protected.</b> Designing for very high durability means data is unlikely to be lost to hardware failure. It does not protect you from someone — or a script — deleting it. Use versioning and backups for that.</p>
      <p><b>Block vs file vs object.</b> Block storage gives you a raw disk to format. File storage gives you folders with permissions. Object storage gives you whole objects by key; you replace an object, you do not edit it in place.</p>
      <p><b>Access.</b> Use IAM roles (concept 3), and for S3 also bucket policies and Block Public Access. Private subnets can reach S3 through a VPC endpoint (concept 4).</p>
      <p><b>Cost.</b> Prices depend on class, Region and requests; this page gives no figures. Check the pricing pages.</p>''')
    body += recall([
      'Object (S3), block (EBS) and file (EFS, FSx) — pick by access shape.',
      'S3: buckets and objects over an API, regional, many storage classes. EBS: a disk for one server in one AZ. EFS/FSx: shared file systems.',
      'EBS volumes live in one zone; use snapshots. S3 spreads objects across zones (except One Zone classes).',
      'Durability does not protect against deletion — use versioning and backups.',
      'When unsure, S3 is the default for most data.'])
    body += saythis('"I pick storage by its shape. S3 is object storage over an API — my default for files, media and backups. EBS is a block disk for one server in one zone, so I snapshot it. EFS or FSx is for shared file systems that many servers mount. '
      'And I remember that high durability is not protection from deletion, so I use versioning and backups."')
    body += trap([
      '<b>Using a server\'s local disk as the only home for important data.</b> Servers get replaced. Keep the data in S3, a database or an EBS volume that is backed up.',
      'Second trap: <b>an S3 bucket left open "for now".</b> Public buckets are the classic data leak. Keep Block Public Access on and share with presigned URLs or roles instead.'])
    body += confuse('🪣 S3 (object)', 'Whole objects by key, over an API. Replace, do not edit in place. Regional.', '📂 EFS (file)', 'Folders and files with permissions, mounted like a drive by many servers.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># create a bucket and upload one file</span>
aws s3 mb s3://my-example-bucket-12345 --region eu-west-1
aws s3 cp report.pdf s3://my-example-bucket-12345/reports/report.pdf''',
      'Illustrative shape only — bucket names are globally unique and the name and Region here are examples; real setups also set encryption, access rules and lifecycle rules.'))
    body += next_box('Files and disks now have homes. But when you need to <b>search</b>, <b>join</b> and <b>update records safely</b>, storage alone is not enough. Next: Databases.', 'databases.html', 'Databases')
    body += fact_note(FOOT, [DOCS_CH, DOCS_S3, DOCS_CLS, DOCS_EBS, DOCS_EFS, DOCS_FSX])
    return page('storage', 'Storage', 'Concept 6 of 19 · 🧱 Building blocks',
        'Compute is disposable but data is not — <span class="grad-text">pick the storage shape by how the data is read.</span>',
        'S3, EBS, EFS and FSx: object, block and file storage, what each is for and how to choose.',
        'When would you use S3, EBS or EFS?',
        body, CR + ['<span class="cur">Storage</span>'], '', search_title='Storage')

# ---------------------------------------------------------------- deep dive: S3
def d_classes():
    d = Diagram('s31', 640, 300, 'S3 storage classes arranged from frequently accessed to archive: Standard, Intelligent-Tiering, infrequent access, Glacier archives')
    d.text(10, 24, 'hot · accessed often', anchor='start', size=9.5, mono=True)
    d.text(630, 24, 'cold · accessed rarely', anchor='end', size=9.5, mono=True)
    boxes = [
      (10,  'emerald', [('S3 Standard','t'),('frequent access','s'),('millisecond reads','s')]),
      (138, 'cyan',    [('Intelligent-','t'),('Tiering','t'),('unknown pattern','s'),('moves for you','s')]),
      (266, 'violet',  [('Infrequent','t'),('Access','t'),('less often, still','s'),('instant reads','s')]),
      (394, 'amber',   [('Glacier','t'),('archive classes','s'),('cheap to keep','s'),('slower to read','s')]),
      (522, 'rose',    [('Deep Archive','t'),('rarely, ever','s'),('lowest cost','s'),('hours to restore','s')]),
    ]
    for x,col,lines in boxes: d.box(x, 40, 108, 130, lines, col)
    d.arrow([(64,170),(64,214),(576,214),(576,170)], 'cyan', label='cheaper to store, costlier to read', at=(320,214))
    d.text(320, 268, 'Lifecycle rules can move data down this line for you as it ages.', size=9.5, weight=700)
    return d

def d_presign():
    d = Diagram('s32', 640, 280, 'An app with permission signs a time-limited URL; the user downloads from the private bucket without making it public')
    d.box(10, 100, 110, 64, [('👤 User','t'),('wants a file','s')], 'n')
    d.box(250, 100, 140, 64, [('📱 Your app','t'),('has permission','s')], 'amber')
    d.box(510, 100, 120, 64, [('🪣 Private','t'),('bucket','t')], 'emerald')
    d.arrow([(120,122),(250,122)], 'amber', label='asks', at=(185,122))
    d.arrow([(250,148),(120,148)], 'amber', label='signed URL', at=(185,148))
    d.arrow([(60,100),(60,40),(570,40),(570,100)], 'emerald', label='downloads until the URL expires', at=(315,40))
    d.text(320, 224, 'The bucket stays private. The URL carries the app\'s permission and an expiry.', size=9.5)
    d.text(320, 242, 'Anyone holding the link can use it until it expires — keep the time short.', size=9.5, weight=700)
    return d

def d_safe():
    d = Diagram('s33', 640, 338, 'Layers that keep a bucket safe: Block Public Access, least-privilege IAM and bucket policies, versioning and lifecycle')
    rows = [
      ('🚫 Block Public Access','keep the bucket off the public internet','rose'),
      ('🪪 IAM and bucket policies','only the roles that need it, only the actions they need','violet'),
      ('♻️ Versioning','undo overwrites and deletes','cyan'),
      ('⏳ Lifecycle rules','move old data to cheaper classes, expire what you do not need','amber'),
    ]
    for i,(t,s_,c) in enumerate(rows):
        y = 10 + i*82
        d.box(20, y, 600, 52, [(t,'t'),(s_,'s')], c)
        if i < 3: d.arrow([(320,y+52),(320,y+82)], 'n', label='then', at=(380,y+67))
    return d

def build_s3_in_depth():
    body = ''
    body += see(figure(d_classes(),
        'S3 has several <b>storage classes</b> — one price tag for how often you read the data. <b>Standard</b> is for data you use often. <b>Intelligent-Tiering</b> is for data with an unknown or changing pattern; it moves objects for you. '
        '<b>Infrequent Access</b> is cheaper to store but costs more per read. The <b>Glacier</b> classes are archives: cheap to keep, slower and costlier to read, some needing a restore first. The durability design is the same across them; the trade is access speed and cost.'))
    body += one('S3 is cheap and durable when you match each object to the right class, keep the bucket private, and let lifecycle rules do the housekeeping.')
    body += why([
      'The Storage page said S3 is your default for files. Real buckets grow for years, and most of what is in them stops being read. Paying "hot" prices for cold data is the most common S3 waste. And a bucket that is too open is the most common S3 leak.',
      'So S3 comes with levers: <b>storage classes and lifecycle rules</b> for cost, <b>versioning</b> for mistakes, <b>presigned URLs</b> for sharing, and <b>Block Public Access</b> for safety.'])
    body += block('🧰 The levers', pick_cards([
      dict(icon='🔥', name='Standard and Intelligent-Tiering', tag='the hot end', color='#34d399',
           use=['Standard: data accessed frequently, millisecond reads', 'Intelligent-Tiering: unknown or changing access; it moves objects between tiers and charges a small monitoring fee per object'],
           skip=['Very small objects in Intelligent-Tiering — those below a minimum size are not monitored']),
      dict(icon='🧊', name='Infrequent Access classes', tag='the middle', color='#a78bfa',
           use=['Data you read rarely but need instantly', 'One Zone-IA costs less but keeps data in a single zone'],
           skip=['One Zone-IA for data you cannot lose to a zone-level disaster']),
      dict(icon='🏔️', name='Glacier classes', tag='archives', color='#fbbf24',
           use=['Instant Retrieval: archives you still read in milliseconds', 'Flexible Retrieval: archive data read about once a year, minutes to hours', 'Deep Archive: read less than once a year, hours to restore'],
           skip=['Anything you may need right now — archived objects may need a restore first']),
      dict(icon='⏳', name='Lifecycle rules', tag='automatic transitions and expiry', color='#22d3ee',
           use=['Move objects to another class as they age', 'Expire objects (and old versions) you no longer need', 'Essential once versioning is on'],
           skip=['Forgetting minimum storage durations — early deletes can still be billed']),
    ]), label_cls='see')
    body += block('🔗 Sharing without opening the bucket', figure(d_presign(),
        'a <b>presigned URL</b> is a link your app signs using its own permissions. It lets one person do one thing (for example, download one object) until it expires. The bucket stays private and Block Public Access stays on. '
        'The link works for anyone who holds it, as many times as they like, until it expires — so keep the lifetime short. If the role that signed it is deleted, the URL stops working.'), label_cls='see')
    body += block('🛡️ Keep it safe and tidy', figure(d_safe(),
        'four layers, outermost first. <b>Block Public Access</b> (on by default for new buckets) keeps the bucket off the open internet. <b>IAM and bucket policies</b> give each role only what it needs. <b>Versioning</b> lets you undo overwrites and deletes, and <b>lifecycle rules</b> keep the cost under control — without them, every old version is kept forever.'), label_cls='see')
    body += block('📊 Choosing a class', table(['Class family','Read pattern','Access speed','Watch out for'], [
      ['Standard','Frequently','Milliseconds','Highest storage price of the family'],
      ['Intelligent-Tiering','Unknown or changing','Automatic tiers','Per-object monitoring fee; small objects not monitored'],
      ['Infrequent Access','Rarely, but instantly when needed','Milliseconds','Retrieval charges and minimum duration'],
      ['Glacier Flexible Retrieval','About once a year','Minutes to hours','Needs a restore request'],
      ['Glacier Deep Archive','Less than once a year','Hours','Longest minimum duration'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('📸','User photos: hot for a week, then rarely','Access pattern changes with age.','Lifecycle: Standard → Infrequent Access'),
      ('🧾','Tax records kept for years','Almost never read.','Glacier archive class'),
      ('🧪','New data of unknown popularity','No idea what will be read.','Intelligent-Tiering'),
      ('📤','A customer needs to download one invoice','The bucket must stay private.','A presigned URL with a short expiry'),
      ('🗑️','A script overwrites the wrong files','They were the only copy.','Versioning, with lifecycle for old versions'),
      ('🔓','A public bucket is found in an audit','Customer data was exposed.','Block Public Access and least-privilege policies'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — details that cost money or data', '''      <p><b>Durability design.</b> AWS publishes a very high durability design for the main classes — but durability does not protect against deletion by an authorized user or process. Versioning and Object Lock cover that gap.</p>
      <p><b>Minimum durations.</b> Some archive classes have minimum storage durations (for example, Glacier Instant Retrieval 90 days and Deep Archive 180 days). Deleting earlier can still be billed for the minimum.</p>
      <p><b>Versioning without lifecycle</b> can lead to unbounded storage growth, because every modification creates a new version that is kept indefinitely.</p>
      <p><b>Presigned URLs</b> are generated with the SDK or CLI, can grant GET or PUT, and are valid up to a maximum of seven days. They can be used many times until they expire.</p>
      <p><b>Block Public Access.</b> Buckets created since April 2023 block all public access by default. AWS recommends keeping all four settings on unless you know you need otherwise. A presigned URL does not require turning it off.</p>''')
    body += recall([
      'S3 classes trade storage price against access speed and retrieval cost: Standard → Intelligent-Tiering → Infrequent Access → Glacier → Deep Archive.',
      'Lifecycle rules transition and expire objects; essential with versioning.',
      'Presigned URL: a time-limited signed link; the bucket stays private; anyone with the link can use it until expiry.',
      'Block Public Access on; least-privilege IAM and bucket policies; versioning for mistakes.',
      'High durability ≠ protection from deletion.'])
    body += saythis('"I match each S3 object to a storage class by how often it is read and let lifecycle rules move data as it ages — Intelligent-Tiering when the pattern is unknown. '
      'Buckets stay private with Block Public Access on and least-privilege policies; I share single objects with short-lived presigned URLs, and I turn on versioning with lifecycle for old versions so mistakes are recoverable."')
    body += trap([
      '<b>Turning on versioning and forgetting lifecycle rules.</b> Every overwrite keeps a new version forever, and the bill grows quietly.',
      'Second trap: <b>making a bucket public to share one file.</b> A presigned URL does the job with a time limit and without opening everything.'])
    body += confuse('🧊 Infrequent Access', 'Rarely read, but instantly available when needed. Retrieval is billed.', '🏔️ Glacier archive', 'Archive for data you almost never need. Some classes require a restore before you can read.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># make a link that lets someone download one object for one hour</span>
aws s3 presign s3://my-example-bucket-12345/reports/report.pdf --expires-in 3600''',
      'Illustrative shape only — the bucket and key are examples, and the 3600 seconds (one hour) is an example expiry.'))
    body += next_box('That is S3 in depth. Back to the Storage page for the big picture — and on to the next concept: Databases.', 'storage.html', 'Back to Storage')
    body += fact_note(FOOT, [DOCS_S3, DOCS_CLS, ('S3 presigned URLs', 'https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html'), ('S3 Block Public Access', 'https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html')])
    return page('s3-in-depth', 'S3 in Depth', 'Deep dive · Storage · 🪣 S3',
        'S3 stays cheap and safe when you <span class="grad-text">match data to a storage class, keep the bucket private and let lifecycle rules tidy up.</span>',
        'Storage classes, lifecycle rules, versioning, presigned URLs and Block Public Access.',
        'How do S3 storage classes and lifecycle rules work, and how do you share a file safely?',
        body, CR + ['<a href="storage.html">Storage</a>', '<span class="cur">S3 in Depth</span>'], '', search_title='S3 in Depth')
