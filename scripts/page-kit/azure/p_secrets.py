from kit import *
from p_storage import CR

DOCS_KV = ('Azure Key Vault overview', 'https://learn.microsoft.com/en-us/azure/key-vault/general/overview')
DOCS_KVR = ('Key Vault RBAC guide', 'https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide')
DOCS_AC = ('Azure App Configuration overview', 'https://learn.microsoft.com/en-us/azure/azure-app-configuration/overview')
DOCS_SEC = ('Best practices for protecting secrets', 'https://learn.microsoft.com/en-us/azure/security/fundamentals/secrets-best-practices')
DOCS_ROT = ('Understanding autorotation in Key Vault', 'https://learn.microsoft.com/en-us/azure/key-vault/general/autorotation')
DOCS_REF = ('Key Vault references in App Service', 'https://learn.microsoft.com/en-us/azure/app-service/app-service-key-vault-references')
FOOT = 'Cloud services change often. This page teaches the ideas; for current features, roles and limits, check the official docs.'

def d_ladder():
    d = Diagram('sx1', 640, 246, 'Four places a secret can live, from worst to best: in the code, in a config file, in Key Vault, or no secret at all with a managed identity')
    boxes = [
      (10,  'rose',    [('💥 In the code','t'),('ends up in Git','s'),('and in every copy','s')]),
      (168, 'amber',   [('📄 Config file','t'),('lives beside the app','s'),('easy to leak','s')]),
      (326, 'cyan',    [('🔑 Key Vault','t'),('one guarded place','s'),('audited access','s')]),
      (484, 'emerald', [('🪪 No secret','t'),('a managed identity','s'),('nothing to leak','s')]),
    ]
    for x, col, lines in boxes:
        d.box(x, 40, 146, 100, lines, col)
    d.arrow([(83,140),(83,174),(557,174),(557,140)], 'emerald', label='safer, and easier to rotate', at=(320,174))
    d.text(320, 220, 'Whenever the target service accepts a token, prefer the identity over any stored secret.', size=9.5, weight=700)
    return d

def d_flow():
    d = Diagram('sx2', 640, 262, 'The app reads plain settings from App Configuration and secrets from Key Vault using its managed identity; App Configuration can point to a secret in Key Vault')
    d.box(10, 100, 120, 70, [('📱 App','t'),('managed identity','s')], 'n')
    d.box(270, 30, 140, 60, [('⚙️ App Config','t'),('settings, flags','s')], 'violet')
    d.box(270, 180, 140, 60, [('🔑 Key Vault','t'),('secrets, keys','s')], 'cyan')
    d.arrow([(130,120),(200,120),(200,60),(270,60)], 'violet', label='settings', at=(200,90))
    d.arrow([(130,150),(200,150),(200,210),(270,210)], 'cyan', label='secrets', at=(200,180))
    d.arrow([(340,90),(340,180)], 'cyan', label='points to a secret', at=(415,135))
    d.text(500, 56, 'Entra ID checks who', anchor='start', size=9.5)
    d.text(500, 72, 'is asking; a role (such', anchor='start', size=9.5)
    d.text(500, 88, 'as Key Vault Secrets', anchor='start', size=9.5)
    d.text(500, 104, 'User) decides what it', anchor='start', size=9.5)
    d.text(500, 120, 'may read.', anchor='start', size=9.5)
    return d

def d_choose():
    d = Diagram('sx3', 640, 428, 'Decision tree: use a managed identity if the target accepts tokens, Key Vault for a real secret, App Configuration for plain settings and feature flags')
    d.box(190, 8, 260, 34, [('🤔 What do you need to store?','t')], 'cyan')
    qs = [
     ('🪪 Does the target accept Entra ID sign-in?', 'storage, SQL, Key Vault and more', 'Managed identity', 'no secret to store', 'emerald'),
     ('🔑 A real secret: password, key, certificate?', 'must stay hidden and be rotated', 'Key Vault', 'guarded and audited', 'cyan'),
     ('⚙️ A setting or a feature flag, not a secret?', 'changes between environments', 'App Configuration', 'change without redeploy', 'violet'),
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
        'four places a secret can live. In the <b>code</b> is the worst: it is copied into Git, builds and every developer\'s laptop. A <b>config file</b> is a little better but still travels with the app. <b>Key Vault</b> keeps secrets in one guarded, audited place. '
        'The best secret is <b>no secret</b>: when the service accepts a token, a managed identity (concept 3) needs nothing stored at all. Move right whenever you can.'))
    body += one('Keep secrets out of code and out of pipelines: ask for them at run time from a guarded place, using the app\'s own identity — or avoid having a secret at all.')
    body += why([
      'The last concept built a pipeline that deploys without a stored password. But the app itself still needs things: a database connection string, an API key for a payment provider, a certificate, and plain settings like "which environment is this?" or "is the new checkout switched on?".',
      'The classic leak is putting those in code or in a pipeline variable. Both get copied, logged and shared. The fix has two halves. <b>Secrets</b> (things that must stay hidden) go to a vault with access control, audit and rotation. <b>Settings</b> (things that just change) go to a configuration store, so you can change them without redeploying.'])
    body += block('🧰 The pieces', pick_cards([
      dict(icon='🪪', name='Managed identity', tag='no stored secret at all', color='#34d399',
           use=['The target service accepts Entra ID tokens', 'Microsoft recommends it over shared keys, for Azure workloads', 'Nothing to store, rotate or leak'],
           skip=['The other side only understands passwords or keys → get them from Key Vault']),
      dict(icon='🔑', name='Azure Key Vault', tag='secrets, keys and certificates', color='#22d3ee',
           use=['Passwords, API keys, connection strings, certificates', 'Audited, access-controlled, soft-delete and purge protection', 'Rotation, with the app always reading the latest version'],
           skip=['Plain settings and feature flags — App Configuration fits them better']),
      dict(icon='⚙️', name='Azure App Configuration', tag='settings and feature flags', color='#a78bfa',
           use=['Settings shared by many apps and environments', 'Feature flags to release a feature without a deployment', 'It can hold a pointer to a Key Vault secret'],
           skip=['Anything that is a secret itself — keep that in Key Vault, and reference it']),
      dict(icon='🔗', name='Key Vault references', tag='a setting that points to a secret', color='#fbbf24',
           use=['App Service and App Configuration can resolve a secret from Key Vault at run time', 'The app never sees the vault wiring'],
           skip=['The app\'s identity has no access to the vault — the reference will not resolve']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'ask three questions in order. <b>Can the target accept a token?</b> Then use a managed identity and store nothing. <b>Is it a real secret?</b> Then Key Vault. <b>Is it a plain setting or a feature flag?</b> Then App Configuration. '
        'Microsoft\'s own guidance points the same way: use managed identity where supported, and where a secret is unavoidable, fetch it from Key Vault rather than embedding it.'), label_cls='see')
    body += block('🔌 How the app gets them', figure(d_flow(),
        'the app uses its <b>managed identity</b> to sign in — it never holds a password. It reads <b>settings</b> from App Configuration and <b>secrets</b> from Key Vault. An App Configuration entry can be a <em>Key Vault reference</em>: it holds only a pointer, and the real secret stays in the vault. '
        'Each read needs a role, such as <em>Key Vault Secrets User</em> for secrets and <em>App Configuration Data Reader</em> for settings — least privilege from concept 3, applied to data.'), label_cls='see')
    body += block('📊 Side by side', table(['','Holds','Changes how?','Watch out for'], [
      ['🪪 Managed identity','Nothing — it is an identity','—','The target must accept Entra ID sign-in'],
      ['🔑 Key Vault','Secrets, keys, certificates','Rotate; read the latest version','Turn on soft delete and purge protection; use RBAC roles'],
      ['⚙️ App Configuration','Settings and feature flags','Update live; apps poll or get push notices','Do not store raw secrets here'],
      ['📄 Config file / pipeline variable','Whatever you put in it','Redeploy','The classic leak'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🗄️','App talks to Azure SQL','The database supports Entra ID sign-in.','Managed identity, no password'),
      ('💳','A payment provider API key','Only a key is accepted. It must stay hidden.','Key Vault + managed identity'),
      ('🚩','Turn on the new checkout for 10% of users','Without a new deployment.','App Configuration feature flag'),
      ('🔄','A storage key that must rotate','The app must not break when it changes.','Read the latest version from Key Vault'),
      ('🧑‍💻','A developer commits a key by mistake','It is now in Git history.','Rotate it, then move it to Key Vault'),
      ('🌍','Same app in dev, test and prod','Different settings per environment.','App Configuration, one store per environment'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — rotation, recovery and access models', '''      <p><b>Rotation.</b> Secrets in memory or config files stay exposed for the whole life of the app, so rotate them regularly. For zero downtime, use two credentials and switch between them; Key Vault stores each new value as a new <i>version</i>. Apps should read the <b>latest</b> version and refresh any cached value when a secret rotates.</p>
      <p><b>Protect the vault itself.</b> <i>Soft delete</i> keeps deleted vaults and items recoverable for a retention period. <i>Purge protection</i> blocks permanent deletion until that period ends, and once on it cannot be switched off by anyone.</p>
      <p><b>Access.</b> Use Azure RBAC for the data plane (built-in roles such as Key Vault Secrets User). Older vaults may still use access policies. Two permission questions exist: who can manage the vault, and who can read its contents.</p>
      <p><b>Storage keys.</b> Microsoft prefers Entra ID with a managed identity over shared account keys, and where rules allow you can switch shared-key access off, which removes key rotation altogether.</p>
      <p><b>App Configuration tip.</b> Watch one "sentinel" key and refresh everything only when it changes, instead of polling every key.</p>''')
    body += recall([
      'Best to worst: no secret (managed identity) → Key Vault → config file → in the code.',
      'Key Vault = secrets, keys, certificates, with access control, audit, soft delete, purge protection. App Configuration = settings and feature flags, changeable without redeploy.',
      'App Configuration can hold a Key Vault reference — a pointer, not the secret.',
      'Read the latest secret version and refresh caches on rotation; use two credentials for zero-downtime rotation.',
      'Use RBAC roles (for example Key Vault Secrets User, App Configuration Data Reader) — least privilege.'])
    body += saythis('"I avoid secrets where I can: managed identity for anything that accepts Entra ID. Where a secret is unavoidable it lives in Key Vault, with RBAC, soft delete and purge protection, and the app reads the latest version so rotation does not break it. '
      'Plain settings and feature flags go to App Configuration so I can change them without redeploying, and it can reference Key Vault secrets instead of storing them. Nothing sensitive goes in code or pipeline variables."')
    body += trap([
      '<b>Putting the secret in the pipeline variable "just for now".</b> Variables are copied into logs, forks and screenshots. Use OIDC for the pipeline and managed identity or Key Vault for the app.',
      'Second trap: <b>using Key Vault but never rotating.</b> A vault protects where a secret lives, not how long it lives. Without rotation, one leaked secret works forever.'])
    body += confuse('🔑 Key Vault', 'Holds things that must stay hidden — secrets, keys, certificates — with strict access control and audit.', '⚙️ App Configuration', 'Holds settings and feature flags that change — easy to update live, not meant for raw secrets.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># create a vault, then let the app's managed identity read secrets (RBAC)</span>
az keyvault create --name kv-shop-prod --resource-group rg-shop-prod --enable-rbac-authorization true
az role assignment create --assignee &lt;app-identity-id&gt; \\
    --role "Key Vault Secrets User" --scope &lt;vault-resource-id&gt;''',
      'Illustrative shape only — vault names are globally unique, real setups also enable purge protection and network rules, and flags change.'))
    body += next_box('Secrets are one slice of security. An architect also needs guardrails that apply to every resource, layers that protect each other, and a way to see threats. Next: Security &amp; Governance.', 'security-governance.html', 'Security &amp; Governance')
    body += fact_note(FOOT, [DOCS_KV, DOCS_KVR, DOCS_AC, DOCS_SEC, DOCS_ROT, DOCS_REF])
    return page('secrets-configuration', 'Secrets & Configuration', 'Concept 15 of 19 · 🛠️ Shipping and operating',
        'Keep secrets out of code: <span class="grad-text">ask for them at run time from a guarded place — or avoid having a secret at all.</span>',
        'Managed identity, Key Vault and App Configuration: where each kind of value belongs, how the app reads them, and how rotation works.',
        'Where do you keep secrets and configuration for an Azure app, and why?',
        body, CR + ['<span class="cur">Secrets &amp; Configuration</span>'], '', search_title='Secrets & Configuration')
