from kit import *
from p_common import CR

DOCS_DG = ('Choosing an AWS cost management strategy', 'https://docs.aws.amazon.com/decision-guides/latest/cost-management-on-aws-how-to-choose/cost-management-on-aws-how-to-choose.html')
DOCS_CM = ('AWS Billing and Cost Management', 'https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html')
DOCS_TAG = ('Building a cost allocation strategy (tagging)', 'https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/building-a-cost-allocation-strategy.html')
DOCS_BUD = ('Establish cloud budgets and forecasts', 'https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_cloud_financial_management_budget_forecast.html')
DOCS_PM = ('Perform pricing model analysis', 'https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_pricing_model_analysis.html')
DOCS_CO = ('AWS Compute Optimizer', 'https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html')
FOOT = 'Prices, discount levels and offers change often, so this page uses no price numbers. For current prices and terms, check the official AWS docs and the pricing calculator.'

def d_cycle():
    d = Diagram('co1', 640, 294, 'The cost loop: see where the money goes, stop paying for waste, pay less for what stays, then review again')
    rows = [
      ('👀 See where the money goes','tags, Cost Explorer, budgets and alerts','cyan'),
      ('✂️ Stop paying for waste','idle, oversized and forgotten resources','amber'),
      ('🏷️ Pay less for what stays','Savings Plans, Reserved Instances, Spot','emerald'),
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
    d = Diagram('co2', 640, 536, 'Decision tree for paying less for compute: Spot for interruptible work, Reserved Instances for steady fixed use, Savings Plans for steady flexible spend')
    d.box(190, 8, 260, 34, [('🤔 How do you run it?','t')], 'cyan')
    qs = [
     ('⏸️ Can the work be interrupted?', 'batch, test, jobs that checkpoint', 'Spot Instances', 'spare capacity, can stop', 'rose'),
     ('📌 Steady use of one instance family?', 'running all month, every month', 'Reserved Instances', 'commit to specific use', 'emerald'),
     ('🔀 Steady spend, but the shape changes?', 'a baseline you always have', 'Savings Plans', 'commit to $/hour', 'cyan'),
     ('📏 Are you sure the size is right?', 'check before you commit', 'Compute Optimizer', 'resize first', 'violet'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 460
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 460, 330, 56, [('💳 Otherwise: On-Demand','t'),('no commitment, flexible, highest unit price','s')], 'n')
    return d

def d_budget():
    d = Diagram('co3', 640, 270, 'Tags group costs, Cost Explorer shows them, and a budget compares spend to a limit and sends an alert')
    d.box(10, 50, 130, 64, [('🏷️ Tagged','t'),('resources','t')], 'amber')
    d.box(250, 50, 140, 64, [('📊 Cost Explorer','t'),('grouped by tag','s')], 'cyan')
    d.box(500, 50, 130, 64, [('🎯 Budget','t'),('limit and alerts','s')], 'violet')
    d.arrow([(140,82),(250,82)], 'amber', label='grouped in', at=(195,82))
    d.arrow([(390,82),(500,82)], 'violet', label='compared to', at=(441,82))
    d.box(500, 170, 130, 64, [('🔔 Alert','t'),('notify or act','s')], 'emerald')
    d.arrow([(565,114),(565,170)], 'emerald', label='at a threshold', at=(490,142))
    d.text(190, 188, 'Cost allocation tags show which team', size=9.5)
    d.text(190, 204, 'or product drives spend.', size=9.5)
    d.text(190, 232, 'Budgets alert you — they do not stop spending.', size=9.5, weight=700)
    return d

def build_cost_management():
    body = ''
    body += see(figure(d_cycle(),
        'cost work is a <b>loop</b>. First <b>see</b> where the money goes — with tags, Cost Explorer, budgets and alerts. Then <b>stop paying for waste</b>: servers nobody uses, resources bigger than they need to be, things left behind. '
        'Only then <b>pay less for what stays</b>, with commitments and discounts. Doing it in this order matters: a discount on a resource you should have deleted is still waste.'))
    body += one('Cloud spend is metered, so cost is a design input: see it first, cut the waste, then commit to a discount.')
    body += why([
      'Everything built so far is billed by the hour, by the gigabyte, by the request. Auto Scaling adds copies, the second Region doubles the base, logs grow, a forgotten test environment keeps running. A design can be reliable, secure and fast — and still unaffordable.',
      'The good news is that AWS also gives you the levers. You can <b>see</b> cost by team and by workload, <b>cut</b> what is idle or oversized, and <b>commit</b> to steady use at a lower price. The architect\'s job is to make cost visible early and to treat it as one more trade-off, not a surprise on the invoice.'])
    body += block('🧰 The levers', pick_cards([
      dict(icon='📊', name='Cost Explorer, Budgets, Cost Categories', tag='see, analyse, budget', color='#22d3ee',
           use=['Cost Explorer shows which services drive spend; cost allocation tags break it down by team or workload', 'AWS Budgets: custom cost and usage budgets with alerts; filter by tags', 'Cost Categories group accounts and tags into business views'],
           skip=['Expecting a budget to stop spending — it alerts']),
      dict(icon='📏', name='Compute Optimizer and cleanup', tag='stop paying for waste', color='#fbbf24',
           use=['Recommends right-sized compute for your workload', 'Start with a generic size, then resize on real CPU and memory use', 'Remove resources nobody uses'],
           skip=['Doing it once — waste comes back']),
      dict(icon='📌', name='Savings Plans and Reserved Instances', tag='commit for a lower price', color='#34d399',
           use=['Savings Plans: a commitment measured in dollars per hour for one or three years, more flexible', 'Reserved Instances: can be cheaper still for steady workloads, less flexible', 'Cost Explorer makes purchase recommendations'],
           skip=['Uncertain or short-lived workloads — an unused commitment is waste']),
      dict(icon='🎟️', name='Spot Instances', tag='spare capacity at a discount', color='#a78bfa',
           use=['Request spare compute at a discounted hourly rate, with no upfront commitment', 'Suits non-critical, interruptible work'],
           skip=['Anything that cannot be interrupted']),
    ]), label_cls='see')
    body += block('🧭 Paying less for compute', figure(d_choose(),
        'ask in order. <b>Can the work be interrupted?</b> Spot Instances. <b>Steady use of one instance family?</b> Reserved Instances. <b>Steady spend that changes shape?</b> Savings Plans — the Well-Architected guidance suggests working toward them as the more flexible option. '
        '<b>Not sure the size is right?</b> Resize with Compute Optimizer before you commit. If none fits, On-Demand is the flexible, most expensive unit price. Discount sizes change, so this page quotes none.'), label_cls='see')
    body += block('🏷️ Tags and budgets', figure(d_budget(),
        '<b>Cost allocation tags</b> let you see spend by team or workload in Cost Explorer. A <b>budget</b> compares spend to a limit and alerts you; AWS suggests one budget for overall account spend and another per workload using tags. '
        'One catch: fees for commitments such as Savings Plans and Reserved Instances cannot be tagged in advance, so you look at amortized cost grouped by tag afterwards.'), label_cls='see')
    body += block('📊 Which discount?', table(['','You commit to','Flexibility','Best when'], [
      ['💳 On-Demand','Nothing','Highest','Short, unpredictable or experimental'],
      ['📌 Reserved Instances','A specific usage, for one or three years','Lower','Steady, predictable, long-running'],
      ['🔀 Savings Plans','An hourly spend for one or three years','Higher','Steady spend with changing sizes and services'],
      ['⏸️ Spot','Nothing — but it can be taken away','n/a','Interruptible, non-critical work'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🌙','Dev and test run all night','Nobody uses them from evening to morning.','Shut down out of hours'),
      ('💾','Deleted servers left things behind','Forgotten resources keep billing.','Find and remove them'),
      ('🏭','A database tier that runs 24/7 for years','The size will not change.','Reserved or Savings Plan, after checking the size'),
      ('🧪','A nightly batch job that checkpoints','It can restart if interrupted.','Spot Instances'),
      ('🏷️','"Whose spend is this?"','Finance wants it by team.','Cost allocation tags + Cost Explorer'),
      ('🔔','A bill that doubled last month','Find it before the next invoice.','Budget alerts'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — details that surprise people', '''      <p><b>Commitments.</b> Savings Plans offer lower prices than On-Demand in exchange for a specific usage commitment, measured in dollars per hour, for a one- or three-year period. Reserved Instances can be cheaper still for steady workloads but are less flexible.</p>
      <p><b>Spot.</b> Spot Instances let you request spare compute capacity at a discounted hourly rate with no upfront commitment. AWS guidance is to use them for non-critical workloads.</p>
      <p><b>Tags.</b> Cost allocation tags combined with Cost Explorer show which teams or parts of the organization drive spend; Cost Categories group accounts and tags into business-unit views that also appear in Budgets and Cost Anomaly Detection.</p>
      <p><b>Design choices are cost choices.</b> A second Region, extra copies, longer log retention and bigger instances all show up on the bill. The Well-Architected cost pillar asks you to weigh them against the value they give — which is the next, last concept.</p>''')
    body += recall([
      'Cost loop: see (tags, Cost Explorer, budgets) → cut waste (idle, oversized) → commit (Savings Plans, Reserved Instances, Spot) → repeat.',
      'Savings Plans = commitment in dollars per hour, one or three years, more flexible. Reserved Instances = less flexible. Spot = spare capacity, can be interrupted.',
      'AWS Budgets alert on cost and usage; they do not cap spending by themselves.',
      'Cost allocation tags give cost business meaning; commitment fees cannot be tagged in advance — use amortized cost.',
      'Resize with Compute Optimizer before you commit; cut waste before discounts.'])
    body += saythis('"I treat cost as a design input and a loop. First visibility: cost allocation tags, Cost Explorer and budget alerts. Then waste: idle and oversized resources, checked with Compute Optimizer. '
      'Then commitments: Savings Plans for steady flexible spend, Reserved Instances for steady fixed use, and Spot for interruptible work."')
    body += trap([
      '<b>Buying a commitment before cleaning up.</b> You lock in a discount on resources that should not exist. Remove waste first, then commit to what remains.',
      'Second trap: <b>thinking a budget protects you.</b> A budget sends alerts; by itself it does not stop spending. Watch forecasts as well as actuals, and act on the alert.'])
    body += confuse('📌 Reserved Instances', 'Commit to specific usage for one or three years. Can be cheaper for steady, fixed use.', '🔀 Savings Plans', 'Commit to an hourly spend. More flexible when sizes and services change.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># tag a resource so its cost can be grouped by team in Cost Explorer</span>
aws ec2 create-tags --resources &lt;instance-id&gt; --tags Key=team,Value=checkout Key=env,Value=prod''',
      'Illustrative only — tag keys must also be activated as cost allocation tags in billing before they appear in cost reports.'))
    body += next_box('You now have the building blocks, the safety, the signals and the bill. One last question remains: how do you judge all of it together? Next: Well-Architected &amp; Landing Zones.', 'well-architected.html', 'Well-Architected &amp; Landing Zones')
    body += fact_note(FOOT, [DOCS_DG, DOCS_CM, DOCS_TAG, DOCS_BUD, DOCS_PM, DOCS_CO])
    return page('cost-management', 'Cost Management', 'Concept 18 of 19 · 🛠️ Shipping and operating',
        'Cloud spend is metered — so cost is a design input: <span class="grad-text">see it first, cut the waste, then commit to a discount.</span>',
        'Cost Explorer, Budgets, tags, Savings Plans, Reserved Instances, Spot and Compute Optimizer: the levers an architect uses to keep a good design affordable.',
        'How would you control and reduce AWS costs?',
        body, CR + ['<span class="cur">Cost Management</span>'], '', search_title='Cost Management')
