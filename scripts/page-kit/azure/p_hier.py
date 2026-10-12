from kit import *
from p_storage import CR

DOCS_ARM = ('Azure Resource Manager documentation', 'https://learn.microsoft.com/en-us/azure/azure-resource-manager/')
DOCS_GOV = ('Azure governance (management groups) documentation', 'https://learn.microsoft.com/en-us/azure/governance/')
DOCS_CAF = ('Cloud Adoption Framework', 'https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official docs.'

def d_tree():
    d = Diagram('rh1', 640, 388, 'Azure resource hierarchy: a tenant contains management groups, which contain subscriptions, which contain resource groups, which contain resources; roles and policies flow downward')
    d.zone(10, 8, 470, 368, 'violet', 'TENANT · Microsoft Entra ID (your directory)')
    d.zone(22, 36, 446, 330, 'cyan', 'MANAGEMENT GROUPS · optional folders of subscriptions')
    d.zone(34, 64, 208, 290, 'amber', 'SUBSCRIPTION · Prod')
    d.zone(254, 64, 208, 290, 'amber', 'SUBSCRIPTION · Dev')
    d.zone(46, 92, 184, 122, 'emerald', 'RESOURCE GROUP · rg-web')
    d.box(58, 120, 160, 34, [('🌐 Web app','t')], 'n')
    d.box(58, 162, 160, 34, [('🔌 API app','t')], 'n')
    d.zone(46, 226, 184, 118, 'emerald', 'RESOURCE GROUP · rg-data')
    d.box(58, 254, 160, 34, [('🛢️ SQL database','t')], 'n')
    d.box(58, 296, 160, 34, [('🗂️ Storage account','t')], 'n')
    d.zone(266, 92, 184, 122, 'emerald', 'RESOURCE GROUP · rg-dev')
    d.box(278, 120, 160, 34, [('🧪 Test web app','t')], 'n')
    d.box(278, 162, 160, 34, [('🧪 Test database','t')], 'n')
    d.box(490, 78, 140, 56, [('📌 Assign a role','t'),('or a policy here','s')], 'violet')
    d.box(490, 300, 140, 56, [('✅ Applies to','t'),('everything below it','s')], 'emerald')
    d.arrow([(560,134),(560,300)], 'violet', label='flows down', at=(523,217))
    return d

def d_group():
    d = Diagram('rh2', 640, 252, 'Grouping resources by lifecycle (one group per app) versus by type (all databases together)')
    d.zone(10, 8, 305, 236, 'emerald', 'GROUP BY LIFECYCLE ✅')
    d.zone(24, 38, 134, 136, 'n', 'rg-shop-prod')
    d.box(36, 64, 110, 28, [('🌐 shop-web','b')], 'n')
    d.box(36, 98, 110, 28, [('🛢️ shop-db','b')], 'n')
    d.box(36, 132, 110, 28, [('🗂️ shop-files','b')], 'n')
    d.zone(168, 38, 134, 136, 'n', 'rg-blog-prod')
    d.box(180, 64, 110, 28, [('🌐 blog-web','b')], 'n')
    d.box(180, 98, 110, 28, [('🛢️ blog-db','b')], 'n')
    d.text(162, 198, 'Retire the blog? Delete one group.', size=9.5, weight=700)
    d.text(162, 216, 'Things that live and die together stay together.', size=9.5)
    d.zone(325, 8, 305, 236, 'rose', 'GROUP BY TYPE ⚠️')
    d.zone(339, 38, 134, 136, 'n', 'rg-all-web')
    d.box(351, 64, 110, 28, [('🌐 shop-web','b')], 'n')
    d.box(351, 98, 110, 28, [('🌐 blog-web','b')], 'n')
    d.zone(483, 38, 134, 136, 'n', 'rg-all-databases')
    d.box(495, 64, 110, 28, [('🛢️ shop-db','b')], 'n')
    d.box(495, 98, 110, 28, [('🛢️ blog-db','b')], 'n')
    d.text(477, 198, 'Retire the blog? Hunt through every group.', size=9.5, weight=700)
    d.text(477, 216, 'One app is scattered across many groups.', size=9.5)
    return d

def d_arm():
    d = Diagram('rh3', 640, 270, 'Every tool sends its request to Azure Resource Manager, which passes it to the resource provider that owns each kind of resource')
    clients = [('🖱️ Portal','the web UI'),('⌨️ CLI','and PowerShell'),('📦 SDKs','from your code'),('📄 Bicep','templates (IaC)')]
    d.box(250, 16, 140, 218, [('🧭 Azure Resource','t'),('Manager (ARM)','t'),('checks who you are,','s'),('what you may do,','s'),('and the policy','s')], 'cyan')
    for i, (t, s_) in enumerate(clients):
        y = 16 + i*58
        d.box(10, y, 140, 44, [(t,'t'),(s_,'s')], 'n')
        d.arrow([(150,y+22),(250,y+22)], 'cyan', label='REST call', at=(200,y+22))
    provs = [(36,'Microsoft.Compute','virtual machines'),(100,'Microsoft.Storage','storage accounts'),(164,'Microsoft.Network','virtual networks')]
    for y, t, s_ in provs:
        d.box(490, y, 140, 46, [(t,'t'),(s_,'s')], 'violet')
        d.arrow([(390,y+23),(490,y+23)], 'violet', label='routes to', at=(440,y+23))
    d.text(560, 252, 'resource providers', size=9, mono=True)
    return d

def build_resource_hierarchy():
    body = ''
    body += see(figure(d_tree(),
        'every Azure resource lives in a family tree. At the top is your <b>tenant</b> — your organization\'s Microsoft Entra ID directory. Under it you can add <b>management groups</b> (optional folders), then <b>subscriptions</b>, then <b>resource groups</b>, and finally the <b>resources</b> themselves: web apps, databases, storage accounts. '
        'The box on the right is the most important rule: a <b>role or a policy assigned at one level applies to everything below it</b>.'))
    body += one('Before you deploy anything, Azure asks three questions: where does it live, who pays for it, and who may touch it. The hierarchy answers all three.')
    body += why([
      'This is where the journey starts, so nothing came before it. Think about what happens without structure: fifty resources dropped into one pile. '
      'You cannot tell which ones belong to which app, you cannot send one team its own bill, and you cannot give a contractor access to one app without handing over the keys to everything.',
      'The hierarchy fixes that with four simple layers, each with one job: the <b>tenant</b> says who can sign in, <b>management groups</b> apply rules to many subscriptions at once, a <b>subscription</b> is the unit of billing and access, '
      'and a <b>resource group</b> keeps one app\'s resources together so they can be managed — and deleted — as one.'])
    body += block('🧰 The four layers — what each one is for', pick_cards([
      dict(icon='🏢', name='Tenant', tag="your organization's directory of identities (Microsoft Entra ID)", color='#a78bfa',
           use=['Decide who can sign in: users, groups and apps', 'One directory that many subscriptions trust', 'Every subscription trusts exactly one tenant'],
           skip=['Separating Dev from Prod — use subscriptions for that', 'Thinking of it as a bill — the tenant itself holds identities, not costs']),
      dict(icon='🗂️', name='Management group', tag='an optional folder that holds subscriptions', color='#22d3ee',
           use=['Apply the same role or policy to many subscriptions at once', 'Mirror your company: departments, environments', 'Keep rules in one place instead of copying them'],
           skip=['A single subscription — you do not need one', 'Holding resources — resources never sit directly in a management group']),
      dict(icon='💳', name='Subscription', tag='the unit of billing and access, where resources are created', color='#fbbf24',
           use=['Give a team or environment its own bill and budget', 'A strong boundary for access and limits', 'Keep Prod and Dev apart'],
           skip=['Grouping the pieces of one app — that is a resource group', 'Creating dozens with no plan — decide a pattern first']),
      dict(icon='📦', name='Resource group', tag='a container for resources that share a lifecycle', color='#34d399',
           use=['Keep one app\'s resources together', 'Delete everything for an app in one step', 'Give a role to just that app'],
           skip=['Grouping by type ("all databases") — it scatters each app', 'Using it as a security wall — permissions come from roles']),
    ]))
    body += block('🧱 Grouping resources: by lifecycle, not by type', figure(d_group(),
        'the rule of thumb is to put resources that <b>deploy together and retire together</b> into one resource group. On the left, each app has its own group, so retiring the blog means deleting one group. '
        'On the right, resources are grouped by type — all web apps in one group, all databases in another — so one app is scattered over many groups and every change touches several of them.'), label_cls='see')
    body += block('📊 The levels side by side', table(['Level','What sits inside it','Its main job'], [
      ['Tenant','Users, groups, apps — and the subscriptions that trust it','Identity: who can sign in'],
      ['Management group','Subscriptions and other management groups','Governance: roles and policy for many subscriptions'],
      ['Subscription','Resource groups','Billing and access boundary'],
      ['Resource group','Resources','Lifecycle: manage and delete together'],
      ['Resource','—','The real thing: a VM, a database, a storage account'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios — which level?', scenarios([
      ('💰','Finance wants its own bill','The finance team should see and control its own costs.','Its own subscription'),
      ('📜','"Only EU regions" for every team','One rule must apply to every subscription in the company.','Policy on a management group'),
      ('🧹','Delete the demo on Friday','A demo with a web app, a database and storage should vanish in one step.','One resource group per demo'),
      ('🧑‍💻','A contractor sees one app','They must work on the web app and nothing else.','A role on that resource group'),
      ('🚧','Dev must never touch Prod','A mistake in Dev must not be able to reach Prod.','Separate subscriptions (plus roles)'),
      ('🏷️','Cost report by project','Costs must roll up by project across many groups.','Tags on resources'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — Azure Resource Manager', figure(d_arm(),
        'whichever tool you use — the portal, the CLI, an SDK in your code, or a Bicep template — it sends a REST request to <b>Azure Resource Manager (ARM)</b>. ARM checks who you are, what you may do and which policies apply, then hands the work to the <b>resource provider</b> that owns that kind of resource. '
        'That is why the same roles and policies work no matter which tool you use.') +
        '''      <p><b>Good to know.</b> A subscription trusts one tenant; one tenant can have many subscriptions. Each resource belongs to exactly one resource group (you can move it). '
      The <i>location</i> of a resource group is only where its metadata is stored — its resources can live in other regions. Deleting a resource group deletes every resource inside it.</p>''')
    body += recall([
      'Hierarchy: tenant → management groups (optional) → subscriptions → resource groups → resources.',
      'Roles and policies assigned at a level are inherited by everything below it.',
      'Subscription = billing and access boundary. Resource group = lifecycle container. Tenant = identity directory.',
      'A subscription trusts one tenant; a resource belongs to one resource group; deleting a resource group deletes its resources.',
      'Group resources by lifecycle (one app together), not by type.'])
    body += saythis('"Azure organizes everything in a hierarchy: a Microsoft Entra tenant for identity, optional management groups to apply governance across subscriptions, subscriptions as the billing and access boundary, '
      'and resource groups to hold resources that share a lifecycle. Roles and policies are inherited downward, so I assign them at the highest sensible level. I group resources by application lifecycle, not by type."')
    body += trap([
      '<b>A resource group is not a region, and not a security wall.</b> Its location only says where its metadata is stored. Resources inside it can be in other regions, and being in the same group gives nobody any permission by itself — permissions come from role assignments.',
      'Second trap: <b>deleting a resource group deletes everything inside it</b> — including the database. Use resource locks and separate groups for anything you cannot afford to lose.'])
    body += confuse('🏢 Tenant', 'The directory of identities (Microsoft Entra ID). It decides who you are. It is not where resources live.', '💳 Subscription', 'The container where resources are created and billed. It trusts one tenant, and a tenant can have many subscriptions.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># create a resource group — its location says where the group's metadata is stored</span>
az group create --name rg-shop-prod --location westeurope

<span class="cmt"># delete it — this removes EVERY resource inside the group (the CLI asks you to confirm)</span>
az group delete --name rg-shop-demo''',
      'Illustrative shape only — real teams create groups from templates (Bicep) and protect important ones with locks.'))
    body += next_box('You now know how Azure is organized. Next question: <b>where in the world</b> do those resources physically live — and what happens if a datacenter fails?', 'regions-availability-zones.html', 'Regions &amp; Availability Zones')
    body += fact_note(FOOT, [DOCS_ARM, DOCS_GOV, DOCS_CAF])
    return page('resource-hierarchy', 'Tenants, Subscriptions & Resource Groups', 'Concept 1 of 19 · 🏗️ Foundations',
        'Before you deploy anything, Azure asks <span class="grad-text">where it lives, who pays, and who may touch it.</span>',
        'Every Azure resource sits in a family tree: tenant, management groups, subscriptions, resource groups, resources. Learn what each level is for — and why a role or policy set high in the tree reaches everything below.',
        'Explain Azure\'s resource hierarchy — what are tenants, management groups, subscriptions and resource groups for?',
        body, CR + ['<span class="cur">Resource Hierarchy</span>'], '', search_title='Tenants, Subscriptions & Resource Groups')
