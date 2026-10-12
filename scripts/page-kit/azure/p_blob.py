from kit import *
from p_storage import CR, DOCS_ST

def d_anatomy():
    d = Diagram('bl1', 640, 282, 'Anatomy of a blob URL, and where each part lives: storage account, container, blob')
    segs = [('https://',76,'n','protocol'), ('myaccount',90,'cyan','storage account'), ('.blob.core.windows.net',180,'violet','Blob service endpoint'),
            ('/photos',84,'amber','container'), ('/cat.jpg',88,'emerald','blob (file) name')]
    x = 53
    for t, w, col, lab in segs:
        d.box(x, 12, w, 34, [(t,'u')], col)
        d.text(x + w/2, 62, lab, size=8.5)
        x += w + 4
    d.zone(10, 78, 620, 188, 'cyan', 'STORAGE ACCOUNT  ·  myaccount')
    conts = [(24,'photos',['cat.jpg','dog.png','2025/trip.jpg'],'block blob'),
             (224,'backups',['db-jan.bak','db-feb.bak','db-mar.bak'],'block blob'),
             (424,'logs',['app.log','web.log','api.log'],'append blob')]
    for cx, name, blobs, typ in conts:
        d.zone(cx, 104, 192, 150, 'amber', f'CONTAINER  ·  {name}')
        for i, b in enumerate(blobs):
            d.box(cx + 12, 136 + i*38, 168, 32, [(b,'t')] if False else [(b,'b'),(typ,'s')], 'emerald')
    return d

def d_sas_flow():
    d = Diagram('bl2', 640, 332, 'Upload flow: browser asks the API for a SAS link, uploads straight to Blob, Event Grid triggers a function that saves a thumbnail')
    d.box(10, 30, 110, 60, [('📱 Browser','t'),("the user's app",'s')], 'n')
    d.box(300, 30, 130, 60, [('⚙️ Your API','t'),('decides who may upload','s')], 'violet')
    d.text(470, 60, 'SAS link = a temporary web address', size=9.5, anchor='start')
    d.text(470, 76, 'with limited rights (e.g. one upload)', size=9.5, anchor='start')
    d.box(10, 210, 110, 60, [('📦 Blob','t'),('container "photos"','s')], 'cyan')
    d.box(300, 210, 130, 60, [('⚡ Event Grid','t'),('routes events','s')], 'emerald')
    d.box(520, 210, 110, 60, [('λ Function','t'),('makes thumbnails','s')], 'violet')
    d.arrow([(120,48),(300,48)], 'cyan', label='1 · asks to upload', at=(210,48))
    d.arrow([(300,72),(120,72)], 'amber', label='2 · sends a SAS link', at=(210,72))
    d.arrow([(65,90),(65,210)], 'cyan', label='3 · uploads straight to Blob, using the SAS link', at=(205,150))
    d.arrow([(120,240),(300,240)], 'emerald', label='4 · BlobCreated event', at=(210,240))
    d.arrow([(430,240),(520,240)], 'emerald', label='5 · push', at=(475,240))
    d.arrow([(575,270),(575,308),(65,308),(65,270)], 'violet', label='6 · saves the thumbnail back to Blob', at=(320,308))
    return d

def d_tiers():
    d = Diagram('bl3', 640, 304, 'Blob access tiers Hot, Cool, Cold and Archive, with minimum stay and a lifecycle rule moving blobs down over time')
    tiers = [(10,'rose','🔥 Hot',['read often','no minimum stay','instant access']),
             (170,'cyan','🌤️ Cool',['read now and then','stay at least 30 days','instant access']),
             (330,'violet','🧊 Cold',['rarely read','stay at least 90 days','instant access']),
             (490,'n','🗄️ Archive',['almost never read','stay at least 180 days','offline: hours to restore'])]
    for x, col, name, lines in tiers:
        d.box(x, 22, 140, 108, [(name,'t')] + [(l,'s') for l in lines], col)
    d.arrow([(80,130),(80,170),(560,170),(560,130)], 'n', label='a lifecycle rule moves blobs down as they go cold', at=(325,170))
    d.add('<defs><linearGradient id="bl3g1" x1="0" x2="1"><stop offset="0" stop-color="#fb7185"/><stop offset="1" stop-color="#34d399"/></linearGradient>'
          '<linearGradient id="bl3g2" x1="0" x2="1"><stop offset="0" stop-color="#34d399"/><stop offset="1" stop-color="#fb7185"/></linearGradient></defs>')
    d.text(10, 214, 'Price to STORE it (per GB)', anchor='start', size=10, weight=600)
    d.add('<rect x="10" y="222" width="620" height="18" rx="9" fill="url(#bl3g1)" opacity=".75"/>')
    d.add('<text x="26" y="235" text-anchor="start" font-size="9" font-weight="700" fill="#0a0d14">highest (Hot)</text>')
    d.add('<text x="614" y="235" text-anchor="end" font-size="9" font-weight="700" fill="#0a0d14">lowest (Archive)</text>')
    d.text(10, 262, 'Price to READ it', anchor='start', size=10, weight=600)
    d.add('<rect x="10" y="270" width="620" height="18" rx="9" fill="url(#bl3g2)" opacity=".75"/>')
    d.add('<text x="26" y="283" text-anchor="start" font-size="9" font-weight="700" fill="#0a0d14">lowest (Hot)</text>')
    d.add('<text x="614" y="283" text-anchor="end" font-size="9" font-weight="700" fill="#0a0d14">highest (Archive)</text>')
    return d

def build_blob_storage():
    body = ''
    body += see(figure(d_anatomy(),
        'a blob\'s web address tells you exactly where it lives. Read it from left to right: the <b>storage account</b> name, the <b>Blob service</b> endpoint, the <b>container</b>, and the <b>blob name</b>. '
        'Below, the same colors show the real nesting — an account holds containers, and containers hold blobs. '
        'Notice <code>2025/trip.jpg</code>: that slash is just part of the name, not a real folder (more on that in the trap below).'))
    body += one('A blob is a file with a web address, kept in a container, inside a storage account — and the cooler it gets, the cheaper it is to keep.')
    body += why([
      'On the Storage page you met the four doors. Blob is the one almost every app opens first, because almost every app has <b>files</b>: photos, PDFs, videos, backups, logs.',
      'A normal disk cannot do this job well. It fills up and you must resize it, it belongs to one machine, and it cannot hand a file to a user on the other side of the world. '
      '<b>Object storage</b> fixes all three: there is no disk to manage, the amount of data can grow very large, and every object gets its own web address that any permitted app can use.'])
    body += block('🧱 The three kinds of blob', '''    <div class="taxonomy-strip">
      <div class="tax-item"><h5>🟦 Block blob</h5><p>The normal one. Photos, documents, videos, backups. Big files are uploaded in pieces ("blocks") and joined. <b>Choose this unless you have a reason not to.</b></p></div>
      <div class="tax-item"><h5>➕ Append blob</h5><p>You can only add to the end. Perfect for log files: write a new line, never change an old one.</p></div>
      <div class="tax-item"><h5>💽 Page blob</h5><p>Fast random reading and writing in the middle of the file. This is what virtual-machine disks use under the hood.</p></div>
    </div>''', label_cls='see')
    body += block('🎬 Real scenario: users upload profile photos', figure(d_sas_flow(),
        'your website lets users upload a photo. The browser asks your API for permission (1). The API checks who the user is and returns a <b>SAS link</b> (2) — a temporary web address that allows exactly one upload, for a few minutes. '
        'The browser then sends the file <b>straight to Blob Storage</b> (3), so your API never carries the heavy file. When the file lands, Blob Storage publishes a <b>BlobCreated</b> event (4). '
        'Event Grid pushes it (5) to a Function, which makes a small thumbnail and saves it back (6).') +
        '\n    <div class="kd-card" style="margin-top:16px"><b>Why this design?</b> Your API stays small and fast because the file bytes skip it. The SAS link is short-lived and limited, so a leaked link stops working soon. '
        'And the thumbnail step is <em>event-driven</em>: nothing polls, the event simply arrives (you will meet Event Grid properly in the Messaging concept).</div>', label_cls='see')
    body += block('💰 Save money: access tiers', figure(d_tiers(),
        'every blob sits in a tier. <b>Hot</b> costs the most to store but the least to read — for data you touch daily. As data goes cold, storing it gets cheaper, but reading it costs more, and each cooler tier has a <b>minimum stay</b> '
        '(delete or move early and you pay an early-deletion fee). <b>Archive</b> is <em>offline</em>: you must restore ("rehydrate") a blob to a warmer tier first, which takes hours. '
        'A <b>lifecycle management rule</b> can move blobs down automatically — the 30 / 90 / 180 days here are just an example rule.') +
        '\n' + table(['Tier','Best for','Minimum stay','Can you read it right away?'], [
          ['Hot','data used all the time','none','yes'],
          ['Cool','backups and older files read now and then','30 days','yes'],
          ['Cold','rarely read, but must be online','90 days','yes'],
          ['Archive','compliance copies you hope never to open','180 days','no — restore takes hours'],
        ]), label_cls='see')
    body += block('✅ When to use Blob — real examples', scenarios([
      ('🌐','Static website','HTML, CSS and images served straight from storage — no web server to run.','Blob static website'),
      ('💾','Database backups','Nightly backup files, kept 30 days online, then moved to a cheaper tier.','Blob + lifecycle rule'),
      ('🎞️','Video library','Large files streamed to customers. Often put behind a CDN.','Blob'),
      ('🧾','Log archive','Application logs appended all day, rarely read after a month.','Append blob + Cool/Archive'),
      ('📊','Data lake','Raw files for analytics jobs that need real folders and file permissions.','Blob with hierarchical namespace (Data Lake Gen2)'),
      ('⬇️','App downloads','Installers and update packages anyone with the link may download.','Blob'),
    ]), label_cls='see')
    body += block('⚖️ Strengths and limits', proscons('Blob Storage at a glance',
      ['Very low cost per GB, and cheaper still in cooler tiers', 'Grows to very large amounts of data without disks to manage', 'Redundancy from LRS up to geo-zone-redundant (see Storage)', 'Publishes events (like BlobCreated) so other services can react',
       'Works with Entra ID, RBAC and short-lived SAS links'],
      ['It stores files, it does not search inside them — use a database or analytics tool for that', 'No true folders unless you turn on the hierarchical namespace',
       'Each read/write operation is billed, and Archive reads are slow', 'A public container or a leaked SAS link exposes data — keep public access off unless you truly need it',
       'Not a mounted drive — for that, use Azure Files']), label_cls='see')
    body += block('🔐 Keep it locked down — quick checklist', '''    <div class="taxonomy-strip">
      <div class="tax-item"><h5>1 · Private by default</h5><p>Keep anonymous public access off unless the files are meant for everyone.</p></div>
      <div class="tax-item"><h5>2 · Entra ID first</h5><p>Give your app an identity and an RBAC role. If you need a SAS, prefer a <b>user delegation SAS</b> (signed with Entra credentials, not the account key).</p></div>
      <div class="tax-item"><h5>3 · Short expiry</h5><p>Make SAS links last minutes, not months, and give them only the permission needed.</p></div>
      <div class="tax-item"><h5>4 · Undo button</h5><p>Turn on soft delete and versioning so a mistake can be rolled back. Use immutable (write-once) storage for rules that forbid changes.</p></div>
    </div>''', label_cls='see')
    body += recall([
      'URL = https://&lt;account&gt;.blob.core.windows.net/&lt;container&gt;/&lt;blob name&gt;. Account → containers → blobs.',
      'Three blob types: block (normal files), append (logs), page (VM disks / random access).',
      'Tiers: Hot → Cool (30 days) → Cold (90 days) → Archive (180 days, offline). Cooler = cheaper to store, dearer to read.',
      'Let browsers upload with a short-lived SAS link so files skip your API. Prefer user delegation SAS.',
      'A lifecycle management rule moves or deletes blobs automatically by age.',
      'Data Lake Storage Gen2 = Blob with the hierarchical namespace turned on.'])
    body += saythis('"Blob Storage is Azure\'s object store. Data lives as blobs in containers inside a storage account, addressed by URL. I use block blobs for ordinary files, append blobs for logs and page blobs for disks. '
      'To control cost I use access tiers — Hot, Cool, Cold and Archive — and a lifecycle policy to move data down automatically. For uploads from browsers I issue a short-lived user delegation SAS, so files go straight to storage."')
    body += trap([
      '<b>Folders in Blob are just part of the name.</b> <code>2025/trip.jpg</code> looks like a file in a folder, but without the hierarchical namespace there are no real folders — "renaming a folder" means copying every blob. '
      'If you need real folders, rename operations or file-style permissions, enable the hierarchical namespace (Data Lake Storage Gen2) when you create the account.',
      'Second trap: a SAS link is a password in URL form. Anyone who has it can use it until it expires — so keep the lifetime short and the permission small.'])
    body += confuse('📦 Blob Storage (flat)', 'A flat list of blobs per container. The slash in a name is only a naming convention.', '🗂️ Data Lake Storage Gen2', 'The same Blob service with the hierarchical namespace on: real directories, atomic renames, file-style permissions.')
    body += zoom('💻 Tiny illustrative example — make a short-lived upload link', code_block(
'''<span class="kw">from</span> datetime <span class="kw">import</span> datetime, timedelta, timezone
<span class="kw">from</span> azure.identity <span class="kw">import</span> DefaultAzureCredential
<span class="kw">from</span> azure.storage.blob <span class="kw">import</span> BlobServiceClient, BlobSasPermissions, generate_blob_sas

service = BlobServiceClient(<span class="str">"https://myaccount.blob.core.windows.net"</span>, credential=DefaultAzureCredential())
now = datetime.now(timezone.utc)
key = service.get_user_delegation_key(now, now + timedelta(minutes=<span class="num">15</span>))   <span class="cmt"># signed with Entra, not the account key</span>

sas = generate_blob_sas(account_name=<span class="str">"myaccount"</span>, container_name=<span class="str">"photos"</span>, blob_name=<span class="str">"u42/cat.jpg"</span>,
                        user_delegation_key=key, permission=BlobSasPermissions(create=<span class="kw">True</span>, write=<span class="kw">True</span>),
                        expiry=now + timedelta(minutes=<span class="num">10</span>))
upload_url = <span class="str">f"https://myaccount.blob.core.windows.net/photos/u42/cat.jpg?{sas}"</span>   <span class="cmt"># hand this to the browser</span>''',
      'Illustrative shape only — real code also validates the user, picks a safe blob name and handles errors. Check the current SDK docs for exact signatures.'))
    body += next_box('That is Blob in depth. Back to the big picture: the Storage page shows how Blob fits with Files, Queues and Tables — and from there the journey moves on to Databases.', 'storage.html', 'Back to Storage')
    body += fact_note('Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official docs.',
        [('Blob Storage documentation', 'https://learn.microsoft.com/en-us/azure/storage/blobs/'), DOCS_ST])
    return page('blob-storage', 'Blob Storage in Depth', 'Deep dive · Storage · 📦 Blob',
        'A blob is <span class="grad-text">a file with a web address</span> — and the colder it gets, the cheaper it is to keep.',
        'Blob Storage is where most apps keep their files. Learn how a blob is addressed, which of the three blob types to pick, how a browser can upload safely, '
        'and how access tiers turn "old files" into savings.',
        'When would you use Azure Blob Storage, and how do access tiers and SAS links work?',
        body, CR + ['<a href="storage.html">Storage</a>', '<span class="cur">Blob in depth</span>'], '', search_title='Blob Storage in Depth')
