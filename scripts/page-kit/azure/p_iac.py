from kit import *
from p_storage import CR

DOCS_BICEP = ('What is Bicep?', 'https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview')
DOCS_WHATIF = ('Bicep what-if', 'https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-what-if')
DOCS_TFB = ('Comparing Terraform and Bicep', 'https://learn.microsoft.com/en-us/azure/developer/terraform/comparing-terraform-and-bicep')
DOCS_AVM = ('Azure Verified Modules', 'https://learn.microsoft.com/en-us/community/content/azure-verified-modules')
DOCS_ARM = ('Azure Resource Manager documentation', 'https://learn.microsoft.com/en-us/azure/azure-resource-manager/')
FOOT = 'Tools and versions change often. This page teaches the ideas; for current syntax, versions and features, check the official docs.'

def d_flow():
    d = Diagram('ia1', 640, 210, 'Infrastructure as code flow: a file in Git, a what-if preview, a deployment, and Azure resources that match the file')
    d.box(10, 56, 110, 64, [('📄 Bicep file','t'),('lives in Git','s')], 'violet')
    d.box(240, 56, 150, 64, [('👀 Preview','t'),('what will change?','s')], 'amber')
    d.box(510, 56, 120, 64, [('☁️ Azure','t'),('matches the file','s')], 'emerald')
    d.arrow([(120,88),(240,88)], 'amber', label='what-if', at=(180,88))
    d.arrow([(390,88),(510,88)], 'emerald', label='deploy', at=(450,88))
    d.text(320, 168, 'Want a change? Edit the file and review it — do not click it into the portal.', size=9.5, weight=700)
    d.text(320, 188, 'Then the same file can build the same environment again, anywhere.', size=9.5)
    return d

def d_modes():
    d = Diagram('ia2', 640, 258, 'Incremental mode leaves resources that are not in the file alone; complete mode deletes them')
    d.zone(10, 8, 305, 242, 'emerald', 'INCREMENTAL · the default')
    d.box(24, 64, 90, 60, [('📄 File','t'),('A and B','s')], 'n')
    d.box(206, 64, 94, 60, [('🗂️ Group','t'),('A, B, C all stay','s')], 'emerald')
    d.arrow([(114,94),(206,94)], 'emerald', label='deploy', at=(160,94))
    d.text(162, 176, 'C is not in the file,', size=9.5)
    d.text(162, 192, 'so it is left alone.', size=9.5)
    d.zone(325, 8, 305, 242, 'rose', 'COMPLETE · be careful')
    d.box(339, 64, 90, 60, [('📄 File','t'),('A and B','s')], 'n')
    d.box(521, 64, 94, 60, [('🗂️ Group','t'),('A, B only','s')], 'rose')
    d.arrow([(429,94),(521,94)], 'rose', label='deploy', at=(475,94))
    d.text(477, 176, 'C is not in the file,', size=9.5)
    d.text(477, 192, 'so it is deleted.', size=9.5, weight=700)
    d.text(477, 220, 'Run what-if first.', size=9.5, weight=700)
    return d

def d_choose():
    d = Diagram('ia3', 640, 428, 'Decision tree for infrastructure-as-code tools: Bicep for Azure only, Terraform for several providers, ARM templates for existing JSON')
    d.box(190, 8, 260, 34, [('🤔 Which tool?','t')], 'cyan')
    qs = [
     ('☁️ Only Azure, and no state file to look after?', 'Azure-native, deployed through ARM', 'Bicep', 'the usual Azure choice', 'violet'),
     ('🌐 Other clouds or providers in the same code?', 'one tool and workflow for all', 'Terraform', 'keeps a state file', 'emerald'),
     ('📜 Already have JSON templates that work?', 'keep them; Bicep compiles to this', 'ARM templates', 'what Azure runs underneath', 'n'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 366
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 366, 330, 50, [('🤔 Still unsure?','t'),('start with Bicep for Azure-only teams','s')], 'emerald')
    return d

def build_infrastructure_as_code():
    body = ''
    body += see(figure(d_flow(),
        'the environment lives in a <b>file</b>, kept in Git like any other code. Before deploying, <b>what-if</b> shows what would be created, changed or deleted — a preview, without touching anything. Then the deployment makes Azure match the file. '
        'To change the environment, you change the file and get it reviewed. The same file can build the same environment again, in a new subscription or a new region.'))
    body += one('Infrastructure as code means your environment is described in files that you can review, repeat and roll back — instead of being a pile of clicks nobody remembers.')
    body += why([
      'By now the system is dozens of resources: networks, apps, databases, caches, queues, functions. Someone clicked them together in the portal. Ask three questions: <b>Can we build the same thing again?</b> (a second environment, or after a disaster) <b>Who changed what, and why?</b> <b>Does production really match staging?</b> With clicking, the honest answer to all three is "not sure".',
      'Infrastructure as code (IaC) answers all three. You write what you want — <i>declaratively</i>: "there should be a storage account like this" — and a tool makes Azure match. The file is the record, it goes through review like code, and it is the plan for the disaster-recovery day from the Scaling concept.'])
    body += block('🧰 Which tool?', pick_cards([
      dict(icon='💪', name='Bicep', tag='Azure-native, declarative', color='#a78bfa',
           use=['You work on Azure only', 'Microsoft\'s own language for Azure resources', 'No state file — Azure itself tracks deployments', 'The default tool for the Azure Developer CLI'],
           skip=['You also manage other clouds or non-Azure services in the same code']),
      dict(icon='🌐', name='Terraform', tag='multi-provider, with a state file', color='#34d399',
           use=['One tool across Azure, other clouds and services', 'Plan and apply with a recorded state'],
           skip=['You want Azure to hold the record — Terraform keeps its own state file that you must store and protect']),
      dict(icon='📜', name='ARM templates (JSON)', tag='what Azure Resource Manager runs', color='#93a0b8',
           use=['You already have working templates', 'Bicep files are turned into this format when deployed'],
           skip=['Writing new ones by hand — Bicep is shorter and easier to read']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'if your world is Azure only, <b>Bicep</b> is the usual starting point. If the same code must also manage other clouds or services, <b>Terraform</b> is the common choice. If you already have JSON <b>ARM templates</b> that work, keep them — Azure Resource Manager (concept 1) is what runs everything underneath anyway.'), label_cls='see')
    body += block('📊 Bicep vs Terraform', table(['','Bicep','Terraform'], [
      ['Scope','Azure resources','Azure plus other providers'],
      ['State','No state file; relies on incremental deployments','Keeps a state file, which you store remotely and protect'],
      ['Where the work happens','On the Azure side','Planning runs on your side, using state and its own language'],
      ['Sign-in','Uses your deployment token','Uses provider credentials'],
      ['Ready-made modules','Azure Verified Modules','Azure Verified Modules'],
    ]), label_cls='see')
    body += block('⚠️ The one setting that can delete things', figure(d_modes(),
        'a deployment has a <b>mode</b>. <b>Incremental</b> (the default) adds and updates what is in the file and leaves everything else in the resource group alone. <b>Complete</b> also deletes anything in the group that is <em>not</em> in the file. '
        'That can be what you want for a tidy group — and a disaster if you forgot a resource. Microsoft\'s advice: run <b>what-if</b> before any complete-mode deployment.'), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🧪','Spin up a test copy of production','Same shape, smaller sizes, deleted on Friday.','Parameters on one Bicep file'),
      ('🆘','The primary region is gone','Build the second region fast, not by memory.','Deploy the same file to the other region'),
      ('👀','A teammate wants to change a firewall rule','Someone should review it first.','Pull request on the file + what-if'),
      ('🧹','Clean up a resource group','Remove everything not in the file.','Complete mode — after what-if'),
      ('☁️','Azure plus another cloud, one team','Same workflow for both.','Terraform'),
      ('🧩','Repeating the same pattern 20 times','Do not copy and paste.','A reusable module (e.g. Azure Verified Modules)'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — modules, parameters and drift', '''      <p><b>Parameters</b> let one file build many environments (dev, test, prod) with different names and sizes. <b>Modules</b> package a pattern so you reuse it instead of copying it. <b>Azure Verified Modules</b> are ready-made, versioned modules from Microsoft for both Bicep and Terraform, aligned with the Well-Architected Framework.</p>
      <p><b>Idempotent:</b> deploying the same Bicep file twice leaves the existing resources as they are — the result is the same, not a duplicate.</p>
      <p><b>Drift</b> is when the real environment stops matching the file, usually because someone changed something in the portal. Treat the portal as read-only for anything the code owns, and let the pipeline (next concept) do the deploying.</p>
      <p><b>Scopes.</b> A deployment can target a resource group, a subscription, a management group or the tenant — matching the hierarchy from concept 1.</p>''')
    body += recall([
      'IaC = the environment described in reviewed, versioned files; repeatable, reviewable, recoverable.',
      'Bicep: declarative, Azure-native, no state file. Terraform: multi-provider, keeps a state file. ARM templates: the JSON underneath.',
      'what-if previews changes (create, modify, delete) without changing anything.',
      'Incremental mode (default) leaves extra resources alone; complete mode deletes resources not in the file — what-if first.',
      'Drift = reality no longer matches the file; avoid portal edits for code-managed resources.'])
    body += saythis('"I define environments as code so they are repeatable, reviewable and recoverable. On Azure only I use Bicep, which is declarative and needs no state file; if I must manage several providers I use Terraform and protect its state. '
      'Before deploying I run what-if, I use incremental mode by default, and I keep the portal read-only for anything the code owns so there is no drift."')
    body += trap([
      '<b>Complete mode with a missing resource.</b> It will delete whatever is not in the file. Always preview with what-if, and use complete mode on purpose, not by habit.',
      'Second trap: <b>leaving the Terraform state file somewhere unprotected.</b> It is the tool\'s record of your infrastructure and can contain sensitive data; store it remotely, with access limited and backups on.'])
    body += confuse('💪 Bicep', 'Azure-only, declarative. Azure itself tracks deployments, so there is no state file to look after.', '🌐 Terraform', 'Many providers in one workflow. It keeps its own state file that you must store and protect.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt">// a storage account in Bicep — declare what you want, not the steps to get it</span>
param location string = resourceGroup().location

resource sa 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'stshopprod001'
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}''',
      'Illustrative only — the API version, the name and the SKU are examples; storage account names must be globally unique, and real files add tags, network rules and more.'))
    body += next_box('Environments are now code. But code needs a safe, automatic way to <b>build, test and roll out</b> — and to roll back when something goes wrong. Next: CI/CD &amp; Deployment Strategies.', 'ci-cd-deployment.html', 'CI/CD &amp; Deployment Strategies')
    body += fact_note(FOOT, [DOCS_BICEP, DOCS_WHATIF, DOCS_TFB, DOCS_AVM, DOCS_ARM])
    return page('infrastructure-as-code', 'Infrastructure as Code', 'Concept 13 of 19 · 🛠️ Shipping and operating',
        'Infrastructure as code turns your environment into files you can <span class="grad-text">review, repeat and roll back.</span>',
        'Bicep, Terraform and ARM templates: why clicking resources together stops working, how a preview protects you, and which tool to pick.',
        'What is infrastructure as code, and would you use Bicep or Terraform on Azure?',
        body, CR + ['<span class="cur">Infrastructure as Code</span>'], '', search_title='Infrastructure as Code')
