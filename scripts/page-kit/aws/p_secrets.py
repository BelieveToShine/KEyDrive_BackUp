from kit import *
from p_common import CR

DOCS_SM = ('AWS Secrets Manager user guide', 'https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html')
DOCS_PS = ('AWS Systems Manager Parameter Store', 'https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html')
DOCS_INT = ('Using Secrets Manager secrets in Parameter Store', 'https://docs.aws.amazon.com/secretsmanager/latest/userguide/integrating_parameterstore.html')
DOCS_KMS = ('AWS Key Management Service', 'https://docs.aws.amazon.com/kms/latest/developerguide/overview.html')
DOCS_WKLD = ('Use ephemeral secrets or a secrets-management service', 'https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-startup-security-baseline/wkld-03.html')
DOCS_ECS = ('Pass sensitive data to an Amazon ECS container', 'https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html')
FOOT = 'Cloud services change often. This page teaches the ideas; for current features, roles and limits, check the official AWS docs.'

def d_ladder():
    d = Diagram('sx1', 640, 246, 'Four places a secret can live, from worst to best: in the code, in a config file, in Secrets Manager, or no stored secret at all with an IAM role')
    boxes = [
      (10,  'rose',    [('💥 In the code','t'),('ends up in Git','s'),('and in every copy','s')]),
      (168, 'amber',   [('📄 Config file','t'),('lives beside the app','s'),('easy to leak','s')]),
      (326, 'cyan',    [('🔑 Secrets Manager','t'),('one guarded place','s'),('rotation, audit','s')]),
      (484, 'emerald', [('🪪 No secret','t'),('an IAM role','s'),('nothing to leak','s')]),
    ]
    for x, col, lines in boxes:
        d.box(x, 40, 146, 100, lines, col)
    d.arrow([(83,140),(83,174),(557,174),(557,140)], 'emerald', label='safer, and easier to rotate', at=(320,174))
    d.text(320, 220, 'Whenever the target accepts IAM sign-in, prefer the role over any stored secret.', size=9.5, weight=700)
    return d

def d_flow():
    d = Diagram('sx2', 640, 262, 'The app uses its IAM role to read plain settings from Parameter Store and secrets from Secrets Manager; Parameter Store can reference a Secrets Manager secret; KMS encrypts both')
    d.box(10, 100, 120, 70, [('📱 App','t'),('IAM role','s')], 'n')
    d.box(270, 30, 140, 60, [('⚙️ Parameter Store','t'),('settings','s')], 'violet')
    d.box(270, 180, 140, 60, [('🔑 Secrets Manager','t'),('secrets','s')], 'cyan')
    d.arrow([(130,120),(200,120),(200,60),(270,60)], 'violet', label='settings', at=(200,90))
    d.arrow([(130,150),(200,150),(200,210),(270,210)], 'cyan', label='secrets', at=(200,180))
    d.arrow([(340,90),(340,180)], 'cyan', label='can point to', at=(405,135))
    d.text(500, 56, 'Both encrypt values', anchor='start', size=9.5)
    d.text(500, 72, 'with AWS KMS. An IAM', anchor='start', size=9.5)
    d.text(500, 88, 'policy decides what the', anchor='start', size=9.5)
    d.text(500, 104, 'role may read.', anchor='start', size=9.5)
    return d

def d_choose():
    d = Diagram('sx3', 640, 428, 'Decision tree: use an IAM role if the target accepts it, Secrets Manager for a secret that rotates, Parameter Store for plain configuration')
    d.box(190, 8, 260, 34, [('🤔 What do you need to store?','t')], 'cyan')
    qs = [
     ('🪪 Does the target accept IAM sign-in?', 'AWS services you call from your code', 'IAM role', 'no secret to store', 'emerald'),
     ('🔑 A real secret that should rotate?', 'database credentials, API keys, tokens', 'Secrets Manager', 'automatic rotation', 'cyan'),
     ('⚙️ A setting, not a secret?', 'changes between environments', 'Parameter Store', 'hierarchical parameters', 'violet'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 366
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 366, 330, 50, [('🤔 Still unsure?','t'),('secrets never go in code or Git','s')], 'emerald')
    return d

def build_secrets_configuration():
    body = ''
    body += see(figure(d_ladder(),
        'four places a secret can live. In the <b>code</b> is the worst: it is copied into Git, builds and every developer\'s laptop. A <b>config file</b> is a little better but still travels with the app. <b>Secrets Manager</b> keeps secrets in one guarded place with rotation and audit. '
        'The best secret is <b>no secret</b>: when the target accepts IAM sign-in, a role (concept 3) needs nothing stored at all. Move right whenever you can.'))
    body += one('Keep secrets out of code and out of pipelines: ask for them at run time from a guarded place, using the app\'s own role — or avoid having a secret at all.')
    body += why([
      'The last concept built a pipeline that deploys without a stored key. But the app itself still needs things: a database password, an API key for a payment provider, and plain settings like "which environment is this?".',
      'The classic leak is putting those in code or in a pipeline variable. Both get copied, logged and shared. The fix has two halves. <b>Secrets</b> (things that must stay hidden) go to a service with access control, audit and rotation. <b>Settings</b> (things that just change) go to a configuration store. Both encrypt with <b>AWS KMS</b>.'])
    body += block('🧰 The pieces', pick_cards([
      dict(icon='🪪', name='IAM roles', tag='no stored secret at all', color='#34d399',
           use=['The target accepts IAM sign-in', 'Temporary, automatically rotated credentials', 'Nothing to store, rotate or leak'],
           skip=['The other side only understands passwords or keys → get them from Secrets Manager']),
      dict(icon='🔑', name='AWS Secrets Manager', tag='secrets with rotation', color='#22d3ee',
           use=['Database credentials, API keys and tokens', 'Automatic rotation; random secret generation; cross-account sharing; cross-Region replication', 'Rotation of database credentials expects the stored JSON to follow the database secret structure'],
           skip=['Large amounts of plain, frequently read configuration — Parameter Store fits that better']),
      dict(icon='⚙️', name='Systems Manager Parameter Store', tag='configuration and light secrets', color='#a78bfa',
           use=['Plain settings and frequently read configuration', 'Standard-tier parameters up to a small size have no charge', 'SecureString values encrypted with KMS'],
           skip=['A secret that must rotate on its own — Parameter Store has no automatic rotation']),
      dict(icon='🗝️', name='AWS KMS', tag='the keys that encrypt', color='#fbbf24',
           use=['Both secret services encrypt with KMS keys', 'Control who may use a key with key policies and IAM'],
           skip=['Treating KMS as a place to store application secrets — it manages encryption keys']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'ask in order. <b>Does the target accept IAM sign-in?</b> Use a role and store nothing. <b>A real secret that should rotate?</b> Secrets Manager. <b>A setting?</b> Parameter Store. '
        'AWS\'s guidance is the same: use ephemeral credentials where you can, and a secrets-management service for the rest. A common split: Secrets Manager for secrets that benefit from rotation; Parameter Store for frequently read configuration.'), label_cls='see')
    body += block('🔌 How the app gets them', figure(d_flow(),
        'the app uses its <b>IAM role</b> to sign in — it never holds a password. It reads <b>settings</b> from Parameter Store and <b>secrets</b> from Secrets Manager. A Parameter Store parameter can <em>point to</em> a Secrets Manager secret, so one place holds the value. '
        'Each read needs an IAM permission on that one parameter or secret — least privilege applied to data. For containers, services such as ECS can inject these values at launch.'), label_cls='see')
    body += block('📊 Side by side', table(['','Holds','Rotation','Watch out for'], [
      ['🪪 IAM role','Nothing — it is an identity','Automatic','The target must accept IAM sign-in'],
      ['🔑 Secrets Manager','Secrets','Automatic, built in','Billed per secret and per API call'],
      ['⚙️ Parameter Store','Settings and light secrets','None built in','Do not rely on it to rotate secrets'],
      ['📄 Config file / pipeline variable','Whatever you put in it','Redeploy','The classic leak'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🗄️','App talks to S3 and DynamoDB','Both accept IAM sign-in.','An IAM role, no keys'),
      ('💳','A payment provider API key','Only a key is accepted; it must stay hidden.','Secrets Manager + an IAM role'),
      ('🔄','A database password that must rotate','The app must not break when it changes.','Secrets Manager rotation'),
      ('🌍','Same app in dev, test and prod','Different settings per environment.','Parameter Store hierarchy'),
      ('🧑‍💻','A developer commits a key by mistake','It is now in Git history.','Rotate it, then move it to Secrets Manager'),
      ('📦','A container needs a secret at launch','Environment variables risk leaks.','Inject from Secrets Manager (or a sidecar)'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — what AWS says', '''      <p><b>Rotation.</b> Parameter Store does not rotate stored secrets; AWS suggests keeping the secret in Secrets Manager and referencing it from Parameter Store. Secrets Manager adds automatic rotation, random secret generation and cross-account sharing.</p>
      <p><b>Cost shape.</b> Standard-tier parameters have no charge below a small value size, while Secrets Manager charges per secret per month and per API call. This page quotes no prices; check the pricing pages.</p>
      <p><b>Containers.</b> Passing secrets as environment variables carries a higher risk of leakage; one AWS guide describes a sidecar that reads from Secrets Manager and writes to a shared volume.</p>
      <p><b>Ephemeral first.</b> AWS\'s security baseline recommends ephemeral secrets or a secrets-management service rather than long-lived static credentials.</p>''')
    body += recall([
      'Best to worst: no secret (IAM role) → Secrets Manager → config file → in the code.',
      'Secrets Manager = secrets with rotation, sharing and replication. Parameter Store = configuration (and light secrets) with no automatic rotation.',
      'A Parameter Store parameter can reference a Secrets Manager secret.',
      'Both encrypt with KMS; IAM policies decide what a role may read.',
      'Containers: avoid plain environment variables for secrets where you can.'])
    body += saythis('"I avoid secrets where I can: IAM roles for anything that accepts IAM sign-in. Where a secret is unavoidable it lives in Secrets Manager, which rotates it, and the app reads it with its role. '
      'Plain settings go to Parameter Store, which can also reference a Secrets Manager secret. Both encrypt with KMS, and nothing sensitive goes in code or pipeline variables."')
    body += trap([
      '<b>Putting the secret in the pipeline variable "just for now".</b> Variables are copied into logs, forks and screenshots. Use OIDC for the pipeline and roles or Secrets Manager for the app.',
      'Second trap: <b>using Parameter Store for a secret and never rotating it.</b> It stores the value safely but does not rotate it. Without rotation, one leaked secret works forever.'])
    body += confuse('🔑 Secrets Manager', 'Holds secrets that must stay hidden, with automatic rotation and sharing.', '⚙️ Parameter Store', 'Holds settings and light secrets in a hierarchy; no built-in rotation.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># read a secret at run time — the caller needs an IAM permission for this one secret</span>
aws secretsmanager get-secret-value --secret-id prod/shop/db''',
      'Illustrative shape only — the secret name is a placeholder; real apps use an SDK and cache the value.'))
    body += next_box('Secrets are one slice of security. An architect also needs guardrails that apply to every resource, layers that protect each other, and a way to see threats. Next: Security &amp; Governance.', 'security-governance.html', 'Security &amp; Governance')
    body += fact_note(FOOT, [DOCS_SM, DOCS_PS, DOCS_INT, DOCS_KMS, DOCS_WKLD, DOCS_ECS])
    return page('secrets-configuration', 'Secrets & Configuration', 'Concept 15 of 19 · 🛠️ Shipping and operating',
        'Keep secrets out of code: <span class="grad-text">ask for them at run time from a guarded place — or avoid having a secret at all.</span>',
        'IAM roles, Secrets Manager, Parameter Store and KMS: where each kind of value belongs and how the app reads it.',
        'Where do you keep secrets and configuration for an AWS app, and why?',
        body, CR + ['<span class="cur">Secrets &amp; Configuration</span>'], '', search_title='Secrets & Configuration')
