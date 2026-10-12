from kit import *
from p_common import CR

DOCS_CFN = ('AWS CloudFormation user guide', 'https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html')
DOCS_CDK = ('AWS CDK developer guide', 'https://docs.aws.amazon.com/cdk/v2/guide/home.html')
DOCS_CHOOSE = ('Choosing an IaC tool (Prescriptive Guidance)', 'https://docs.aws.amazon.com/prescriptive-guidance/latest/choose-iac-tool/introduction.html')
DOCS_TF = ('Getting started with Terraform (Prescriptive Guidance)', 'https://docs.aws.amazon.com/prescriptive-guidance/latest/getting-started-terraform/introduction.html')
FOOT = 'Tools and versions change often. This page teaches the ideas; for current syntax, versions and features, check the official AWS docs.'

def d_flow():
    d = Diagram('ia1', 640, 210, 'Infrastructure as code flow: a template in Git, a change set preview, a deployment, and AWS resources that match the template')
    d.box(10, 56, 120, 64, [('📄 Template','t'),('lives in Git','s')], 'violet')
    d.box(240, 56, 150, 64, [('👀 Change set','t'),('what will change?','s')], 'amber')
    d.box(510, 56, 120, 64, [('☁️ AWS','t'),('matches the file','s')], 'emerald')
    d.arrow([(130,88),(240,88)], 'amber', label='preview', at=(185,88))
    d.arrow([(390,88),(510,88)], 'emerald', label='deploy', at=(450,88))
    d.text(320, 168, 'Want a change? Edit the template and review it — do not click it into the console.', size=9.5, weight=700)
    d.text(320, 188, 'Then the same template can build the same environment again, anywhere.', size=9.5)
    return d

def d_cdk():
    d = Diagram('ia2', 640, 250, 'The CDK turns code in a familiar language into a CloudFormation template, and from there the process is the same as CloudFormation')
    d.box(10, 90, 130, 64, [('💻 CDK code','t'),('TypeScript, Python…','s')], 'violet')
    d.box(250, 90, 140, 64, [('📄 Template','t'),('CloudFormation','s')], 'amber')
    d.box(500, 90, 130, 64, [('📦 Stack','t'),('real resources','s')], 'emerald')
    d.arrow([(140,122),(250,122)], 'amber', label='synthesize', at=(195,122))
    d.arrow([(390,122),(500,122)], 'emerald', label='deploy', at=(445,122))
    d.text(320, 206, 'Constructs are reusable pieces; one construct can stand for several resources.', size=9.5, weight=700)
    return d

def d_choose():
    d = Diagram('ia3', 640, 428, 'Decision tree for infrastructure-as-code tools: CloudFormation templates, CDK for real programming languages, Terraform for several providers')
    d.box(190, 8, 260, 34, [('🤔 Which tool?','t')], 'cyan')
    qs = [
     ('📄 AWS only, and you like declarative files?', 'JSON or YAML templates', 'CloudFormation', 'AWS-native service', 'amber'),
     ('💻 AWS only, and you prefer real code?', 'loops, functions, reuse', 'AWS CDK', 'generates CloudFormation', 'violet'),
     ('🌐 Other clouds or providers in the same code?', 'one tool and workflow for all', 'Terraform', 'keeps a state file', 'emerald'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 366
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 366, 330, 50, [('🤔 Still unsure?','t'),('start with CloudFormation or CDK','s')], 'n')
    return d

def build_infrastructure_as_code():
    body = ''
    body += see(figure(d_flow(),
        'the environment lives in a <b>template</b>, kept in Git like any other code. Before deploying, a <b>change set</b> shows what would be created, changed or deleted — a preview. Then the deployment makes AWS match the template. '
        'To change the environment, you change the template and get it reviewed. The same template can build the same environment again, in a new account or a new Region.'))
    body += one('Infrastructure as code means your environment is described in files that you can review, repeat and roll back — instead of being a pile of clicks nobody remembers.')
    body += why([
      'By now the system is dozens of resources: networks, servers, databases, queues, functions. Someone clicked them together in the console. Ask three questions: <b>Can we build the same thing again?</b> (a second environment, or after a disaster) <b>Who changed what, and why?</b> <b>Does production really match staging?</b> With clicking, the honest answer to all three is "not sure".',
      'Infrastructure as code (IaC) answers all three. You describe what you want and a tool makes AWS match. The file is the record, it goes through review like code, and it is the plan for the disaster-recovery day from the Scaling concept.'])
    body += block('🧰 Which tool?', pick_cards([
      dict(icon='📄', name='AWS CloudFormation', tag='AWS-native templates and stacks', color='#fbbf24',
           use=['You work on AWS only', 'A template describes resources; a stack is the deployed, trackable unit', 'Change sets preview changes'],
           skip=['You also manage non-AWS providers in the same code']),
      dict(icon='💻', name='AWS CDK', tag='infrastructure in a programming language', color='#a78bfa',
           use=['Write infrastructure in familiar languages, with loops and functions', 'Constructs package reusable patterns', 'It generates CloudFormation templates'],
           skip=['You want a no-code, purely declarative file — and note each account and Region needs a bootstrapped environment']),
      dict(icon='🌐', name='Terraform', tag='multi-provider, with a state file', color='#34d399',
           use=['One tool across AWS, other clouds and services', 'A plan shows changes before apply'],
           skip=['You want AWS to track state for you — Terraform keeps its own state, which you must store and protect']),
    ]), label_cls='see')
    body += block('💻 How the CDK fits', figure(d_cdk(),
        'with the <b>CDK</b> you write infrastructure in a language like TypeScript or Python. <b>Synthesizing</b> turns it into a CloudFormation template; after that the process is identical to CloudFormation. A <b>construct</b> is a reusable piece that represents one or more CloudFormation resources. '
        'So CDK and CloudFormation are not rivals: the CDK is a nicer way to write the template.'), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'if your world is AWS only, <b>CloudFormation</b> or the <b>CDK</b> are the usual starting points: files if you like them declarative, code if you want loops and reuse. If the same code must also manage other clouds or services, <b>Terraform</b> is the common choice. '
        'AWS\'s guide maps the vocabulary for you: a CloudFormation change set is the equivalent of a Terraform plan, and a template is the equivalent of a configuration.'), label_cls='see')
    body += block('📊 Side by side', table(['','CloudFormation','CDK','Terraform'], [
      ['Written as','JSON or YAML template','Code in a programming language','Configuration files'],
      ['Scope','AWS','AWS (via CloudFormation)','Many providers'],
      ['Preview','Change set','Change set (after synthesis)','Plan'],
      ['State','Tracked by the stack','Tracked by the stack','Your state file — store and protect it'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🧪','Spin up a test copy of production','Same shape, smaller, deleted on Friday.','The same template with parameters'),
      ('🆘','The primary Region is gone','Build the second Region fast, not by memory.','Deploy the same template to the other Region'),
      ('👀','A teammate wants to change a security group','Someone should review it first.','Pull request + change set'),
      ('💻','The same pattern ten times','Do not copy and paste.','A CDK construct'),
      ('☁️','AWS plus another provider, one team','Same workflow for both.','Terraform'),
      ('🖱️','Someone fixes something in the console','Production no longer matches the template.','Drift — detect it and fix the template'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — stacks, drift and state', '''      <p><b>Stacks.</b> A stack is infrastructure as code deployed and tracked as a single unit; a template is one CloudFormation file. A change set lets you review a change before it runs.</p>
      <p><b>Drift</b> is when the real environment stops matching the template, usually because someone changed something in the console. Treat the console as read-only for anything the code owns, and let the pipeline (next concept) deploy.</p>
      <p><b>CDK bootstrapping.</b> The CDK needs a bootstrapped environment in each account and Region it deploys to.</p>
      <p><b>Terraform state.</b> Terraform records what it manages in its own state; store it remotely, limit access and back it up. There is also a CDK variant for Terraform that lets you write Terraform configuration in a programming language.</p>''')
    body += recall([
      'IaC = the environment described in reviewed, versioned files; repeatable, reviewable, recoverable.',
      'CloudFormation: templates and stacks, change sets to preview. CDK: code that synthesizes into CloudFormation. Terraform: multi-provider with a state file.',
      'A CloudFormation change set ≈ a Terraform plan; a template ≈ a configuration.',
      'The CDK needs a bootstrapped environment per account and Region.',
      'Drift = reality no longer matches the template; avoid console edits for code-managed resources.'])
    body += saythis('"I define environments as code so they are repeatable, reviewable and recoverable. On AWS only I use CloudFormation, often through the CDK so I can use a programming language; if I must manage several providers I use Terraform and protect its state. '
      'I preview with change sets or plans, and I keep the console read-only for anything the code owns so there is no drift."')
    body += trap([
      '<b>Fixing things in the console "just this once".</b> The template no longer matches reality, and the next deployment may undo your fix — or fail.',
      'Second trap: <b>leaving the Terraform state file somewhere unprotected.</b> It is the tool\'s record of your infrastructure and can contain sensitive data; store it remotely, with access limited and backups on.'])
    body += confuse('📄 CloudFormation', 'You write the template; AWS tracks the stack. Declarative.', '💻 CDK', 'You write code; it produces the CloudFormation template for you.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># a CloudFormation template (YAML) that creates one S3 bucket</span>
Resources:
  ReportsBucket:
    Type: AWS::S3::Bucket
    Properties:
      VersioningConfiguration:
        Status: Enabled''',
      'Illustrative only — a real template adds encryption, access rules and tags, and names are chosen per environment.'))
    body += next_box('Environments are now code. But code needs a safe, automatic way to <b>build, test and roll out</b> — and to roll back when something goes wrong. Next: CI/CD &amp; Deployment Strategies.', 'ci-cd-deployment.html', 'CI/CD &amp; Deployment Strategies')
    body += fact_note(FOOT, [DOCS_CFN, DOCS_CDK, DOCS_CHOOSE, DOCS_TF])
    return page('infrastructure-as-code', 'Infrastructure as Code', 'Concept 13 of 19 · 🛠️ Shipping and operating',
        'Infrastructure as code turns your environment into files you can <span class="grad-text">review, repeat and roll back.</span>',
        'CloudFormation, the CDK and Terraform: why clicking resources together stops working, how a preview protects you, and which tool to pick.',
        'What is infrastructure as code, and would you use CloudFormation, the CDK or Terraform on AWS?',
        body, CR + ['<span class="cur">Infrastructure as Code</span>'], '', search_title='Infrastructure as Code')
