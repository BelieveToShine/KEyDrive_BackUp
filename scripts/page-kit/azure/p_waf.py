from kit import *
from p_storage import CR

DOCS_WAF = ('Azure Well-Architected Framework', 'https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework')
DOCS_PIL = ('Well-Architected pillars', 'https://learn.microsoft.com/en-us/azure/well-architected/pillars')
DOCS_LZ = ('What is an Azure landing zone?', 'https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/')
DOCS_LZD = ('Landing zone design areas', 'https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-areas')
DOCS_CAF = ('Cloud Adoption Framework', 'https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/')
DOCS_ADV = ('Azure Advisor', 'https://learn.microsoft.com/en-us/azure/advisor/advisor-overview')
DOCS_ARCH = ('Azure Architecture Center', 'https://learn.microsoft.com/en-us/azure/architecture/')
FOOT = 'Frameworks are renamed and reorganised often (the Cloud Adoption Framework recently renamed its landing zone terms). This page teaches the ideas; for current names and guidance, check the official docs.'

def d_pillars():
    d = Diagram('wa1', 640, 330, 'Five pillars of the Well-Architected Framework around your design, each one a trade-off against the others')
    d.box(20, 14, 170, 56, [('🛟 Reliability','t'),('concepts 2, 8, 9','s')], 'cyan')
    d.box(235, 14, 170, 56, [('🔐 Security','t'),('concepts 3, 4, 15, 16','s')], 'rose')
    d.box(450, 14, 170, 56, [('💰 Cost optimization','t'),('concept 18','s')], 'amber')
    d.box(240, 130, 160, 70, [('⚖️ Your design','t'),('every choice is a','s'),('trade-off','s')], 'emerald')
    d.box(60, 262, 170, 56, [('🛠️ Operations','t'),('concepts 13, 14, 17','s')], 'violet')
    d.box(410, 262, 170, 56, [('🚀 Performance','t'),('concepts 5–7, 10','s')], 'n')
    d.arrow([(105,70),(105,165),(240,165)], 'cyan', label='trade-off', at=(172,165))
    d.arrow([(320,70),(320,130)], 'rose', label='trade-off', at=(320,100))
    d.arrow([(535,70),(535,165),(400,165)], 'amber', label='trade-off', at=(468,165))
    d.arrow([(145,262),(145,231),(280,231),(280,200)], 'violet', label='trade-off', at=(212,231))
    d.arrow([(495,262),(495,231),(360,231),(360,200)], 'n', label='trade-off', at=(428,231))
    return d

def d_lz():
    d = Diagram('wa2', 640, 312, 'A landing zone: management groups and policy at the top, a platform landing zone with shared services, and workload landing zones where applications run')
    d.box(190, 8, 260, 54, [('🏛️ Management groups','t'),('hierarchy + policy at the top','s')], 'amber')
    d.zone(10, 108, 270, 168, 'cyan', 'PLATFORM · shared services')
    d.box(24, 138, 242, 34, [('🪪 Identity','t')], 'n')
    d.box(24, 180, 242, 34, [('🌐 Connectivity','t')], 'n')
    d.box(24, 222, 242, 34, [('📈 Management and monitoring','t')], 'n')
    d.zone(360, 108, 270, 168, 'emerald', 'WORKLOADS · where apps run')
    d.box(374, 140, 242, 52, [('📦 Workload A','t'),('one team\'s subscription','s')], 'n')
    d.box(374, 204, 242, 52, [('📦 Workload B','t'),('another team\'s subscription','s')], 'n')
    d.arrow([(260,62),(260,88),(145,88),(145,108)], 'amber', label='governs', at=(205,88))
    d.arrow([(380,62),(380,88),(495,88),(495,108)], 'amber', label='governs', at=(435,88))
    d.arrow([(360,192),(280,192)], 'emerald', label='uses', at=(320,192))
    d.text(320, 298, 'Guardrails come from the top, so every new workload starts inside them.', size=9.5, weight=700)
    return d

def d_journey():
    d = Diagram('wa3', 640, 440, 'The whole Azure journey in five stages, each one raising the question the next one answers')
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
        'the Well-Architected Framework looks at a design through <b>five pillars</b>: Reliability, Security, Cost Optimization, Operational Excellence and Performance Efficiency. Each box shows which earlier concepts feed it. '
        'The point of the picture is the arrows: <b>improving one pillar often costs another</b>. A second region raises reliability and the bill. Deep inspection raises security and lowers speed. Your job is to choose consciously, not to maximise every pillar.'))
    body += one('A well-architected system is not the one with the most features — it is the one whose trade-offs between reliability, security, cost, operations and performance were chosen on purpose.')
    body += why([
      'You now know the pieces: hierarchy, regions, identity, networks, compute, storage, databases, load balancing, scaling, caching, messaging, serverless, code for infrastructure, pipelines, secrets, security, signals and cost. Each one was a good answer to a real limit. But each one also has a price: another thing to run, pay for, secure or watch.',
      'So the last skill is not another service. It is <b>judgement</b>: how to look at a whole design and ask whether it fits what the business needs. Microsoft packages that judgement in two frameworks. The <b>Well-Architected Framework</b> helps you review a <i>workload</i>. The <b>Cloud Adoption Framework</b> and its <b>landing zone</b> help you set up the <i>environment</i> that workloads live in.'])
    body += block('🧰 The frameworks', pick_cards([
      dict(icon='⚖️', name='Well-Architected Framework', tag='review one workload', color='#34d399',
           use=['Check a design against five pillars', 'Each pillar gives practices, risks and trade-offs', 'Record where you traded one pillar for another'],
           skip=['Using it as a checklist to tick — it is about decisions, not boxes']),
      dict(icon='🧭', name='Cloud Adoption Framework', tag='plan and govern the whole move to cloud', color='#22d3ee',
           use=['Strategy, planning, readiness and governance', 'Guidance for setting up and managing the environment'],
           skip=['Looking for service-level design details — that is the Architecture Center']),
      dict(icon='🏔️', name='Landing zone', tag='a ready, governed place for workloads', color='#a78bfa',
           use=['A platform landing zone with shared services (identity, connectivity, management)', 'Workload landing zones where application teams deploy', 'Policy and structure set up before the first app arrives'],
           skip=['A one-off experiment — start small, grow into it']),
      dict(icon='💡', name='Azure Advisor', tag='recommendations on your real resources', color='#fbbf24',
           use=['Recommendations in cost, performance, reliability, security and operational excellence', 'A quick, practical starting point'],
           skip=['Treating it as a full architecture review — it looks at configuration and usage, not intent']),
    ]), label_cls='see')
    body += block('🏔️ What a landing zone is', figure(d_lz(),
        'a landing zone is a <b>prepared environment</b> so teams do not start from an empty subscription. At the top, <b>management groups and policy</b> (concepts 1 and 16) set the guardrails. A <b>platform landing zone</b> holds the shared services — identity, connectivity, management. '
        '<b>Workload landing zones</b> are where each application team deploys. Workloads use the platform, and the guardrails reach them automatically. Its design areas cover identity, network, security, management, governance and automation.'), label_cls='see')
    body += block('🗺️ The whole journey', figure(d_journey(),
        'each stage exists because the one before it ran into a limit. <b>Foundations</b> organise and connect things. Then code needs a place to run (<b>building blocks</b>), one copy is not enough (<b>handling load</b>), and by hand it all becomes too much to click and ship (<b>shipping and operating</b>). '
        'Finally, you need a way to judge it all together — this concept.'), label_cls='see')
    body += block('📊 The five pillars', table(['Pillar','The question it asks','Concepts you already have for it'], [
      ['🛟 Reliability','Does it keep working, and recover when it does not?','Zones and regions, load balancing, scaling, disaster recovery'],
      ['🔐 Security','Is it protected, and is access limited?','Identity, networks, secrets, policy, Defender'],
      ['💰 Cost Optimization','Are we getting value for what we spend?','Cost Management, rightsizing, commitments'],
      ['🛠️ Operational Excellence','Can we ship, run and fix it reliably?','Infrastructure as code, CI/CD, monitoring'],
      ['🚀 Performance Efficiency','Does it meet demand quickly, without waste?','Right compute, caching, scaling, databases'],
    ]), label_cls='see')
    body += block('🎬 Real-world trade-offs', scenarios([
      ('🌍','"Let\'s go multi-region for safety."','Reliability goes up, and so do cost and complexity.','Is a zone-redundant design enough?'),
      ('🔍','"Inspect and log every request."','Security and visibility go up; speed and cost can go down.','Decide what is worth inspecting.'),
      ('⚡','"Always keep extra capacity warm."','Performance is smooth; you pay for idle capacity.','Autoscale, or reserve a baseline'),
      ('🧑‍💻','"Let teams create what they like."','Speed is high; security and cost become unpredictable.','Policy guardrails in a landing zone'),
      ('🔁','"Release five times a day."','Operations improve; risk must be managed with slots and checks.','CI/CD with a fast rollback'),
      ('📝','"Why did we choose this?"','Nobody remembers the reasoning.','Write the trade-off down'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — how to use the frameworks in practice', '''      <p><b>Balance, not maximise.</b> Microsoft says design decisions must be balanced across all pillars given the business requirements, and that adopting a recommendation may mean choosing against another pillar. For many production workloads, a zone-redundant deployment is a good balance; multiple regions raise reliability but add cost and complexity. Write the choice and the reason down.</p>
      <p><b>Start from requirements.</b> What must be true: how much downtime, how much data loss (RPO and RTO from concept 9), what compliance, what budget? The pillars are a way to check you did not forget a dimension.</p>
      <p><b>Review regularly.</b> A design that was right last year may not be now: traffic grows, prices and services change, teams change. Revisit with the framework and with Azure Advisor.</p>
      <p><b>Landing zone terms move.</b> The Cloud Adoption Framework has recently renamed "application landing zones" to "workload landing zones" and dropped the separate data-landing-zone categories; detailed architecture guidance now lives mainly in the Azure Architecture Center and the Well-Architected Framework. Check the current names.</p>''')
    body += recall([
      'Five pillars: Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency.',
      'The pillars trade off against each other; record where you chose one over another and why.',
      'Well-Architected Framework reviews a workload; the Cloud Adoption Framework and landing zones set up the environment.',
      'Landing zone = platform landing zone (shared services: identity, connectivity, management) + workload landing zones, under management groups and policy.',
      'Azure Advisor gives recommendations across cost, performance, reliability, security and operational excellence.'])
    body += saythis('"I review a design against the five Well-Architected pillars and accept that they trade off — for example a second region improves reliability but adds cost and complexity — so I write down the choices. '
      'For the environment I use a landing zone: management groups and policy at the top, a platform landing zone with shared identity, connectivity and management, and workload landing zones for each team. Then I review again as things change."')
    body += trap([
      '<b>Treating the framework as a checklist.</b> Ticking every recommendation is not the goal; some will cost more than the risk they remove. The value is in the explicit trade-offs.',
      'Second trap: <b>building the landing zone last.</b> Guardrails added after a hundred workloads exist are far harder to apply than guardrails that every workload starts inside.'])
    body += confuse('⚖️ Well-Architected Framework', 'Reviews a workload against five pillars and its trade-offs. "Is this design a good one?"', '🏔️ Landing zone', 'Prepares the environment that workloads run in, with structure and guardrails. "Where do workloads go?"')
    body += next_box('That completes the Azure journey: from a tenant and its subscriptions all the way to judging a whole design. The same 19 steps work for AWS, with different service names — start there next.', None)
    body += fact_note(FOOT, [DOCS_WAF, DOCS_PIL, DOCS_LZ, DOCS_LZD, DOCS_CAF, DOCS_ADV, DOCS_ARCH])
    return page('well-architected', 'Well-Architected & Landing Zones', 'Concept 19 of 19 · 🏛️ The capstone',
        'A well-architected system is one whose trade-offs were <span class="grad-text">chosen on purpose — not one that maximised everything.</span>',
        'The five Well-Architected pillars, why they pull against each other, and how landing zones prepare an environment so every workload starts with guardrails.',
        'What is the Azure Well-Architected Framework, and what is a landing zone?',
        body, CR + ['<span class="cur">Well-Architected</span>'], '', search_title='Well-Architected & Landing Zones')
