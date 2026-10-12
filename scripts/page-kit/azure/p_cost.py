from kit import *
from p_storage import CR

DOCS_CM = ('Microsoft Cost Management overview', 'https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/overview-cost-management')
DOCS_BUD = ('Create and manage budgets', 'https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets')
DOCS_OPT = ('Optimize your cloud investment', 'https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-mgt-best-practices')
DOCS_ALLOC = ('Allocate Azure costs', 'https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/allocate-costs')
DOCS_ADV = ('Azure Advisor cost recommendations', 'https://learn.microsoft.com/en-us/azure/advisor/advisor-cost-recommendations')
DOCS_SPOT = ('Azure Spot Virtual Machines', 'https://learn.microsoft.com/en-us/azure/virtual-machines/spot-vms')
DOCS_WAF = ('Well-Architected: cost optimization principles', 'https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/principles')
FOOT = 'Prices, discount levels and offers change often, so this page uses no price numbers. For current prices and terms, check the official docs and the pricing calculator.'

def d_cycle():
    d = Diagram('co1', 640, 294, 'The cost loop: see where the money goes, stop paying for waste, pay less for what stays, then review again')
    rows = [
      ('👀 See where the money goes','tags, cost analysis, budgets and alerts','cyan'),
      ('✂️ Stop paying for waste','idle VMs, orphaned disks, oversized resources','amber'),
      ('🏷️ Pay less for what stays','reservations, savings plans, Spot, Hybrid Benefit','emerald'),
    ]
    labels = ['finds','then commits']
    for i,(t,s_,c) in enumerate(rows):
        y = 12 + i*96
        d.box(70, y, 550, 60, [(t,'t'),(s_,'s')], c)
        if i < 2:
            d.arrow([(345,y+60),(345,y+96)], 'n', label=labels[i], at=(420,y+78))
    d.arrow([(70,204),(36,204),(36,42),(70,42)], 'n', label='repeat', at=(36,123))
    d.text(345, 284, 'Cost is a habit, not a project: the loop never really ends.', size=9.5, weight=700)
    return d

def d_choose():
    d = Diagram('co2', 640, 536, 'Decision tree for paying less for compute: Spot for interruptible work, reservation for steady fixed use, savings plan for steady flexible use, Hybrid Benefit for existing licenses')
    d.box(190, 8, 260, 34, [('🤔 How do you run it?','t')], 'cyan')
    qs = [
     ('⏸️ Can the work be interrupted?', 'batch, dev/test, jobs that checkpoint', 'Spot VMs', 'spare capacity, can be evicted', 'rose'),
     ('📌 Steady use of the same VM size and region?', 'running all month, every month', 'Reservation', 'prepaid, one or three years', 'emerald'),
     ('🔀 Steady spend, but sizes and services change?', 'a baseline you will always have', 'Savings plan', 'commit to hourly spend', 'cyan'),
     ('🪪 Own Windows Server or SQL licenses?', 'with Software Assurance or subscriptions', 'Hybrid Benefit', 'use what you own', 'violet'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 460
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 460, 330, 56, [('💳 Otherwise: pay as you go','t'),('no commitment, the highest unit price','s')], 'n')
    return d

def d_budget():
    d = Diagram('co3', 640, 270, 'Tags group costs, Cost Management compares them with a budget, and a budget alert can call an action group')
    d.box(10, 50, 130, 64, [('🏷️ Tagged','t'),('resources','t')], 'amber')
    d.box(250, 50, 140, 64, [('📊 Cost analysis','t'),('grouped by tag','s')], 'cyan')
    d.box(500, 50, 130, 64, [('🎯 Budget','t'),('limit and alerts','s')], 'violet')
    d.arrow([(140,82),(250,82)], 'amber', label='grouped in', at=(195,82))
    d.arrow([(390,82),(500,82)], 'violet', label='compared to', at=(441,82))
    d.box(500, 170, 130, 64, [('🔔 Action group','t'),('notify or act','s')], 'emerald')
    d.arrow([(565,114),(565,170)], 'emerald', label='alert at a threshold', at=(480,142))
    d.text(190, 188, 'Azure Policy can require the tag,', size=9.5)
    d.text(190, 204, 'so cost can be traced to an owner.', size=9.5)
    d.text(190, 232, 'Budgets alert you — on their own they do not stop spending.', size=9.5, weight=700)
    return d

def build_cost_management():
    body = ''
    body += see(figure(d_cycle(),
        'cost work is a <b>loop</b>. First <b>see</b> where the money goes — with tags, cost analysis, budgets and alerts. Then <b>stop paying for waste</b>: VMs nobody uses, disks left behind, resources bigger than they need to be. '
        'Only then <b>pay less for what stays</b>, with commitments and discounts. Doing it in this order matters: a discount on a resource you should have deleted is still waste.'))
    body += one('Cloud spend is metered, so cost is a design input: first see it, then cut the waste, and only then commit to a discount.')
    body += why([
      'Everything built so far is billed by the hour, by the gigabyte, by the request. Autoscale adds copies, the second region doubles the base, logs grow, a forgotten test environment keeps running. A design can be reliable, secure and fast — and still unaffordable.',
      'The good news is that the cloud also gives you the levers. You can <b>see</b> cost by team and by product, <b>cut</b> what is idle or oversized, and <b>commit</b> to steady use at a lower price. The architect\'s job is to make cost visible early and to treat it as one more trade-off, not a surprise on the invoice.'])
    body += block('🧰 The levers', pick_cards([
      dict(icon='📊', name='Cost Management', tag='see, analyse, budget', color='#22d3ee',
           use=['Cost analysis by subscription, resource group or tag', 'Budgets with alerts on actual or forecast spend', 'Recommendations and potential savings'],
           skip=['You expect it to cap spending — a budget alerts, it does not stop things by itself']),
      dict(icon='✂️', name='Rightsizing and cleanup', tag='stop paying for waste', color='#fbbf24',
           use=['Azure Advisor flags VMs with little use over a week and suggests shutting down or a cheaper size', 'Remove orphaned disks, IP addresses and other leftovers', 'Shut down non-production out of hours'],
           skip=['Doing it once — waste comes back']),
      dict(icon='📌', name='Reservations and savings plans', tag='commit for a lower price', color='#34d399',
           use=['Steady, predictable use', 'Reservation: prepaid for one or three years for a specific size and region', 'Savings plan for compute: the most flexible commitment, to an hourly spend'],
           skip=['Uncertain or short-lived workloads — a commitment you do not use is waste']),
      dict(icon='🎟️', name='Spot and Hybrid Benefit', tag='special discounts', color='#a78bfa',
           use=['Spot: spare capacity for interruptible work such as batch and dev/test', 'Hybrid Benefit: use existing Windows Server or SQL Server licenses'],
           skip=['Spot for anything that cannot be interrupted — Azure can take the VM back']),
    ]), label_cls='see')
    body += block('🧭 Paying less for compute', figure(d_choose(),
        'ask in order. <b>Can the work be interrupted?</b> Then Spot VMs, which use spare capacity at a big discount but can be evicted (with a short warning). <b>Steady use of one size and region?</b> A reservation. <b>Steady spend that changes shape?</b> A savings plan. <b>Own licenses?</b> Hybrid Benefit. '
        'If none fits, pay as you go — the flexible, most expensive unit price. The discount sizes change, so this page leaves out numbers; check the pricing pages.'), label_cls='see')
    body += block('🏷️ Tags and budgets', figure(d_budget(),
        '<b>Tags</b> are the way to add your own business meaning — team, product, environment — to cost data. Cost analysis groups spend by those tags. A <b>budget</b> compares spend (actual or forecast) with a limit and fires an alert at thresholds you choose, and the alert can call an <b>action group</b>, even one that stops VMs. '
        'Tags that must exist can be enforced with Azure Policy (concept 16).'), label_cls='see')
    body += block('📊 Which discount?', table(['','You commit to','Flexibility','Best when'], [
      ['💳 Pay as you go','Nothing','Highest','Short, unpredictable or experimental'],
      ['📌 Reservation','A specific size and region, for one or three years (prepaid)','Low','Steady, predictable, long-running'],
      ['🔀 Savings plan for compute','An hourly spend for one or three years','High','Steady spend with changing sizes and services'],
      ['⏸️ Spot','Nothing — but it can be taken away','n/a','Batch, dev/test, interruptible'],
      ['🪪 Hybrid Benefit','Licenses you already own','n/a','Windows Server or SQL Server workloads'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🌙','Dev and test run all night','Nobody uses them from evening to morning.','Shut down out of hours'),
      ('💾','Deleted VMs left their disks behind','Orphaned resources keep billing.','Find and remove orphans'),
      ('🏭','A database tier that runs 24/7 for years','The size will not change.','Reservation'),
      ('🧪','A nightly batch job that checkpoints','It can restart if interrupted.','Spot VMs'),
      ('🏷️','"Whose spend is this?"','Finance wants it by team.','Tags + cost analysis, enforced by Policy'),
      ('🔔','A bill that doubled last month','Find it before the next invoice.','Budget alerts on actual and forecast'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — details that surprise people', '''      <p><b>Tags and allocation.</b> Tags are the only way to add your own business context to cost details. Tag inheritance can copy subscription and resource-group tags onto the costs of their resources. Cost allocation rules can split shared costs, but they do not apply to purchases such as reservations and savings plans.</p>
      <p><b>Budgets.</b> They can be scoped to a subscription, a resource group or a set of resources, and can use actual or forecast cost. Because there is no built-in hard stop for a whole subscription, alerts and automation are your main defence.</p>
      <p><b>Spot VMs.</b> Azure can evict a Spot VM when it needs the capacity back, usually giving a short warning through Scheduled Events. Work that is not checkpointed is lost, so they suit interruptible jobs. You choose whether an evicted VM is deallocated (kept) or deleted.</p>
      <p><b>Design choices are cost choices.</b> A second region, extra copies, longer log retention and bigger SKUs all show up on the bill. The Well-Architected cost pillar asks you to weigh them against the value they give — which is the next, last concept.</p>''')
    body += recall([
      'Cost loop: see (tags, analysis, budgets) → cut waste (idle, orphaned, oversized) → commit (reservations, savings plans, Spot, Hybrid Benefit) → repeat.',
      'Reservation = prepaid, one or three years, specific size/region. Savings plan for compute = hourly spend commitment, most flexible. Spot = spare capacity, can be evicted.',
      'Budgets alert on actual or forecast spend and can trigger action groups; they do not cap spending by themselves.',
      'Tags give cost business meaning; enforce them with Azure Policy; cost allocation does not cover reservations or savings plans.',
      'Cut waste before you commit — discounts on waste are still waste.'])
    body += saythis('"I treat cost as a design input and a loop. First visibility: tags enforced by policy, cost analysis and budget alerts. Then waste: idle and oversized resources and orphans, with Advisor\'s help. '
      'Then commitments: reservations for steady fixed use, savings plans for steady flexible spend, Spot for interruptible work and Hybrid Benefit for licenses I already own."')
    body += trap([
      '<b>Buying a reservation before cleaning up.</b> You lock in a discount on resources that should not exist. Remove waste first, then commit to what remains.',
      'Second trap: <b>thinking a budget protects you.</b> A budget sends alerts; by itself it does not stop spending. Attach an action group, and watch the forecast, not only the actual.'])
    body += confuse('📌 Reservation', 'Commit to a specific resource (size and region) for one or three years, paid up front. Good for fixed, steady use.', '🔀 Savings plan', 'Commit to an hourly spend that applies across eligible compute. More flexible when sizes and services change.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># tag a resource group so its cost can be grouped by team</span>
az group update --name rg-shop-prod --tags team=checkout env=prod cost-center=cc-1042''',
      'Illustrative only — the tag names and values are examples; many teams enforce a fixed tag set with Azure Policy.'))
    body += next_box('You now have the building blocks, the safety, the signals and the bill. One last question remains: how do you judge all of it together? Next: Well-Architected &amp; Landing Zones.', 'well-architected.html', 'Well-Architected &amp; Landing Zones')
    body += fact_note(FOOT, [DOCS_CM, DOCS_BUD, DOCS_OPT, DOCS_ALLOC, DOCS_ADV, DOCS_SPOT, DOCS_WAF])
    return page('cost-management', 'Cost Management', 'Concept 18 of 19 · 🛠️ Shipping and operating',
        'Cloud spend is metered — so cost is a design input: <span class="grad-text">see it first, cut the waste, then commit to a discount.</span>',
        'Cost analysis, budgets, tags, reservations, savings plans, Spot and Hybrid Benefit: the levers an architect uses to keep a good design affordable.',
        'How would you control and reduce Azure costs?',
        body, CR + ['<span class="cur">Cost Management</span>'], '', search_title='Cost Management')
