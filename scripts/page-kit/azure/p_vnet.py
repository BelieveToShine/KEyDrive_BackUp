from kit import *
from p_storage import CR

DOCS_VNET = ('Azure Virtual Network documentation', 'https://learn.microsoft.com/en-us/azure/virtual-network/')
DOCS_PL = ('Azure Private Link documentation', 'https://learn.microsoft.com/en-us/azure/private-link/')
DOCS_NET = ('Azure networking documentation', 'https://learn.microsoft.com/en-us/azure/networking/')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official docs.'

def d_vnet():
    d = Diagram('vn1', 640, 332, 'A virtual network with a web subnet and a data subnet; network security groups let HTTPS reach the web servers and only the web subnet reach the database, and the internet cannot reach the database directly')
    d.box(10, 78, 96, 56, [('🌍 Internet','t'),('users','s')], 'n')
    d.zone(150, 8, 480, 316, 'violet', 'VIRTUAL NETWORK · 10.0.0.0/16 (example range)')
    d.zone(166, 40, 448, 120, 'cyan', 'SUBNET · web · 10.0.1.0/24')
    d.box(180, 78, 170, 56, [('🛡️ NSG','t'),('allow HTTPS (443)','s')], 'amber')
    d.box(440, 78, 160, 56, [('🖥️ Web servers','t'),('the app tier','s')], 'cyan')
    d.zone(166, 184, 448, 120, 'emerald', 'SUBNET · data · 10.0.2.0/24')
    d.box(180, 222, 170, 56, [('🛡️ NSG','t'),('allow SQL from web only','s')], 'amber')
    d.box(440, 222, 160, 56, [('🛢️ Database','t'),('the data tier','s')], 'emerald')
    d.arrow([(106,106),(180,106)], 'cyan', label='HTTPS', at=(143,106))
    d.arrow([(350,106),(440,106)], 'cyan', label='allowed', at=(395,106))
    d.arrow([(450,134),(450,172),(340,172),(340,222)], 'emerald', label='SQL 1433', at=(395,172))
    d.arrow([(350,250),(440,250)], 'emerald', label='allowed', at=(395,250))
    d.arrow([(58,134),(58,250),(180,250)], 'rose', label='no direct path', at=(119,250), dash=True)
    return d

def d_nsg():
    d = Diagram('vn2', 640, 336, 'How a network security group checks rules from the lowest priority number up and stops at the first match: RDP from the internet matches the deny rule at 200')
    d.box(10, 14, 150, 56, [('📨 Traffic','t'),('from the Internet','s'),('to TCP port 3389','s')], 'n')
    d.arrow([(160,42),(250,42)], 'cyan', label='arrives', at=(205,42))
    d.box(250, 14, 290, 44, [('100 · Allow · TCP 443','t'),('from the Internet — no match','s')], 'n')
    d.box(250, 94, 290, 44, [('200 · Deny · TCP 3389','t'),('MATCH → denied, search stops','s')], 'rose')
    d.box(250, 174, 290, 44, [('65000 · Allow · from the virtual network','t'),('default rule — never reached','s')], 'n')
    d.box(250, 254, 290, 44, [('65500 · Deny all inbound','t'),('default rule — never reached','s')], 'n')
    for y in (58, 138, 218):
        d.arrow([(395,y),(395,y+36)], 'n', label='no match' if y == 58 else 'next', at=(458,y+18))
    d.text(10, 130, 'Rules run from the', anchor='start', size=9.5)
    d.text(10, 146, 'lowest number up.', anchor='start', size=9.5)
    d.text(10, 170, 'The first match', anchor='start', size=9.5, weight=700)
    d.text(10, 186, 'wins — and stops.', anchor='start', size=9.5, weight=700)
    d.text(320, 322, 'Your own rules use priorities 100 to 4096. The built-in defaults sit at 65000 and above.', size=9.5)
    return d

def d_peering():
    d = Diagram('vn3', 640, 214, 'Virtual network peering connects two networks directly and is not transitive: A and B are peered and B and C are peered, but A cannot reach C through B')
    d.box(10, 88, 140, 70, [('🕸️ VNet A','t'),('10.0.0.0/16','s')], 'cyan')
    d.box(250, 88, 140, 70, [('🕸️ VNet B','t'),('10.1.0.0/16','s')], 'cyan')
    d.box(490, 88, 140, 70, [('🕸️ VNet C','t'),('10.2.0.0/16','s')], 'cyan')
    d.arrow([(150,123),(250,123)], 'cyan', label='peered', at=(200,123), both=True)
    d.arrow([(390,123),(490,123)], 'cyan', label='peered', at=(440,123), both=True)
    d.arrow([(80,88),(80,40),(560,40),(560,88)], 'rose', label='A cannot reach C through B', at=(320,40), dash=True)
    d.text(320, 192, 'To let A talk to C, peer A with C directly. Address ranges must not overlap.', size=9.5, weight=700)
    return d

def build_virtual_networks():
    body = ''
    body += see(figure(d_vnet(),
        'a <b>virtual network</b> is your own private network in Azure, with an address range you choose. You slice it into <b>subnets</b> — here a web subnet and a data subnet — and put a <b>network security group (NSG)</b> at each door. '
        'The web NSG lets HTTPS in from the internet. The data NSG lets SQL in <em>only from the web subnet</em>. So the internet can reach the web servers, the web servers can reach the database, and nobody on the internet can reach the database directly.'))
    body += one('A virtual network is a private, fenced-off corner of Azure. Subnets split it into zones, and network security groups are the doors with rules: who may come in, from where, on which port.')
    body += why([
      'Identity decides who may <i>ask</i> Azure to do things. The network decides what can physically <i>reach</i> what. A database with a public address that anyone on the internet can try to connect to is a risk, even behind a strong password — the best protection is that it cannot be reached at all.',
      'A <b>virtual network</b> gives your resources private addresses and a boundary. <b>Subnets</b> let you separate tiers (web, app, data). <b>NSGs</b> add simple allow-or-deny rules. Together they turn "everything can talk to everything" into "only the paths I planned".'])
    body += block('📖 The words you need', '''    <div class="taxonomy-strip">
      <div class="tax-item"><h5>🕸️ Virtual network (VNet)</h5><p>Your private network in Azure. It lives in one region and one subscription, and it can span the availability zones of that region. Networks in different regions connect through peering.</p></div>
      <div class="tax-item"><h5>🔢 Address space</h5><p>The range of private IP addresses the VNet uses, written like <code>10.0.0.0/16</code>. Use private ranges, and pick ranges that will not overlap other networks you may connect later.</p></div>
      <div class="tax-item"><h5>🧱 Subnet</h5><p>A slice of the address space. NSGs and route tables attach to subnets. Azure reserves five addresses in every subnet, so very small subnets run out quickly.</p></div>
      <div class="tax-item"><h5>🛡️ Network security group</h5><p>A list of allow and deny rules for traffic by source, destination, port and protocol. Associate one with every subnet.</p></div>
      <div class="tax-item"><h5>🤝 Peering</h5><p>A direct, private link between two VNets so their resources can talk to each other.</p></div>
      <div class="tax-item"><h5>🔌 Private endpoint</h5><p>A private IP address in your subnet that points at an Azure service such as storage or SQL. Explained in the deep dive below.</p></div>
    </div>''', label_cls='see')
    body += block('🚦 How an NSG decides', figure(d_nsg(),
        'imagine remote-desktop traffic (port 3389) arriving from the internet. Azure checks the rules <b>from the lowest priority number upward</b>. Rule 100 allows HTTPS only — no match, so it moves on. Rule 200 denies port 3389 — <b>match</b>, so the traffic is denied and the search <b>stops</b>. The rules further down are never looked at. '
        'Azure also adds default rules (priority 65000 and higher) that you cannot delete but can override with your own, lower-numbered rules.'), label_cls='see')
    body += block('🔗 Ways to connect things', pick_cards([
      dict(icon='🌍', name='Public internet', tag='a public IP address on the resource', color='#fb7185',
           use=['Things meant for everyone: a public website or API', 'Quick experiments'],
           skip=['Databases, storage with private data and admin ports → keep them private']),
      dict(icon='🤝', name='VNet peering', tag='a direct link between two virtual networks', color='#22d3ee',
           use=['Two networks (for example Dev and Shared services) must talk privately', 'You want a simple, direct connection'],
           skip=['You expect traffic to pass through a middle network — peering is not transitive']),
      dict(icon='🏢', name='VPN gateway or ExpressRoute', tag='connect Azure to your office or datacenter', color='#a78bfa',
           use=['An on-premises network must reach Azure resources privately', 'A VPN is an encrypted tunnel over the internet; ExpressRoute is a private connection through a provider'],
           skip=['Everything is already in Azure → peering or private endpoints are enough']),
      dict(icon='🔌', name='Private endpoint', tag='a private IP for an Azure service', color='#34d399',
           use=['Reach Azure Storage, SQL and others without the public internet', 'Turn off the service\'s public access'],
           skip=['You only need a quick subnet allow-list → a service endpoint can be enough (see the deep dive)']),
    ]), label_cls='see')
    body += block('🤝 Peering is not transitive', figure(d_peering(),
        'peering links two networks <b>directly</b>. A is peered with B, and B is peered with C — but that does <em>not</em> let A reach C through B. Each path you need must be peered explicitly. '
        'Also remember that peered networks must have address ranges that do not overlap, so plan your ranges before you build.'), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🛒','Website with a hidden database','Users reach the site. The database must never be reachable from the internet.','Web subnet + data subnet + NSGs'),
      ('🧪','Dev and Prod, shared logging','Two VNets must send logs to a shared network, privately.','VNet peering'),
      ('🏢','Office needs the Azure database','Staff on the corporate network must connect privately.','VPN gateway or ExpressRoute'),
      ('🔌','App to storage, no internet','The web app must reach Blob Storage without a public path.','Private endpoint'),
      ('🚫','Block remote desktop from the internet','Port 3389 must never be open to everyone.','An NSG deny rule (or no public IP)'),
      ('🧮','Planning address ranges','Three teams each build a VNet and later want to connect them.','Non-overlapping ranges, planned up front'),
    ]), label_cls='see')
    body += block('🔬 Go deeper', deep_cards([('Deep dive · Virtual Networks', 'Private endpoints vs service endpoints', 'How to reach Azure Storage or SQL from your network without the public internet — and the DNS detail that trips everybody up.', 'private-endpoints.html')]), label_cls='next')
    body += recall([
      'A VNet is your private network: one region, one subscription, can span zones. Subnets slice it; NSGs and route tables attach to subnets.',
      'NSG rules run from the lowest priority number up (custom 100–4096; defaults 65000+); the first match wins and stops. Default rules cannot be deleted, only overridden.',
      'Azure reserves five addresses in each subnet.',
      'Peering is a direct link and is not transitive; address ranges must not overlap.',
      'Use private endpoints to reach Azure services privately; plan your address ranges first.'])
    body += saythis('"A virtual network is a private network scoped to a region and subscription. I split it into subnets by tier and attach a network security group to each, with allow rules for what is needed and a deny for the rest — rules are evaluated from the lowest priority number and the first match wins. '
      'I connect networks with peering, remembering it is not transitive, and I reach PaaS services privately with private endpoints."')
    body += trap([
      '<b>The default rules are friendlier than you think.</b> Traffic inside the virtual network — and from networks connected to it — is allowed by a default rule. If two subnets must <i>not</i> talk to each other, add your own deny rule with a lower number.',
      'Second trap: <b>peering is not transitive.</b> Peering A–B and B–C does not connect A to C. Plan each path, or use a central network design (a later concept).'])
    body += confuse('🕸️ Virtual network', 'The whole private network and its address range. Lives in one region.', '🧱 Subnet', 'A slice of the network. This is where you attach NSGs and route tables, and where resources get their addresses.')
    body += zoom('💻 Tiny illustrative examples', code_block(
'''<span class="cmt"># a network with one subnet</span>
az network vnet create --name vnet-shop --resource-group rg-shop-prod \\
    --address-prefixes 10.0.0.0/16 --subnet-name web --subnet-prefixes 10.0.1.0/24

<span class="cmt"># a rule: allow HTTPS in (priority 100 = checked first)</span>
az network nsg rule create --nsg-name nsg-web --resource-group rg-shop-prod \\
    --name allow-https --priority 100 --direction Inbound --access Allow \\
    --protocol Tcp --destination-port-ranges 443''',
      'Illustrative shape only — real setups are written as templates (Bicep) and add more rules, route tables and diagnostics.'))
    body += next_box('You have a safe network. Now it needs something to run: servers, containers, or just code. Next: <b>Compute</b> — and how to choose how much you want to manage.', 'compute.html', 'Compute')
    body += fact_note(FOOT, [DOCS_VNET, DOCS_PL, DOCS_NET])
    return page('virtual-networks', 'Virtual Networks', 'Concept 4 of 19 · 🏗️ Foundations',
        'A virtual network is <span class="grad-text">your private, fenced-off corner</span> of Azure — you decide who gets in and who talks to whom.',
        'Without a network plan, every resource could be reachable from everywhere. Learn how VNets, subnets and security groups build a safe layout, how NSG rules are checked, and how peering connects networks.',
        'What is an Azure virtual network, and how do subnets, NSGs, peering and private endpoints work together?',
        body, CR + ['<span class="cur">Virtual Networks</span>'], '', search_title='Virtual Networks')

# ======================================================================= deep dive
def d_paths():
    d = Diagram('pe1', 640, 316, 'Reaching storage over its public address through the internet versus through a private endpoint that has a private IP address in your subnet')
    d.zone(10, 8, 305, 300, 'rose', 'PUBLIC PATH · over the internet')
    d.box(100, 40, 120, 48, [('💻 Your app','t'),('in your VNet','s')], 'n')
    d.box(100, 136, 120, 48, [('🌍 Internet','t'),('public IP address','s')], 'rose')
    d.box(60, 232, 200, 48, [('🗂️ Storage account','t'),('its public endpoint','s')], 'n')
    d.arrow([(160,88),(160,136)], 'rose', label='goes to a public IP', at=(235,112))
    d.arrow([(160,184),(160,232)], 'rose', label='reaches the service', at=(235,208))
    d.zone(325, 8, 305, 300, 'emerald', 'PRIVATE PATH · a private endpoint')
    d.box(415, 40, 120, 48, [('💻 Your app','t'),('in your VNet','s')], 'n')
    d.box(395, 136, 160, 48, [('🔌 Private endpoint','t'),('10.0.3.4 in your subnet','s')], 'emerald')
    d.box(375, 232, 200, 48, [('🗂️ Storage account','t'),('reached over Private Link','s')], 'n')
    d.arrow([(475,88),(475,136)], 'emerald', label='goes to a private IP', at=(545,112))
    d.arrow([(475,184),(475,232)], 'emerald', label='Private Link', at=(540,208))
    return d

def d_dns():
    d = Diagram('pe2', 640, 270, 'DNS decides the path: without a private DNS zone the storage name resolves to a public IP; with one it resolves to the private endpoint address')
    d.box(10, 107, 100, 56, [('💻 Your app','t'),('wants the name','s')], 'n')
    d.box(200, 107, 110, 56, [('📖 DNS','t'),('name → an IP','s')], 'amber')
    d.box(470, 36, 160, 56, [('🌍 Public IP','t'),('over the internet','s')], 'rose')
    d.box(470, 178, 160, 56, [('🔒 10.0.3.4','t'),('your private endpoint','s')], 'emerald')
    d.arrow([(110,135),(200,135)], 'amber', label='asks', at=(155,135))
    d.arrow([(310,135),(350,135),(350,64),(470,64)], 'rose', label='public answer', at=(410,64))
    d.arrow([(310,135),(350,135),(350,206),(470,206)], 'emerald', label='private answer', at=(410,206))
    d.text(240, 56, 'Name: mystorage.blob.core.windows.net', anchor='middle', size=9, mono=True)
    d.text(240, 250, 'With a private DNS zone the answer is private.', anchor='middle', size=9.5, weight=700)
    return d

def build_private_endpoints():
    body = ''
    body += see(figure(d_paths(),
        '<b>Left:</b> your app reaches a storage account by its public address, so the traffic goes out and back over the internet path. '
        '<b>Right:</b> a <b>private endpoint</b> is a network interface with a <b>private IP address inside your own subnet</b>. Your app connects to that private address, and <b>Private Link</b> carries the connection to the storage account. '
        'With a private endpoint in place you can also turn off the storage account\'s public access.'))
    body += one('A private endpoint gives an Azure service a private IP address inside your own network — so your app reaches it privately, and you can close its public door.')
    body += why([
      'The Virtual Networks page showed how to keep <i>your</i> resources private. But your app also calls Azure services — storage, SQL, a vault — and those have <b>public addresses</b> by default. '
      'How do you let your network reach them without sending that traffic over the public internet, and without leaving them open to everyone?',
      'Azure offers two answers. <b>Service endpoints</b> are the older, simpler one: the service keeps its public IP but can be told to trust your subnet. <b>Private endpoints</b> (built on <b>Private Link</b>) go further: the service gets a private IP in your network. Microsoft recommends Private Link.'])
    body += block('🔎 The part that trips everybody up: DNS', figure(d_dns(),
        'your code still uses the same name, such as <code>mystorage.blob.core.windows.net</code>. <b>DNS</b> turns that name into an address. Unless you set up a <b>private DNS zone</b>, the name still resolves to the <i>public</i> IP — and your traffic ignores the private endpoint. '
        'With the zone in place, the same name resolves to the private endpoint\'s address. That is why a private endpoint always comes with a DNS step.'), label_cls='see')
    body += block('⚖️ Service endpoint vs private endpoint', table(['','Service endpoint','Private endpoint'], [
      ['What you connect to','The service\'s public IP — still public','A private IP in your own subnet'],
      ['What it covers','The whole service','One specific resource (one instance)'],
      ['From on-premises (VPN / ExpressRoute)','Not supported','Supported'],
      ['DNS','Nothing changes','The name must resolve to the private IP (usually a private DNS zone)'],
      ['Can you turn off public access?','Not the goal of this feature','Yes — a private endpoint lets you disable public access'],
      ['Microsoft\'s advice','Fine for simple subnet allow-listing','The recommended option (Private Link)'],
    ]), label_cls='see')
    body += block('🧭 Which one?', pick_cards([
      dict(icon='🧱', name='Service endpoint', tag='the quick subnet-level allow-list', color='#fbbf24',
           use=['You only need "allow my subnet" on the service\'s firewall', 'You want zero DNS changes'],
           skip=['You need access from on-premises', 'You need to restrict to one specific instance', 'You want the service to have no public path']),
      dict(icon='🔌', name='Private endpoint', tag='a private IP for one resource', color='#34d399',
           use=['You want private-only access to a specific resource', 'On-premises users must reach it over VPN or ExpressRoute', 'You want to disable public access'],
           skip=['You cannot manage the DNS side', 'A simple subnet allow-list is enough']),
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🛢️','Database no one can reach from the internet','The app must reach the SQL database, and nothing else may.','Private endpoint + public access off'),
      ('🏢','Office reads a storage account','Staff on the corporate network connect over a VPN.','Private endpoint'),
      ('⚡','Quick lock-down for a demo','Limit a storage account to one subnet, fast, no DNS work.','Service endpoint'),
      ('🔑','Web app reads secrets','Keep the vault off the public internet.','Private endpoint to the vault'),
      ('🐛','"It still uses the public IP!"','The private endpoint exists, but traffic ignores it.','Fix the DNS: private DNS zone'),
      ('🎯','One storage account of many','Only this one account should be reachable privately.','Private endpoint (per instance)'),
    ]), label_cls='see')
    body += recall([
      'A private endpoint = a network interface with a private IP in your subnet, connecting you to one resource over Private Link.',
      'A service endpoint keeps the service\'s public IP and only changes what the service sees (your subnet).',
      'Service endpoints cover the whole service and do not work from on-premises; private endpoints are per resource and do.',
      'DNS must resolve the service name to the private IP — usually with a private DNS zone.',
      'A private endpoint lets you disable public access. Microsoft recommends Private Link.'])
    body += saythis('"A private endpoint puts a network interface with a private IP from my subnet in front of a specific Azure resource, using Private Link, so traffic stays private and I can disable public access. '
      'A service endpoint keeps the service\'s public IP and just lets the service trust my subnet; it covers the whole service and does not help on-premises users. With private endpoints I must also fix DNS so the service name resolves to the private IP."')
    body += trap([
      '<b>"I made a private endpoint but nothing changed."</b> Almost always DNS. If the service name still resolves to the public IP, your app still goes over the public path. Check what the name resolves to from inside the network.',
      'Second trap: <b>creating a private endpoint does not close the public door.</b> It adds a private one. Turn off public network access on the resource separately when you are ready.'])
    body += confuse('🧱 Service endpoint', 'Public IP stays. The service learns the request came from your subnet. Whole-service scope.', '🔌 Private endpoint', 'A private IP in your subnet for one resource. Works from on-premises. Needs DNS.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''az network private-endpoint create --name pe-storage --resource-group rg-shop-prod \\
    --vnet-name vnet-shop --subnet data \\
    --private-connection-resource-id <span class="str">"&lt;storage-account-resource-id&gt;"</span> \\
    --group-id blob --connection-name conn-storage''',
      'Illustrative shape only — you also create a private DNS zone, link it to the network, and then disable public access on the storage account.'))
    body += next_box('That is private access to Azure services. Back to the Virtual Networks page for the full picture — and on to the next concept: Compute.', 'virtual-networks.html', 'Back to Virtual Networks')
    body += fact_note(FOOT, [DOCS_PL, DOCS_VNET])
    return page('private-endpoints', 'Private Endpoints', 'Deep dive · Virtual Networks · 🔌 Private endpoints',
        'A private endpoint puts an Azure service <span class="grad-text">inside your own network</span>, with a private IP address.',
        'Azure services have public addresses by default. Learn how a private endpoint brings one into your network, how it differs from a service endpoint, and the DNS detail that decides whether it works.',
        'What is the difference between a service endpoint and a private endpoint in Azure?',
        body, CR + ['<a href="virtual-networks.html">Virtual Networks</a>', '<span class="cur">Private endpoints</span>'], '', search_title='Private Endpoints')
