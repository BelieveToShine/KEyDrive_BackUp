from kit import *
from p_storage import CR

DOCS_VM = ('Azure Virtual Machines documentation', 'https://learn.microsoft.com/en-us/azure/virtual-machines/')
DOCS_AS = ('Azure App Service documentation', 'https://learn.microsoft.com/en-us/azure/app-service/')
DOCS_CA = ('Azure Container Apps documentation', 'https://learn.microsoft.com/en-us/azure/container-apps/')
DOCS_AKS = ('Azure Kubernetes Service documentation', 'https://learn.microsoft.com/en-us/azure/aks/')
DOCS_CHOOSE = ('Choose an Azure compute service (Architecture Center)', 'https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official docs.'

def d_spectrum():
    d = Diagram('cp1', 640, 276, 'Azure compute options from most control to least to run: virtual machines, AKS, Container Apps, App Service, Functions')
    d.text(10, 24, 'more control · more to run', anchor='start', size=9.5, mono=True)
    d.text(630, 24, 'less to run · fewer knobs', anchor='end', size=9.5, mono=True)
    boxes = [
      (10,  'n',       [('🖥️ VMs','t'),('you patch the OS','s'),('full control','s'),('lift-and-shift','s')]),
      (138, 'violet',  [('☸️ AKS','t'),('Kubernetes itself','s'),('full Kubernetes API','s'),('most to operate','s')]),
      (266, 'cyan',    [('📦 Container','t'),('Apps','t'),('containers, no','s'),('Kubernetes to run','s')]),
      (394, 'emerald', [('🌐 App','t'),('Service','t'),('web apps and APIs','s'),('Azure runs the OS','s')]),
      (522, 'amber',   [('⚡ Functions','t'),('code that reacts','s'),('to events','s')]),
    ]
    for x, col, lines in boxes:
        d.box(x, 40, 108, 130, lines, col)
    d.arrow([(64,170),(64,210),(576,210),(576,170)], 'cyan', label='Azure takes on more of the work', at=(320,210))
    d.text(320, 256, 'A rough guide, not a ranking — pick the most managed option that fits.', size=9.5, weight=700)
    return d

def d_choose():
    d = Diagram('cp2', 640, 708, 'Decision tree for choosing an Azure compute service: virtual machines, App Service, Container Apps, AKS, Functions or Container Instances')
    d.box(190, 8, 260, 34, [('🤔 What are you running?','t')], 'cyan')
    qs = [
     ('🖥️ Need the whole OS, or a lift-and-shift?',      'an installed agent, a legacy app',          'Virtual Machines',       'you control the OS',          'n'),
     ('🌐 A web app or HTTP API — just code?',           'no containers to manage',                    'App Service',            'Azure runs the platform',     'emerald'),
     ('📦 Already a container, no Kubernetes needed?',   'each app scales on its own',                 'Container Apps',         'containers without the cluster','cyan'),
     ('☸️ Need Kubernetes itself?',                     'its API, custom controllers, sidecars',      'AKS',                    'full Kubernetes control',     'violet'),
     ('⚡ Small code that reacts to an event?',          'a message, a timer, a webhook',              'Azure Functions',        'event-driven code',           'amber'),
     ('⏱️ One container for a one-off job?',            'no orchestration needed',                    'Container Instances',    'run it, then it ends',        'n'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 648
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 648, 330, 50, [('🤔 Still unsure?','t'),('start with the most managed option that fits','s')], 'emerald')
    return d

def d_scaling():
    d = Diagram('cp3', 640, 312, 'App Service scales the whole plan so its apps scale together; Container Apps scales each app on its own')
    d.zone(10, 8, 305, 296, 'emerald', 'APP SERVICE · you scale the plan')
    d.zone(24, 40, 277, 150, 'n', 'APP SERVICE PLAN')
    for i in range(3):
        d.box(34 + i*88, 72, 76, 100, [(f'VM {i+1}','t'),('App A','s'),('App B','s')], 'emerald')
    d.text(162, 222, "Both apps share the plan's instances", size=9.5)
    d.text(162, 238, 'and scale together.', size=9.5)
    d.text(162, 262, 'It does not scale to zero.', size=9.5, weight=700)
    d.zone(325, 8, 305, 296, 'cyan', 'CONTAINER APPS · each app scales alone')
    d.box(339, 72, 62, 50, [('App A','t')], 'cyan')
    for i in range(3):
        d.box(411 + i*70, 72, 60, 50, [('A','t'),('replica','s')], 'n')
    d.box(339, 142, 62, 50, [('App B','t')], 'cyan')
    d.box(411, 142, 60, 50, [('B','t'),('replica','s')], 'n')
    d.text(477, 222, 'Each app has its own scale rules.', size=9.5)
    d.text(477, 238, 'Most apps can scale to zero', size=9.5)
    d.text(477, 254, '(not when scaling on CPU or memory).', size=9.5)
    return d

def build_compute():
    body = ''
    body += see(figure(d_spectrum(),
        'five ways to run code on Azure, from the most control on the left to the least to look after on the right. <b>VMs</b> give you a whole machine — and its patching. <b>AKS</b> gives you Kubernetes itself. <b>Container Apps</b> runs your containers without making you run a cluster. '
        '<b>App Service</b> hosts web apps and APIs while Azure runs the operating system. <b>Functions</b> runs small pieces of code when something happens. As you move right, Azure does more of the work — and you get fewer knobs to turn.'))
    body += one('Compute is where your code runs. The real choice is how much of the machine you want to look after — the more you hand to Azure, the less you manage and the fewer knobs you get.')
    body += why([
      'You now have a safe network. Your code still needs somewhere to <b>run</b>. The oldest answer is a virtual machine: rent a computer in the cloud. It works for everything, but you inherit everything — patching the operating system, installing the runtime, planning how to add more copies when traffic grows.',
      'Azure offers a ladder of options because teams want different trade-offs: <b>control</b> or <b>convenience</b>. The skill is picking the <i>most managed</i> option that still meets your needs — and moving down the ladder only for a hard requirement.'])
    body += block('🧰 The six options', pick_cards([
      dict(icon='🖥️', name='Virtual Machines', tag='a whole computer in the cloud', color='#93a0b8',
           use=['You need the operating system itself, or software installed on the machine', 'Lift-and-shift of an existing server', 'Special needs such as GPUs or long-running batch work'],
           skip=['A normal web app — you would take on patching you do not need']),
      dict(icon='🌐', name='App Service', tag='managed hosting for web apps and APIs', color='#34d399',
           use=['A web app or HTTP API that you want to just deploy', 'Azure should handle the OS and runtime', 'Built-in autoscaling and deployment slots'],
           skip=['You need per-service scaling for many small containers', 'You need scale to zero — App Service does not scale to zero']),
      dict(icon='📦', name='Container Apps', tag='containers, without running Kubernetes', color='#22d3ee',
           use=['Microservices or containerised APIs', 'Each app should scale on its own, and most can scale to zero', 'Microsoft suggests looking at it first for containers when you do not need the Kubernetes API'],
           skip=['You need direct access to the Kubernetes API → AKS']),
      dict(icon='☸️', name='Azure Kubernetes Service (AKS)', tag='managed Kubernetes', color='#a78bfa',
           use=['You need Kubernetes itself: its API, custom controllers, CRDs', 'The most customisation and control for containers'],
           skip=['A small team that wants less to operate → Container Apps', 'It takes the most operational effort of the container options']),
      dict(icon='⚡', name='Azure Functions', tag='small code that reacts to events', color='#fbbf24',
           use=['Event-driven work: a message, a timer, a webhook', 'Small pieces of logic that do not need a server of their own'],
           skip=['A long-lived web app with many routes → App Service or Container Apps']),
      dict(icon='⏱️', name='Container Instances', tag='run a single container, no cluster', color='#93a0b8',
           use=['A one-off job or a quick task in a container', 'You do not want to provision a VM or a bigger service'],
           skip=['Autoscaling services — it does not scale beyond the container group']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'read the questions from the top; the first "yes" is usually your answer. The questions run from <b>most control</b> (do you need the whole operating system?) to <b>most specific</b> (a one-off container job). If none fits, do not agonise: start with the most managed option that meets your needs, and move toward more control only when a real requirement forces you.'), label_cls='see')
    body += block('📊 Who looks after what', table(['','You look after','Azure looks after','Scaling'], [
      ['Virtual Machines','The OS, patches, runtime, your app','The physical hardware and host','You set it up (scale sets — a later concept)'],
      ['App Service','Your code and its settings','The OS, patching and runtime','Built-in autoscale, scaled per App Service plan'],
      ['Container Apps','Your container images','The cluster and the scaling engine','Per app; most apps can scale to zero'],
      ['AKS','Containers and the Kubernetes setup','The control plane; node patching is shared','Kubernetes rules, as you configure them'],
      ['Functions','Your code','Almost everything else','On events (details in the Serverless concept)'],
      ['Container Instances','One container','The host','Not beyond the container group'],
    ]), label_cls='see')
    body += block('📏 Two different ways to scale', figure(d_scaling(),
        '<b>App Service</b> (left) scales the <em>plan</em>: you add more VM instances, and every app in the plan runs on all of them, so the apps scale together — and the plan does not scale down to zero. '
        '<b>Container Apps</b> (right) scales <em>each app</em> on its own rules, so a busy app can have many replicas while a quiet one has one — or none. This difference is often what decides between the two.'), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🏭','Old Windows app with an installed agent','It cannot be changed and needs software on the machine.','Virtual Machines'),
      ('🛒','Company website and API','A normal web app. The team wants to deploy code and move on.','App Service'),
      ('🧩','Ten small services in containers','Each scales differently, some are idle at night.','Container Apps'),
      ('🔧','Custom Kubernetes operators','The platform team needs the Kubernetes API and CRDs.','AKS'),
      ('📬','React to a new message','Run a few lines of code every time something arrives.','Azure Functions'),
      ('📊','A nightly data crunch in a container','It runs once, then it should end.','Container Instances'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — patching and the shared-responsibility line', '''      <p><b>Virtual machines (IaaS):</b> Microsoft looks after everything below the operating system — the datacenter, hardware and host. The guest OS is yours to patch, with help from tools such as Azure Update Manager.</p>
      <p><b>App Service (PaaS):</b> Azure patches the OS and the runtime for you. You look after your application and its data.</p>
      <p><b>Container Apps</b> is built on Kubernetes and uses KEDA for event-driven scaling, but it does not expose the Kubernetes API. If you need that API, that is the reason to choose AKS.</p>
      <p><b>Not covered here:</b> how to add more copies automatically and survive failures (Scaling &amp; Resilience), and how Functions really work (Serverless &amp; Orchestration). Both are later concepts in this journey.</p>''')
    body += recall([
      'Compute is a ladder: VMs (most control) → AKS → Container Apps → App Service → Functions (least to run).',
      'VMs: you patch the OS. App Service: Azure runs the OS and runtime. Container Apps: containers without Kubernetes. AKS: you need the Kubernetes API.',
      'Functions = event-driven code. Container Instances = a single container or a one-off job.',
      'App Service scales the plan and does not scale to zero; Container Apps scales each app and most can scale to zero.',
      'Start with the most managed option that fits; move toward control only for a hard requirement.'])
    body += saythis('"Compute on Azure is a trade-off between control and operational effort. Virtual Machines give full control but I patch the OS. App Service is managed hosting for web apps and APIs. Container Apps runs containers without exposing Kubernetes, with per-app scaling. '
      'AKS is for when I really need the Kubernetes API. Functions is for event-driven code, and Container Instances for one-off containers. I start with the most managed option that meets the requirement."')
    body += trap([
      '<b>Do not pick a VM just because it feels familiar.</b> A VM works for everything, but it is the option that gives you the most work: patching, hardening, backup and scaling are all yours. Use it when you have a reason.',
      'Second trap: <b>Kubernetes is a tool, not a goal.</b> Choosing AKS "because everyone does" means taking on the most operational effort of the container options. If you do not need the Kubernetes API, Container Apps is usually enough.'])
    body += confuse('🌐 App Service', 'A single web process or API, deployed as code, scaled per plan. No Dockerfile needed.', '📦 Container Apps', 'Containers, with each service scaled on its own and most able to scale to zero.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># run a container as a Container App — Azure runs and scales it, no cluster for you to manage</span>
az containerapp create --name shop-api --resource-group rg-shop-prod \\
    --environment env-shop --image mcr.microsoft.com/k8se/quickstart:latest \\
    --target-port 80 --ingress external''',
      'Illustrative shape only — you first create the environment, and real apps use their own image, identity, secrets and scale rules.'))
    body += next_box('Your code now has a place to run. But code needs somewhere to <b>keep things</b> — photos, files, messages, records. Next: Storage.', 'storage.html', 'Storage')
    body += fact_note(FOOT, [DOCS_CHOOSE, DOCS_VM, DOCS_AS, DOCS_CA, DOCS_AKS])
    return page('compute', 'Compute', 'Concept 5 of 19 · 🧱 Building blocks',
        'Compute is where your code runs — and the real choice is <span class="grad-text">how much of the machine you want to look after.</span>',
        'Azure offers virtual machines, web hosting, containers and functions. The more you hand to Azure, the less you manage — and the fewer knobs you can turn. Learn the ladder and how to pick your rung.',
        'How do you choose between Azure VMs, App Service, Container Apps, AKS, Functions and Container Instances?',
        body, CR + ['<span class="cur">Compute</span>'], '', search_title='Compute')
