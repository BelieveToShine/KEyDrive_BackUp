from kit import *
from p_common import CR

DOCS_CMP = ('Choosing an AWS compute service', 'https://docs.aws.amazon.com/decision-guides/latest/compute-on-aws-how-to-choose/choosing-aws-compute-service.html')
DOCS_CON = ('Choosing an AWS container service', 'https://docs.aws.amazon.com/decision-guides/latest/containers-on-aws-how-to-choose/choosing-aws-container-service.html')
DOCS_FL = ('Fargate or Lambda?', 'https://docs.aws.amazon.com/decision-guides/latest/decision-guides/fargate-or-lambda.html')
DOCS_EC2 = ('Amazon EC2 documentation', 'https://docs.aws.amazon.com/ec2/')
DOCS_ECS = ('Amazon ECS documentation', 'https://docs.aws.amazon.com/ecs/')
DOCS_EKS = ('Amazon EKS documentation', 'https://docs.aws.amazon.com/eks/')
DOCS_LAM = ('AWS Lambda documentation', 'https://docs.aws.amazon.com/lambda/')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official AWS docs.'

def d_spectrum():
    d = Diagram('co1', 640, 276, 'AWS compute options from most control to least to run: EC2, ECS or EKS on EC2, Fargate, Elastic Beanstalk and App Runner, Lambda')
    d.text(10, 24, 'more control · more to run', anchor='start', size=9.5, mono=True)
    d.text(630, 24, 'less to run · fewer knobs', anchor='end', size=9.5, mono=True)
    boxes = [
      (10,  'n',       [('🖥️ EC2','t'),('you manage the OS','s'),('full control','s'),('lift-and-shift','s')]),
      (138, 'violet',  [('☸️ ECS / EKS','t'),('containers on','s'),('hosts you run','s'),('(EC2)','s')]),
      (266, 'cyan',    [('📦 Fargate','t'),('containers, no','s'),('servers to run','s'),('(ECS or EKS)','s')]),
      (394, 'emerald', [('🌐 App Runner','t'),('Beanstalk','t'),('web apps, APIs','s'),('AWS runs it','s')]),
      (522, 'amber',   [('⚡ Lambda','t'),('code that reacts','s'),('to events','s')]),
    ]
    for x, col, lines in boxes:
        d.box(x, 40, 108, 130, lines, col)
    d.arrow([(64,170),(64,210),(576,210),(576,170)], 'cyan', label='AWS takes on more of the work', at=(320,210))
    d.text(320, 256, 'A rough guide, not a ranking — start at the managed end and move left only when you must.', size=9.5, weight=700)
    return d

def d_choose():
    d = Diagram('co2', 640, 708, 'Decision tree for choosing AWS compute: EC2, Elastic Beanstalk or App Runner, ECS, EKS or Lambda')
    d.box(190, 8, 260, 34, [('🤔 What are you running?','t')], 'cyan')
    qs = [
     ('🖥️ Need the whole OS, or lift-and-shift?',      'special software, a legacy app',          'EC2',              'you control the server',       'n'),
     ('🌐 A web app or API — just code or an image?',  'AWS should run the platform',             'App Runner',       'or Elastic Beanstalk',         'emerald'),
     ('📦 Containers, and AWS-native simplicity?',      'less to configure',                       'ECS on Fargate',   'containers, no servers',       'cyan'),
     ('☸️ Kubernetes is your standard?',               'its API and ecosystem',                   'EKS',              'managed Kubernetes',           'violet'),
     ('⚡ Small code that reacts to an event?',        'a file, a message, a timer, a request',   'Lambda',           'event-driven code',            'amber'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 560
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 560, 330, 50, [('🤔 Still unsure?','t'),('start with the most managed option','s')], 'emerald')
    return d

def d_fgl():
    d = Diagram('co3', 640, 300, 'Fargate runs a steady container service that keeps running, while Lambda runs a function only for the moment an event arrives')
    d.zone(10, 8, 305, 284, 'cyan', 'FARGATE · a container keeps running')
    d.box(24, 70, 80, 56, [('👥 Users','t')], 'n')
    d.box(200, 70, 100, 56, [('📦 Container','t'),('always on','s')], 'cyan')
    d.arrow([(104,98),(200,98)], 'cyan', label='served by', at=(152,98))
    d.text(162, 180, 'Good for steady, long-running', size=9.5)
    d.text(162, 196, 'services and web APIs.', size=9.5)
    d.text(162, 226, 'You think in tasks and services.', size=9.5, weight=700)
    d.zone(325, 8, 305, 284, 'amber', 'LAMBDA · a function runs per event')
    d.box(339, 70, 80, 56, [('⚡ Event','t')], 'n')
    d.box(515, 70, 100, 56, [('λ Function','t'),('runs, then stops','s')], 'amber')
    d.arrow([(419,98),(515,98)], 'amber', label='starts', at=(467,98))
    d.text(477, 180, 'Good for short, bursty, event-driven', size=9.5)
    d.text(477, 196, 'work. You pay while it runs.', size=9.5)
    d.text(477, 226, 'You think in functions and triggers.', size=9.5, weight=700)
    return d

def build_compute():
    body = ''
    body += see(figure(d_spectrum(),
        'five ways to run code on AWS, from the most control on the left to the least to look after on the right. <b>EC2</b> gives you a whole server — and its patching. <b>ECS and EKS</b> run containers (EKS is managed Kubernetes). <b>Fargate</b> runs those containers without servers for you to manage. '
        '<b>App Runner</b> and <b>Elastic Beanstalk</b> host web apps and APIs while AWS runs the platform. <b>Lambda</b> runs small functions when something happens. As you move right, AWS does more — and you get fewer knobs.'))
    body += one('Compute is where your code runs. The real choice is how much of the machine you want to look after — the more you hand to AWS, the less you manage and the fewer knobs you get.')
    body += why([
      'You now have a safe network. Your code still needs somewhere to <b>run</b>. The oldest answer is a virtual server (EC2): rent a computer in the cloud. It works for everything, but you inherit everything — patching the operating system, installing the runtime, planning how to add more copies when traffic grows.',
      'AWS offers a ladder because teams want different trade-offs: <b>control</b> or <b>convenience</b>. AWS\'s own guidance is to start at the managed end (App Runner or Fargate) and move toward self-management only when your workload needs it.'])
    body += block('🧰 The options', pick_cards([
      dict(icon='🖥️', name='Amazon EC2', tag='virtual servers', color='#93a0b8',
           use=['You need the operating system or special software on the machine', 'Lift-and-shift of an existing server', 'The most control over instance types and the host'],
           skip=['A normal web app — you take on patching you do not need']),
      dict(icon='🌐', name='App Runner and Elastic Beanstalk', tag='AWS runs the platform for web apps', color='#34d399',
           use=['App Runner: the simplest way to put a web app or API online from an image or source code', 'Elastic Beanstalk: web apps with several languages and Docker; it manages the EC2 runtime and patching'],
           skip=['You need fine control over networking and orchestration → ECS or EKS']),
      dict(icon='📦', name='Amazon ECS', tag='AWS-native container service', color='#22d3ee',
           use=['Containers with more control over networking and security than App Runner', 'AWS\'s most popular container service for teams that do not need Kubernetes', 'Run on Fargate (no servers) or on EC2'],
           skip=['Kubernetes is already your standard → EKS']),
      dict(icon='☸️', name='Amazon EKS', tag='managed Kubernetes', color='#a78bfa',
           use=['You already use Kubernetes, or want its ecosystem and portability', 'Run on Fargate or on EC2'],
           skip=['A small team that wants less to operate → ECS on Fargate']),
      dict(icon='⚡', name='AWS Lambda', tag='functions that react to events', color='#fbbf24',
           use=['Event-driven work: a file, a message, a timer, an API call', 'Short, bursty tasks where you pay while it runs'],
           skip=['Long-running steady services — a container service fits better']),
      dict(icon='📦', name='AWS Fargate', tag='serverless compute for containers', color='#22d3ee',
           use=['Run ECS or EKS containers without managing EC2 instances', 'Spiky workloads, where it tends to win on cost'],
           skip=['Steady, highly utilised workloads — EC2 can be cheaper']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'read the questions from the top; the first "yes" is usually your answer. The questions run from <b>most control</b> (do you need the whole server?) to <b>most specific</b> (a small function that reacts to an event). '
        'If none fits, do not agonise: start with the most managed option that meets your needs, and move toward more control only when a real requirement forces you.'), label_cls='see')
    body += block('📦 Fargate or Lambda?', figure(d_fgl(),
        'both are "serverless" but they think differently. <b>Fargate</b> (left) runs a container that stays up and serves requests — good for steady services and long-running work. '
        '<b>Lambda</b> (right) starts a function for each event and you pay while it runs — good for short, bursty tasks. AWS\'s guidance is that Lambda fits short, bursty tasks better than long-running services.'), label_cls='see')
    body += block('📊 Who looks after what', table(['','You look after','AWS looks after','Scaling'], [
      ['🖥️ EC2','The OS, patches, runtime, your app','The physical hardware and host','You set it up (Auto Scaling — a later concept)'],
      ['🌐 Elastic Beanstalk','Your code and its settings','Provisioning, and the EC2 runtime and patching','Managed with the environment'],
      ['🌐 App Runner','Your image or source','Build, deploy and scaling','Automatic'],
      ['📦 ECS / EKS on EC2','Containers and the hosts','The control plane','You scale the hosts and tasks'],
      ['📦 ECS / EKS on Fargate','Containers','The servers underneath','Per task or pod'],
      ['⚡ Lambda','Your function','Almost everything else','Per event'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🏭','Old Windows app with an installed agent','It cannot be changed and needs software on the machine.','EC2'),
      ('🛒','Company website and API','A normal web app. The team wants to push code and move on.','App Runner or Elastic Beanstalk'),
      ('🧩','Ten small services in containers','The team wants AWS-native simplicity.','ECS on Fargate'),
      ('🔧','The platform team runs Kubernetes everywhere','They need its API and ecosystem.','EKS'),
      ('📬','React to a new file in storage','Run a few lines of code each time.','Lambda'),
      ('📈','A steady API busy all day','High, even utilisation.','Containers on EC2 can be cheaper than Fargate'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — the shared-responsibility line', '''      <p><b>EC2:</b> AWS looks after the hardware and the host. The guest operating system is yours to patch and secure.</p>
      <p><b>Fargate</b> is not an orchestrator by itself. It is the serverless compute that ECS and EKS can run on, so you do not manage EC2 instances for those containers. ECS and EKS can both run on Fargate or on EC2, so the choices are not exclusive.</p>
      <p><b>Fargate vs EC2</b> is mainly a cost question: Fargate tends to win for spiky workloads, while steady, highly utilised workloads can be cheaper on EC2. Check the pricing pages before deciding.</p>
      <p><b>Not covered here:</b> how to add more copies automatically and survive failures (Scaling &amp; Resilience), and how Lambda really works (Serverless &amp; Orchestration). Both are later concepts.</p>''')
    body += recall([
      'Compute is a ladder: EC2 (most control) → ECS/EKS → Fargate → App Runner/Elastic Beanstalk → Lambda (least to run).',
      'EC2: you patch the OS. Beanstalk and App Runner: AWS runs the platform. ECS: AWS-native containers. EKS: managed Kubernetes. Fargate: serverless compute for ECS and EKS.',
      'Lambda = event-driven functions, best for short and bursty work.',
      'Fargate vs EC2 is mostly cost: Fargate for spiky, EC2 for steady and highly utilised.',
      'Start at the managed end and move toward control only for a hard requirement.'])
    body += saythis('"Compute on AWS is a trade-off between control and effort. EC2 gives full control but I patch the OS. App Runner and Elastic Beanstalk host web apps with AWS running the platform. ECS is the AWS-native container service and EKS is managed Kubernetes, and both can run on Fargate so I manage no servers. '
      'Lambda runs event-driven functions. I start at the managed end and move left only for a real requirement."')
    body += trap([
      '<b>Do not pick EC2 just because it feels familiar.</b> It works for everything, but it is the option that gives you the most work: patching, hardening, backup and scaling are all yours.',
      'Second trap: <b>Kubernetes is a tool, not a goal.</b> Choosing EKS "because everyone does" means taking on more to operate. If you do not need the Kubernetes API or ecosystem, ECS is usually simpler.'])
    body += confuse('📦 ECS', 'AWS-native container orchestration. Simpler, closely tied to AWS.', '☸️ EKS', 'Managed Kubernetes. Portable and rich in tooling, with more to learn and operate.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># start one small virtual server — you choose the image, the size and the subnet</span>
aws ec2 run-instances --image-id &lt;ami-id&gt; --instance-type t3.micro --subnet-id &lt;subnet-id&gt;''',
      'Illustrative shape only — the image ID, size and subnet are placeholders, and real launches add a role, a security group and storage.'))
    body += next_box('Your code now has a place to run. But code needs somewhere to <b>keep things</b> — files, images, backups, disks. Next: Storage.', None)
    body += fact_note(FOOT, [DOCS_CMP, DOCS_CON, DOCS_FL, DOCS_EC2, DOCS_ECS, DOCS_EKS, DOCS_LAM])
    return page('compute', 'Compute', 'Concept 5 of 19 · 🧱 Building blocks',
        'Compute is where your code runs — and the real choice is <span class="grad-text">how much of the machine you want to look after.</span>',
        'EC2, containers on ECS and EKS, Fargate, App Runner, Elastic Beanstalk and Lambda: learn the ladder and how to pick your rung.',
        'How do you choose between EC2, ECS, EKS, Fargate and Lambda?',
        body, CR + ['<span class="cur">Compute</span>'], '', search_title='Compute')
