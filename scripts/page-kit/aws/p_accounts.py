from kit import *
from p_common import CR

DOCS_ORG = ('AWS Organizations user guide', 'https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html')
DOCS_TERMS = ('Terminology and concepts for AWS Organizations', 'https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html')
DOCS_BILL = ('Consolidated billing for AWS Organizations', 'https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing.html')
DOCS_MULTI = ('Organizing your AWS environment using multiple accounts', 'https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official AWS docs.'

def d_tree():
    d = Diagram('ac1', 640, 336, 'An AWS organization is a tree: a management account creates it, a root holds organizational units, and accounts sit inside the units')
    d.box(10, 24, 190, 64, [('👑 Management account','t'),('pays the bill, no workloads','s')], 'amber')
    d.zone(240, 8, 390, 320, 'cyan', 'ORGANIZATION · a tree of accounts')
    d.box(350, 38, 170, 36, [('🌳 Root','t')], 'n')
    d.box(256, 120, 170, 40, [('📁 OU: Production','t')], 'violet')
    d.box(452, 120, 162, 40, [('📁 OU: Dev and test','t')], 'violet')
    d.box(256, 214, 76, 50, [('📦 App A','t')], 'emerald')
    d.box(350, 214, 76, 50, [('📦 App B','t')], 'emerald')
    d.box(452, 214, 162, 50, [('📦 Dev account','t')], 'emerald')
    d.arrow([(200,56),(240,56)], 'amber')
    d.arrow([(400,74),(400,97),(341,97),(341,120)], 'violet', label='holds', at=(371,97))
    d.arrow([(470,74),(470,97),(533,97),(533,120)], 'violet', label='holds', at=(501,97))
    d.arrow([(294,160),(294,214)], 'emerald', label='holds', at=(334,187))
    d.arrow([(388,160),(388,214)], 'emerald')
    d.arrow([(533,160),(533,214)], 'emerald', label='holds', at=(578,187))
    d.text(105, 130, 'A service control policy', anchor='middle', size=9.5)
    d.text(105, 146, 'attached to a unit limits', anchor='middle', size=9.5)
    d.text(105, 162, 'every account below it.', anchor='middle', size=9.5)
    d.text(105, 190, 'It filters. It never grants.', anchor='middle', size=9.5, weight=700)
    return d

def d_blast():
    d = Diagram('ac2', 640, 262, 'In one big account a mistake in dev can reach production; separate accounts keep each workload behind its own boundary')
    d.zone(10, 8, 305, 246, 'rose', 'ONE ACCOUNT · one shared boundary')
    d.box(24, 74, 90, 56, [('🧪 Dev','t'),('experiments','s')], 'n')
    d.box(210, 74, 90, 56, [('🏭 Prod','t'),('customers','s')], 'n')
    d.arrow([(114,102),(210,102)], 'rose', label='can reach', at=(162,102))
    d.text(162, 176, 'One wrong delete or one leaked', size=9.5)
    d.text(162, 192, 'key can touch everything.', size=9.5)
    d.zone(325, 8, 305, 246, 'emerald', 'ACCOUNT PER WORKLOAD · separate boundaries')
    d.box(339, 74, 90, 56, [('🧪 Dev','t'),('own account','s')], 'n')
    d.box(525, 74, 90, 56, [('🏭 Prod','t'),('own account','s')], 'n')
    d.arrow([(429,102),(525,102)], 'emerald', label='opt-in', at=(477,102), dash=True)
    d.text(477, 176, 'Crossing needs explicit access.', size=9.5)
    d.text(477, 192, 'The blast radius stays small.', size=9.5)
    return d

def d_choose():
    d = Diagram('ac3', 640, 428, 'Decision tree: a different environment, team or compliance need earns its own account; otherwise tag within one account')
    d.box(190, 8, 260, 34, [('🤔 New workload?','t')], 'cyan')
    qs = [
     ('🏭 Production vs non-production?', 'different risk and different people', 'Separate accounts', 'prod apart from dev', 'emerald'),
     ('💳 Different bill or owner?', 'a team or product that pays its own way', 'Own account', 'bill by account', 'cyan'),
     ('📜 Different compliance rules?', 'regulated data needs its own guardrails', 'Own account + OU', 'policies per unit', 'violet'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 366
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 366, 330, 50, [('🏷️ None of these?','t'),('stay in one account, use tags','s')], 'n')
    return d

def build_accounts_organizations():
    body = ''
    body += see(figure(d_tree(),
        'an <b>AWS organization</b> is a tree. A <b>management account</b> creates it and pays the bill. Under the <b>root</b> you make <b>organizational units</b> (OUs) — folders for accounts that need similar rules — and the <b>accounts</b> sit inside them. '
        'A policy attached to a unit flows down to every account below it. That is the whole idea: accounts are the walls, the tree is how you manage many walls at once.'))
    body += one('An AWS account is the basic container for everything you build — the wall around your resources, your permissions and your bill — and an organization lets you manage many of those walls together.')
    body += why([
      'Before you deploy anything on AWS you need three things: <b>a place for it to live</b>, <b>a unit that gets billed</b>, and <b>a boundary that permissions attach to</b>. In AWS all three are the same thing: the <b>account</b>. Nothing comes before it in this journey.',
      'The first account is easy. The trouble comes later, when production, test, a second team and a regulated project all end up in it. One wrong delete or one leaked key then reaches everything. So AWS practice is <b>many accounts</b> — one per environment or workload — tied together by <b>AWS Organizations</b> so they can still be billed, governed and secured as one.'])
    body += block('🧰 The pieces', pick_cards([
      dict(icon='📦', name='Account', tag='the container and the boundary', color='#34d399',
           use=['Holds your resources, permissions and usage for one workload or environment', 'A natural unit for billing and for limiting blast radius'],
           skip=['Putting every workload in one account — the boundary then protects nothing']),
      dict(icon='🌳', name='Organization, root and OUs', tag='manage many accounts as a tree', color='#22d3ee',
           use=['A management account, member accounts and organizational units', 'Attach a policy to a unit and it flows to all accounts below', 'A member account belongs to one organization; an account sits in exactly one OU'],
           skip=['Treating OUs as billing groups — they are for applying policy']),
      dict(icon='🛡️', name='Service control policies (SCPs)', tag='guardrails for whole accounts', color='#a78bfa',
           use=['Limit what accounts may do, whatever their own IAM says', 'Block regions or services you never use', 'They filter — they never grant access'],
           skip=['Expecting an SCP to give someone permission — IAM (concept 3) does that']),
      dict(icon='💳', name='Consolidated billing', tag='one bill for the whole organization', color='#fbbf24',
           use=['The management account pays for all member accounts', 'Combined usage can share volume pricing discounts, Reserved Instance discounts and Savings Plans'],
           skip=['Consolidated billing alone gives no policies — the "all features" mode does (and is the default)']),
    ]), label_cls='see')
    body += block('🧭 When to create a new account', figure(d_choose(),
        'a new account is cheap and a missing boundary is expensive, so ask in order. <b>Production versus non-production?</b> Separate accounts. <b>A different bill or owner?</b> Its own account. <b>Different compliance rules?</b> Its own account, often in its own OU so the right policies attach. '
        'If none of these is true, stay in one account and separate things with tags.'), label_cls='see')
    body += block('💥 Why one account is not enough', figure(d_blast(),
        'on the left, dev and production share a single boundary: a bad script or a leaked key in dev can reach production. On the right, each workload has its own account. '
        'Reaching across is not impossible, but it has to be allowed on purpose — so a mistake stays small. This idea is called limiting the <b>blast radius</b>.'), label_cls='see')
    body += block('📊 Account, OU and organization', table(['','What it is','Use it for','Watch out for'], [
      ['📦 Account','The container and boundary for resources, permissions and billing','One workload, environment or team','Many accounts need a tool to manage them'],
      ['📁 OU','A folder of accounts (can nest; one parent each)','Applying the same policies to similar accounts','Each account is in exactly one OU'],
      ['👑 Management account','The account that created the organization','Creating accounts, attaching policies, paying the bill','Keep workloads out of it; SCPs do not apply to it'],
      ['🛡️ SCP','A filter on what accounts may use','Guardrails across many accounts','Effective permissions = what the SCP allows AND what IAM allows'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🏭','Production and test on one account','A test script deletes the wrong database.','Separate prod and non-prod accounts'),
      ('🧾','Finance asks "what does team B cost?"','One bill, no split.','An account per team, consolidated billing'),
      ('🌍','Only two Regions are allowed by law','Developers can pick any Region.','An SCP on the OU'),
      ('🔐','Audit logs must never be changed by app teams','Different people, different trust.','A separate security account'),
      ('🧪','A new project, same team, same rules','No new boundary needed.','Stay in the account, use tags'),
      ('👑','Someone runs workloads in the management account','Its mistakes cannot be limited by SCPs.','Move workloads to member accounts'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — who does what in an organization', '''      <p><b>Management account.</b> The account that created the organization; this cannot be changed later. It can create accounts, invite others, attach policies and pays the charges for the whole organization. AWS recommends keeping workloads out of it, because SCPs and similar policies do not apply to the management account.</p>
      <p><b>Member accounts</b> are every other account. An account can belong to only one organization at a time.</p>
      <p><b>SCPs are filters.</b> An SCP never grants permissions; it limits what permissions can be used. A principal\'s effective permissions are the overlap between the SCPs and its own IAM policies.</p>
      <p><b>Feature sets.</b> "All features" (the default) turns on policies and service integrations. "Consolidated billing" alone covers only billing.</p>
      <p><b>Landing zones.</b> Setting up the standard set of accounts and guardrails once, so every new account starts safe, is the idea behind a landing zone — the last concept in this journey.</p>''')
    body += recall([
      'An account is the container, the permission boundary and the billing unit. Use several to limit blast radius.',
      'Organizations: a management account, member accounts, OUs in a tree. Policies attached to a node flow down.',
      'SCPs filter what accounts may use; they never grant access. Effective permission = SCP ∩ IAM.',
      'Consolidated billing: one bill, shared volume and commitment discounts. "All features" is the default and adds policies.',
      'Keep workloads out of the management account.'])
    body += saythis('"In AWS the account is the basic boundary for resources, permissions and billing, so I use separate accounts for production and non-production and for teams with different needs. '
      'AWS Organizations ties them into a tree of OUs under a management account, gives one consolidated bill and lets me attach service control policies, which only limit — never grant — what the accounts can do. I keep workloads out of the management account."')
    body += trap([
      '<b>One big account "for now".</b> It is the easiest start and the hardest thing to untangle later. Create the accounts you need early; they cost nothing by themselves.',
      'Second trap: <b>thinking an SCP gives access.</b> It does not. If IAM does not allow an action, the SCP cannot make it allowed — it can only take permission away.'])
    body += confuse('📦 Account', 'The wall: one container for resources, permissions and cost.', '🌳 Organization', 'The tree: how many walls are created, grouped, governed and billed together.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># create a member account inside an existing organization</span>
aws organizations create-account --email prod-app@example.com --account-name "prod-app"''',
      'Illustrative shape only — real setups also place the account in an OU, set up access for people, and use automation; flags can change.'))
    body += next_box('You now have accounts to put things in. Next question: <b>where</b> on the planet do those resources run, and what happens if one location fails? Next: Regions &amp; Availability Zones.', 'regions-availability-zones.html', 'Regions &amp; Availability Zones')
    body += fact_note(FOOT, [DOCS_ORG, DOCS_TERMS, DOCS_BILL, DOCS_MULTI])
    return page('accounts-organizations', 'Accounts & Organizations', 'Concept 1 of 19 · 🏗️ Foundations',
        'An AWS account is the wall around your resources, permissions and bill — <span class="grad-text">and an organization manages many walls together.</span>',
        'Accounts, AWS Organizations, OUs, service control policies and consolidated billing: how to give every workload a safe place to live.',
        'Why do AWS teams use multiple accounts, and what does AWS Organizations add?',
        body, CR + ['<span class="cur">Accounts &amp; Organizations</span>'], '', search_title='Accounts & Organizations')
