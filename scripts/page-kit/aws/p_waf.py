from kit import *
from p_common import CR

DOCS_WAF = ('AWS Well-Architected Framework: the pillars', 'https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html')
DOCS_WAFU = ('What is the AWS Well-Architected Framework?', 'https://docs.aws.amazon.com/wellarchitected/latest/userguide/waf.html')
DOCS_CT = ('What is AWS Control Tower?', 'https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html')
DOCS_SRA = ('AWS Security Reference Architecture', 'https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html')
DOCS_ORG = ('Organizing your AWS environment using multiple accounts', 'https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html')
FOOT = 'Frameworks and services are renamed and reorganised often. This page teaches the ideas; for current names and guidance, check the official AWS docs.'

def d_pillars():
    d = Diagram('wa1', 640, 340, 'Six pillars of the AWS Well-Architected Framework around your design, each one a trade-off against the others')
    d.box(20, 14, 180, 56, [('🛟 Reliability','t'),('concepts 2, 8, 9','s')], 'cyan')
    d.box(230, 14, 180, 56, [('🔐 Security','t'),('concepts 3, 4, 15, 16','s')], 'rose')
    d.box(440, 14, 180, 56, [('💰 Cost optimization','t'),('concept 18','s')], 'amber')
    d.box(240, 130, 160, 70, [('⚖️ Your design','t'),('every choice is a','s'),('trade-off','s')], 'emerald')
    d.box(20, 268, 180, 56, [('🛠️ Operational','t'),('excellence · 13, 14, 17','s')], 'violet')
    d.box(230, 268, 180, 56, [('🚀 Performance','t'),('efficiency · 5–7, 10','s')], 'n')
    d.box(440, 268, 180, 56, [('🌱 Sustainability','t'),('less energy, less waste','s')], 'emerald')
    d.arrow([(110,70),(110,165),(240,165)], 'cyan', label='trade-off', at=(172,165))
    d.arrow([(320,70),(320,130)], 'rose', label='trade-off', at=(320,100))
    d.arrow([(530,70),(530,165),(400,165)], 'amber', label='trade-off', at=(468,165))
    d.arrow([(110,268),(110,234),(270,234),(270,200)], 'violet', label='trade-off', at=(190,234))
    d.arrow([(320,268),(320,200)], 'n', label='trade-off', at=(320,238))
    d.arrow([(530,268),(530,234),(370,234),(370,200)], 'emerald', label='trade-off', at=(450,234))
    return d

def d_lz():
    d = Diagram('wa2', 640, 312, 'A landing zone: Organizations and guardrails at the top, shared platform accounts for security, logging and networking, and workload accounts where applications run')
    d.box(190, 8, 260, 54, [('🏛️ AWS Organizations','t'),('OUs and guardrails at the top','s')], 'amber')
    d.zone(10, 108, 270, 168, 'cyan', 'PLATFORM · shared accounts')
    d.box(24, 138, 242, 34, [('🛡️ Security and logging','t')], 'n')
    d.box(24, 180, 242, 34, [('🌐 Networking','t')], 'n')
    d.box(24, 222, 242, 34, [('🪪 Identity and shared services','t')], 'n')
    d.zone(360, 108, 270, 168, 'emerald', 'WORKLOADS · where apps run')
    d.box(374, 140, 242, 52, [('📦 Workload account A','t'),('one team','s')], 'n')
    d.box(374, 204, 242, 52, [('📦 Workload account B','t'),('another team','s')], 'n')
    d.arrow([(260,62),(260,88),(145,88),(145,108)], 'amber', label='governs', at=(205,88))
    d.arrow([(380,62),(380,88),(495,88),(495,108)], 'amber', label='governs', at=(435,88))
    d.arrow([(360,192),(280,192)], 'emerald', label='uses', at=(320,192))
    d.text(320, 298, 'Guardrails come from the top, so every new account starts inside them.', size=9.5, weight=700)
    return d

def d_journey():
    d = Diagram('wa3', 640, 440, 'The whole AWS journey in five stages, each one raising the question the next one answers')
    rows = [
      ('🏗️ Foundations · concepts 1–4','where things live, who may act, how they connect','n'),
      ('🧱 Building blocks · concepts 5–7','compute, storage, databases','cyan'),
      ('⚙️ Handling load · concepts 8–12','balance, scale, cache, message, serverless','amber'),
      ('🛠️ Shipping and operating · concepts 13–18','code, pipelines, secrets, security, signals, cost','violet'),
      ('🏛️ Well-Architected · concept 19','judge all of it, and set up the landing zone','emerald'),
    ]
    labels = ['now where does code run?','one copy is not enough','too many parts to click and ship by hand','how do we judge all of it?']
    for i,(t,s_,c) in enumerate(rows):
        y = 10 + i*88
        d.box(20, y, 600, 52, [(t,'t'),(s_,'s')], c)
        if i < 4:
            d.arrow([(130,y+52),(130,y+88)], 'n', label=labels[i], at=(300,y+70))
    return d

def build_well_architected():
    body = ''
    body += see(figure(d_pillars(),
        'the AWS Well-Architected Framework looks at a design through <b>six pillars</b>: operational excellence, security, reliability, performance efficiency, cost optimization and sustainability. Each box shows which earlier concepts feed it. '
        'The point of the picture is the arrows: <b>improving one pillar often costs another</b>. A second Region raises reliability and the bill. Deep inspection raises security and lowers speed. Your job is to choose consciously, not to maximise every pillar.'))
    body += one('A well-architected system is not the one with the most features — it is the one whose trade-offs between reliability, security, cost, operations, performance and sustainability were chosen on purpose.')
    body += why([
      'You now know the pieces: accounts, Regions, identity, networks, compute, storage, databases, load balancing, scaling, caching, messaging, serverless, code for infrastructure, pipelines, secrets, security, signals and cost. Each one was a good answer to a real limit. But each one also has a price: another thing to run, pay for, secure or watch.',
      'So the last skill is not another service. It is <b>judgement</b>: how to look at a whole design and ask whether it fits what the business needs. AWS packages that judgement in the <b>Well-Architected Framework</b> (for a <i>workload</i>) and in the <b>landing zone</b> (for the <i>environment</i> workloads live in).'])
    body += block('🧰 The pieces', pick_cards([
      dict(icon='⚖️', name='Well-Architected Framework', tag='review one workload', color='#34d399',
           use=['Check a design against six pillars', 'Each pillar gives practices and trade-offs', 'Record where you traded one pillar for another'],
           skip=['Using it as a checklist to tick — it is about decisions, not boxes']),
      dict(icon='🏔️', name='Landing zone', tag='a ready, governed multi-account environment', color='#a78bfa',
           use=['A well-architected multi-account environment based on security and compliance best practices', 'Structure and guardrails in place before the first workload arrives'],
           skip=['A one-off experiment — start small, grow into it']),
      dict(icon='🗼', name='AWS Control Tower', tag='set up and govern a landing zone', color='#22d3ee',
           use=['Orchestrates Organizations, Service Catalog and IAM Identity Center to build a landing zone', 'Applies preventive and detective guardrails, with a dashboard', 'AWS recommends starting with it'],
           skip=['You need a fully custom design that only a hand-built landing zone supports']),
      dict(icon='🧭', name='Security reference architecture', tag='how to organise security accounts and services', color='#fbbf24',
           use=['Guidance on security accounts, delegated administration and layered services'],
           skip=['Treating it as a ready-made product — it is guidance']),
    ]), label_cls='see')
    body += block('🏔️ What a landing zone is', figure(d_lz(),
        'a landing zone is a <b>prepared multi-account environment</b> so teams do not start from an empty account. At the top, <b>Organizations</b> and its guardrails (concepts 1 and 16) apply to everything. Shared <b>platform accounts</b> hold security and logging, networking and identity. '
        '<b>Workload accounts</b> are where each team deploys. AWS Control Tower can set this up for you with prevention and detection guardrails and a dashboard.'), label_cls='see')
    body += block('🗺️ The whole journey', figure(d_journey(),
        'each stage exists because the one before it ran into a limit. <b>Foundations</b> organise and connect things. Then code needs a place to run (<b>building blocks</b>), one copy is not enough (<b>handling load</b>), and by hand it all becomes too much to click and ship (<b>shipping and operating</b>). '
        'Finally, you need a way to judge it all together — this concept.'), label_cls='see')
    body += block('📊 The six pillars', table(['Pillar','The question it asks','Concepts you already have for it'], [
      ['🛠️ Operational excellence','Can we ship, run and fix it reliably?','Infrastructure as code, CI/CD, monitoring'],
      ['🔐 Security','Is it protected, and is access limited?','IAM, VPC, secrets, SCPs, detection'],
      ['🛟 Reliability','Does it do its job correctly when expected, and recover?','Zones and Regions, load balancing, scaling, disaster recovery'],
      ['🚀 Performance efficiency','Does it meet demand quickly, without waste?','Right compute, caching, scaling, databases'],
      ['💰 Cost optimization','Are we getting value for what we spend?','Cost Management, rightsizing, commitments'],
      ['🌱 Sustainability','Are we using the least energy and resources we need?','Right-sizing, autoscaling, avoiding idle capacity'],
    ]), label_cls='see')
    body += block('🎬 Real-world trade-offs', scenarios([
      ('🌍','"Let\'s go multi-Region for safety."','Reliability goes up, and so do cost and complexity.','Is multi-AZ enough?'),
      ('🔍','"Inspect and log every request."','Security and visibility go up; speed and cost can go down.','Decide what is worth inspecting.'),
      ('⚡','"Always keep extra capacity warm."','Performance is smooth; you pay for idle capacity.','Auto Scaling, or a reserved baseline'),
      ('🧑‍💻','"Let teams create what they like."','Speed is high; security and cost become unpredictable.','Guardrails in a landing zone'),
      ('🔁','"Release five times a day."','Operations improve; risk must be managed with safe rollouts.','CI/CD with a fast rollback'),
      ('📝','"Why did we choose this?"','Nobody remembers the reasoning.','Write the trade-off down'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — how to use the framework in practice', '''      <p><b>Balance, not maximise.</b> When designing a workload you make trade-offs between the pillars based on business needs. AWS notes that security and operational excellence are generally not traded away against the other pillars; the others are weighed against each other. Write the choice and the reason down.</p>
      <p><b>Start from requirements.</b> What must be true: how much downtime, how much data loss (RPO and RTO from concept 9), what compliance, what budget? The pillars are a way to check you did not forget a dimension.</p>
      <p><b>Review regularly.</b> A design that was right last year may not be now: traffic grows, prices and services change, teams change.</p>
      <p><b>Control Tower.</b> It automates account setup in an organization, provisioning and guardrails, and gives a dashboard; a custom-built landing zone is for requirements only a custom solution can meet.</p>''')
    body += recall([
      'Six pillars: operational excellence, security, reliability, performance efficiency, cost optimization, sustainability.',
      'The pillars trade off against each other; record where you chose one over another and why.',
      'The Well-Architected Framework reviews a workload; a landing zone sets up the multi-account environment.',
      'Control Tower builds and governs a landing zone with preventive and detective guardrails and a dashboard.',
      'Landing zone = platform accounts (security, logging, networking, identity) + workload accounts, under Organizations and guardrails.'])
    body += saythis('"I review a design against the six Well-Architected pillars and accept that they trade off — for example a second Region improves reliability but adds cost and complexity — so I write down the choices. '
      'For the environment I use a landing zone: Organizations and guardrails at the top, shared platform accounts for security, logging and networking, and workload accounts for each team, set up with Control Tower. Then I review again as things change."')
    body += trap([
      '<b>Treating the framework as a checklist.</b> Ticking every recommendation is not the goal; some will cost more than the risk they remove. The value is in the explicit trade-offs.',
      'Second trap: <b>building the landing zone last.</b> Guardrails added after a hundred workloads exist are far harder to apply than guardrails that every account starts inside.'])
    body += confuse('⚖️ Well-Architected Framework', 'Reviews a workload against six pillars and its trade-offs. "Is this design a good one?"', '🏔️ Landing zone', 'Prepares the environment that workloads run in, with structure and guardrails. "Where do workloads go?"')
    body += next_box('That completes the AWS journey: from an account and its organization all the way to judging a whole design. The same 19 steps shown for Azure carry over — only the service names change.', None)
    body += fact_note(FOOT, [DOCS_WAF, DOCS_WAFU, DOCS_CT, DOCS_SRA, DOCS_ORG])
    return page('well-architected', 'Well-Architected & Landing Zones', 'Concept 19 of 19 · 🏛️ The capstone',
        'A well-architected system is one whose trade-offs were <span class="grad-text">chosen on purpose — not one that maximised everything.</span>',
        'The six Well-Architected pillars, why they pull against each other, and how landing zones and Control Tower prepare an environment so every account starts with guardrails.',
        'What is the AWS Well-Architected Framework, and what is a landing zone?',
        body, CR + ['<span class="cur">Well-Architected</span>'], '', search_title='Well-Architected & Landing Zones')
