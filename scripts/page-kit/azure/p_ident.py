from kit import *
from p_storage import CR

DOCS_RBAC = ('Azure RBAC documentation', 'https://learn.microsoft.com/en-us/azure/role-based-access-control/')
DOCS_ENTRA = ('Microsoft Entra documentation', 'https://learn.microsoft.com/en-us/entra/')
DOCS_MI = ('Managed identities for Azure resources', 'https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official docs.'
CR_ID = CR + ['<a href="identity-access.html">Identity &amp; Access</a>']

def d_assignment():
    d = Diagram('id1', 640, 280, 'A role assignment is who plus what plus where: a security principal, a role definition and a scope; example: Asha has Reader on rg-shop-prod')
    d.text(10, 14, 'ONE ROLE ASSIGNMENT = WHO + WHAT + WHERE', anchor='start', size=9.5, mono=True)
    d.box(10, 26, 150, 104, [('👤 WHO','t'),('security principal','s'),('user · group','s'),('service principal','s'),('managed identity','s')], 'cyan')
    d.box(245, 26, 150, 104, [('🎟️ WHAT','t'),('role definition','s'),('Owner · Contributor','s'),('Reader','s'),('or a custom role','s')], 'violet')
    d.box(480, 26, 150, 104, [('📍 WHERE','t'),('scope','s'),('management group','s'),('subscription','s'),('resource group · resource','s')], 'emerald')
    d.arrow([(160,78),(245,78)], 'cyan', label='gets', at=(202,78))
    d.arrow([(395,78),(480,78)], 'violet', label='at', at=(437,78))
    d.text(10, 160, 'EXAMPLE', anchor='start', size=9.5, mono=True)
    d.box(10, 172, 150, 56, [('👤 Asha','t'),('a user','s')], 'cyan')
    d.box(245, 172, 150, 56, [('Reader','t'),('view, not change','s')], 'violet')
    d.box(480, 172, 150, 56, [('📦 rg-shop-prod','t'),('a resource group','s')], 'emerald')
    d.arrow([(160,200),(245,200)], 'cyan', label='gets', at=(202,200))
    d.arrow([(395,200),(480,200)], 'violet', label='at', at=(437,200))
    d.text(320, 262, '= Asha can view everything in rg-shop-prod — but cannot change it.', size=10, weight=700)
    return d

def d_authn_authz():
    d = Diagram('id2', 640, 332, 'Authentication versus authorization: the user signs in to Microsoft Entra ID and gets a token, then sends it to Azure where RBAC decides what is allowed')
    d.box(10, 40, 130, 56, [('👤 User or app','t'),('wants to act','s')], 'n')
    d.box(270, 40, 190, 56, [('🪪 Microsoft Entra ID','t'),('AUTHENTICATION: who are you?','s')], 'cyan')
    d.box(270, 174, 190, 56, [('🛡️ Azure (RBAC check)','t'),('AUTHORIZATION: what may you do?','s')], 'violet')
    d.box(270, 268, 190, 48, [('📦 Resource','t'),('storage, VM, database…','s')], 'emerald')
    d.arrow([(140,58),(270,58)], 'cyan', label='1 · signs in', at=(205,58))
    d.arrow([(270,80),(140,80)], 'cyan', label='2 · a token', at=(208,80))
    d.arrow([(75,96),(75,202),(270,202)], 'violet', label='3 · sends the token', at=(172,202))
    d.arrow([(365,230),(365,268)], 'emerald', label='only if a role allows it', at=(470,249))
    return d

def d_two_role_systems():
    d = Diagram('id3', 640, 276, 'Microsoft Entra roles manage the directory (users, groups, apps); Azure roles manage Azure resources; they are separate systems')
    d.zone(10, 8, 305, 240, 'cyan', 'ENTRA ROLES · manage the directory')
    d.box(26, 44, 273, 46, [('🛡️ Global Administrator','t'),('the top Entra role','s')], 'cyan')
    d.box(26, 98, 273, 46, [('🎛️ They control','t'),('users · groups · app registrations','s')], 'n')
    d.text(162, 176, 'Scope: the tenant, an administrative unit,', size=9.5)
    d.text(162, 192, 'or a single object.', size=9.5)
    d.zone(325, 8, 305, 240, 'violet', 'AZURE ROLES · manage Azure resources')
    d.box(341, 44, 273, 40, [('👑 Owner','t'),('manage everything and assign roles','s')], 'violet')
    d.box(341, 92, 273, 40, [('✍️ Contributor','t'),('manage everything, but cannot assign roles','s')], 'violet')
    d.box(341, 140, 273, 40, [('👀 Reader','t'),('view only','s')], 'violet')
    d.text(477, 204, 'Scope: management group, subscription,', size=9.5)
    d.text(477, 220, 'resource group, or a single resource.', size=9.5)
    d.text(320, 266, "Separate systems: permissions from one cannot be used in the other's custom roles.", size=9.5, weight=700)
    return d

def build_identity_access():
    body = ''
    body += see(figure(d_assignment(),
        'access in Azure is always a sentence with three parts: <b>who</b> (a user, a group, an app\'s service principal, or a managed identity), <b>what</b> (a role — a bundle of permissions such as Reader or Contributor) and <b>where</b> (a scope: management group, subscription, resource group or one resource). '
        'Put the three together and you have a <b>role assignment</b>. In the example, Asha gets the Reader role on one resource group, so she can look at everything in it but change nothing.'))
    body += one('Identity answers two questions: who are you (Microsoft Entra ID) and what may you do (Azure RBAC). Access is always who + what + where.')
    body += why([
      'Your resources now have a home and a place in the world. The next risk is people — and apps. Who may create a database, who may delete a resource group, and how does your own app get permission to read a file without anyone typing a password?',
      'Azure splits this into two clear steps. <b>Microsoft Entra ID</b> proves <i>who</i> you are (authentication). <b>Azure RBAC</b> decides <i>what you may do</i>, and <i>where</i> (authorization). Keeping the two apart is what lets you give each person and each app exactly the access it needs — no more.'])
    body += block('🔁 Two checks, in order', figure(d_authn_authz(),
        '<b>1–2 · Authentication.</b> The user or app signs in to Microsoft Entra ID, which proves who they are and returns a <b>token</b>. '
        '<b>3 · Authorization.</b> The caller sends the token to Azure. Azure RBAC looks at the role assignments for that identity at that scope, and the request only reaches the resource if a role allows it. Signing in alone gives you nothing — a new identity has no access until someone assigns a role.'), label_cls='see')
    body += block('🧑‍🤝‍🧑 Who can be given a role?', '''    <div class="taxonomy-strip">
      <div class="tax-item"><h5>👤 User</h5><p>A person with an account in your Microsoft Entra tenant.</p></div>
      <div class="tax-item"><h5>👥 Group</h5><p>A set of users. Assign the role to the group once, then add or remove people — easier than assigning to each person.</p></div>
      <div class="tax-item"><h5>🤖 Service principal</h5><p>The identity of an application inside your tenant. Used when an app (or a pipeline) must act on its own.</p></div>
      <div class="tax-item"><h5>🪪 Managed identity</h5><p>A special service principal that Azure manages for an Azure resource — so your code needs no secret. See the deep dive below.</p></div>
    </div>''', label_cls='see')
    body += block('🎟️ The three roles you meet first', table(['Role','What it can do','Typical person'], [
      ['Owner','Full management of resources <b>and</b> can assign roles to others','A small number of trusted admins'],
      ['Contributor','Full management of resources, but <b>cannot</b> assign roles','Developers who build and run the app'],
      ['Reader','View resources, change nothing','Auditors, support, new team members'],
    ]) + '\n    <div class="kd-card" style="margin-top:14px">Permissions <b>add up</b>: if someone has Reader and Contributor on the same scope, the result is Contributor. And a role given at a higher scope is <b>inherited</b> by everything below it (see the resource hierarchy). '
        'Aim for <b>least privilege</b>: the smallest role at the lowest scope that lets the person or app do its job.</div>', label_cls='see')
    body += block('⚠️ Two kinds of roles — do not mix them up', figure(d_two_role_systems(),
        '<b>Microsoft Entra roles</b> (left) manage the <em>directory</em>: users, groups, app registrations. Their top role is Global Administrator. <b>Azure roles</b> (right) manage <em>Azure resources</em>: Owner, Contributor, Reader and many more. '
        'They are separate systems with different scopes. Being a Global Administrator is not the same as being an Owner of a subscription.'), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🧑‍💻','New developer joins','They must deploy the web app but never touch billing or other teams.','Contributor on their resource group'),
      ('🔍','Auditor reviews Prod','Needs to see everything, change nothing.','Reader on the Prod subscription'),
      ('👥','Ten people, same job','Assigning ten roles by hand is slow and error-prone.','One role to a group'),
      ('🤖','Pipeline deploys the app','A script, not a person, needs access.','A service principal (or managed identity) with a role'),
      ('🌐','Web app reads blobs','The code must read files without a password in its settings.','Managed identity + Blob data role'),
      ('🛑','"Everyone is Owner"','It works today, until one mistake deletes everything.','Least privilege: lowest role, lowest scope'),
    ]), label_cls='see')
    body += block('🔬 Go deeper', deep_cards([('Deep dive · Identity & Access', 'Managed identities', 'How an Azure app gets a token with no password in its code, system-assigned vs user-assigned, and the three steps to set one up.', 'managed-identities.html')]), label_cls='next')
    body += recall([
      'Authentication = who are you (Microsoft Entra ID → a token). Authorization = what may you do (Azure RBAC).',
      'A role assignment = security principal (who) + role definition (what) + scope (where). Scopes: management group, subscription, resource group, resource.',
      'Owner can assign roles; Contributor manages resources but cannot assign roles; Reader only views. Permissions add up and are inherited downward.',
      'Microsoft Entra roles (the directory) and Azure roles (resources) are separate systems.',
      'Prefer groups and managed identities; give least privilege at the lowest useful scope.'])
    body += saythis('"In Azure, Microsoft Entra ID handles authentication — proving who a user or workload is and issuing a token — and Azure RBAC handles authorization. A role assignment combines a security principal, a role definition and a scope, and it is inherited down the hierarchy. '
      'I assign roles to groups, use managed identities for apps so there are no secrets, and follow least privilege at the narrowest scope that works."')
    body += trap([
      '<b>Signing in is not the same as having access.</b> A user who can sign in to the tenant, or a brand-new managed identity, can do nothing in Azure until a role is assigned. "I can log in but get an authorization error" almost always means a missing role at the right scope.',
      'Second trap: <b>Owner is powerful because it can hand out access</b>. Giving Owner to "make things work" lets that person (or app) grant anyone anything. Reach for Contributor, or a narrower role, first.'])
    body += confuse('🪪 Authentication', 'Proves who you are. Done by Microsoft Entra ID. Result: a token.', '🛡️ Authorization', 'Decides what that identity may do, and where. Done by Azure RBAC role assignments.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># give a user the Reader role on one resource group (who + what + where)</span>
az role assignment create \\
    --assignee <span class="str">"asha@contoso.com"</span> \\
    --role <span class="str">"Reader"</span> \\
    --scope <span class="str">"/subscriptions/&lt;subscription-id&gt;/resourceGroups/rg-shop-prod"</span>''',
      'Illustrative shape only — replace the placeholders; in real teams roles are usually assigned to groups, and defined in templates.'))
    body += next_box('People and apps now have identities and roles. Next: the <b>network</b> — how resources talk to each other and to the outside world, and who is allowed through the door.', 'virtual-networks.html', 'Virtual Networks')
    body += fact_note(FOOT, [DOCS_RBAC, DOCS_ENTRA, DOCS_MI])
    return page('identity-access', 'Identity & Access', 'Concept 3 of 19 · 🏗️ Foundations',
        'Identity answers two questions: <span class="grad-text">who are you, and what may you do?</span>',
        'Microsoft Entra ID proves who a person or an app is. Azure RBAC decides what they may do — and where. Learn the role-assignment sentence, the first three roles, and how to keep access small and safe.',
        'What is the difference between authentication and authorization in Azure, and how does Azure RBAC work?',
        body, CR + ['<span class="cur">Identity &amp; Access</span>'], '', search_title='Identity & Access')


def d_secret_vs_identity():
    d = Diagram('mi1', 640, 300, 'An app using a stored secret versus an app using a managed identity to get a token')
    d.zone(10, 8, 305, 284, 'rose', 'WITHOUT · a secret stored with the app')
    d.box(40, 56, 150, 74, [('💻 App','t'),('holds a password','s'),('in its settings or code','s')], 'rose')
    d.box(40, 190, 245, 50, [('🗂️ Storage account','t'),('accepts the password','s')], 'n')
    d.arrow([(115,130),(115,190)], 'rose', label='sends the secret', at=(215,160))
    d.text(162, 266, '⚠️ Secrets can leak — and must be rotated.', size=9.5, weight=700)
    d.zone(325, 8, 305, 284, 'emerald', 'WITH · a managed identity')
    d.box(345, 56, 90, 74, [('💻 App','t'),('no secret','s'),('inside','s')], 'emerald')
    d.box(515, 56, 100, 74, [('🪪 Azure','t'),('identity','t'),('endpoint','s')], 'cyan')
    d.arrow([(435,76),(515,76)], 'cyan', label='asks', at=(475,76))
    d.arrow([(515,110),(435,110)], 'cyan', label='token', at=(475,110))
    d.box(345, 190, 270, 50, [('🗂️ Storage account','t'),("checks the identity's RBAC role",'s')], 'n')
    d.arrow([(390,130),(390,190)], 'emerald', label='calls with the token', at=(500,160))
    d.text(477, 266, '✅ Nothing secret to leak or rotate.', size=9.5, weight=700)
    return d

def d_types():
    d = Diagram('mi2', 640, 256, 'A system-assigned identity belongs to one resource and is deleted with it; a user-assigned identity is a separate resource that several resources can share')
    d.zone(10, 8, 305, 240, 'amber', 'SYSTEM-ASSIGNED · one identity per resource')
    d.box(60, 48, 200, 56, [('💻 App A','t'),('one Azure resource','s')], 'n')
    d.box(60, 152, 200, 56, [('🪪 its own identity','t'),('created with the app','s')], 'amber')
    d.arrow([(160,152),(160,104)], 'amber', label='is tied to', at=(238,128))
    d.text(162, 232, 'Delete the app → the identity is deleted too. Not shareable.', size=9.5, weight=700)
    d.zone(325, 8, 305, 240, 'cyan', 'USER-ASSIGNED · a separate, shareable identity')
    d.box(380, 44, 200, 56, [('🪪 Identity','t'),('its own resource','s')], 'cyan')
    d.box(345, 152, 120, 56, [('💻 App A','t')], 'n')
    d.box(490, 152, 120, 56, [('💻 App B','t')], 'n')
    d.arrow([(405,152),(405,100)], 'cyan', label='uses', at=(405,126))
    d.arrow([(550,152),(550,100)], 'cyan', label='uses', at=(550,126))
    d.text(477, 232, 'Many resources share it. You delete it yourself.', size=9.5, weight=700)
    return d

def build_managed_identities():
    body = ''
    body += see(figure(d_secret_vs_identity(),
        '<b>Left:</b> the app carries a password. Whoever finds it — in a config file, a log, a code repository — can use it, and someone must remember to change it. '
        '<b>Right:</b> the app has a <b>managed identity</b>. It asks an Azure identity endpoint for a short-lived token, then calls the storage account with that token. The storage account checks the identity\'s role. There is no secret in the app at all.'))
    body += one('A managed identity lets an Azure resource prove who it is without a password: Azure creates the identity, hands your code a token, and you control access with ordinary roles.')
    body += why([
      'On the Identity page, apps could be given roles through a <b>service principal</b>. But a service principal that signs in with a secret has the same old problem: a password that must be stored somewhere, kept safe and replaced before it expires. '
      'Passwords in config files are one of the most common ways cloud accounts get broken into.',
      'A <b>managed identity</b> removes the secret from the picture. It is a special service principal that Azure creates and looks after for you, and it can only be used by Azure resources. '
      'Your code asks for a token, Azure provides it, and the identity can do only what the roles you assigned allow.'])
    body += block('🔀 System-assigned or user-assigned?', figure(d_types(),
        '<b>System-assigned</b> (left) is switched on for one resource, and it is tied to that resource: when the resource is deleted, so is the identity. It cannot be shared. '
        '<b>User-assigned</b> (right) is its own Azure resource. You create it first, attach it to as many resources as you like, and it stays until you delete it.'), label_cls='see')
    body += block('🧭 Which one should I pick?', pick_cards([
      dict(icon='🔒', name='System-assigned', tag='the simple one-to-one choice', color='#fbbf24',
           use=['One app needs its own access and nothing else uses it', 'You want the identity cleaned up automatically with the resource', 'The quickest way to start'],
           skip=['Several apps need exactly the same access → user-assigned', 'The resource is often deleted and re-created and you want to keep the role assignments → user-assigned']),
      dict(icon='🤝', name='User-assigned', tag='one identity, many resources', color='#22d3ee',
           use=['A group of resources should share the same permissions', 'You want to create the identity and its roles <i>before</i> the resource exists', 'The identity must outlive any single resource'],
           skip=['A single resource that needs a private identity → system-assigned is simpler', 'You do not want to remember to delete a leftover identity']),
    ]), label_cls='see')
    steps = """    <div class="taxonomy-strip">
      <div class="tax-item"><h5>1 · Turn it on</h5><p>Enable the identity on the app (or create a user-assigned one and attach it).</p></div>
      <div class="tax-item"><h5>2 · Give it a role</h5><p>Assign an RBAC role to the identity, on the resource it needs — for example a Blob data role on the storage account. A new identity has <b>no access</b> by default.</p></div>
      <div class="tax-item"><h5>3 · Let the library do the rest</h5><p>In code, use the Azure Identity library. It asks for the token for you. For a user-assigned identity you also pass its client id.</p></div>
    </div>"""
    body += block('🪜 Three steps to use one', steps, label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🌐','Web app reads blobs','The site shows files from Blob Storage and must not hold a password.','System-assigned + a Blob data role'),
      ('⚙️','Three apps, same access','A web app, an API and a worker all read the same storage account.','One user-assigned identity'),
      ('🔑','App reads secrets','The code needs a secret from a vault, and the vault should not need a secret to open.','Managed identity + vault access'),
      ('🖥️','A VM calls Azure','A VM must list resources through Azure Resource Manager.','Managed identity with a role on that scope'),
      ('🧰','Re-created every deploy','The app is rebuilt on each release but access must stay the same.','User-assigned (it survives)'),
      ('🚫','Code on a laptop','A developer running locally has no managed identity.','Sign in with their own Entra account'),
    ]), label_cls='see')
    body += recall([
      'A managed identity is a service principal that Azure manages for an Azure resource — no credentials in your code.',
      'System-assigned: tied to one resource, deleted with it, not shareable. User-assigned: a separate resource, shareable, deleted by you.',
      'It has no access until you assign RBAC roles. Code asks for a token (Azure Identity library); user-assigned needs the client id.',
      'Use it for Azure-to-Azure calls; local development uses your own account.'])
    body += saythis('"A managed identity gives an Azure resource an identity in Microsoft Entra ID without any secret to manage — Azure issues tokens to the code on request. '
      'System-assigned identities share the resource\'s lifecycle and cannot be shared; user-assigned identities are standalone resources that several resources can use. Either way, the identity starts with no access and I grant it least-privilege RBAC roles."')
    body += trap([
      '<b>"Forbidden" right after enabling it is normal.</b> Turning on a managed identity creates the identity, not its permissions. Until you assign a role at the right scope, every call fails with an authorization error.',
      'Second trap: <b>a managed identity only exists for Azure resources.</b> Your laptop and an on-premises server do not have one — code that works in Azure may need a different sign-in locally.'])
    body += confuse('🪪 Managed identity', 'Azure creates and looks after it. No secret to store or rotate. Only usable by Azure resources.', '🤖 Service principal with a secret', 'You create it and keep its password or certificate safe, and renew it before it expires. Works anywhere, but carries a secret.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="kw">from</span> azure.identity <span class="kw">import</span> DefaultAzureCredential
<span class="kw">from</span> azure.storage.blob <span class="kw">import</span> BlobServiceClient

<span class="cmt"># system-assigned identity: nothing extra to pass</span>
credential = DefaultAzureCredential()

<span class="cmt"># user-assigned identity: say which one by its client id</span>
<span class="cmt"># credential = DefaultAzureCredential(managed_identity_client_id="&lt;client-id&gt;")</span>

service = BlobServiceClient(<span class="str">"https://myaccount.blob.core.windows.net"</span>, credential=credential)''',
      'Illustrative shape only — the identity still needs a role such as Storage Blob Data Reader on the account.'))
    body += next_box('That is how an app gets access without a password. Back to the Identity page for the full picture of roles and scopes — and on to the network.', 'identity-access.html', 'Back to Identity &amp; Access')
    body += fact_note(FOOT, [DOCS_MI, DOCS_RBAC, DOCS_ENTRA])
    return page('managed-identities', 'Managed Identities', 'Deep dive · Identity & Access · 🪪 Managed identities',
        'A managed identity lets an app prove who it is — <span class="grad-text">with no password in your code.</span>',
        'Passwords in config files are a classic way for cloud accounts to be broken into. Learn how Azure gives your app its own identity, the difference between system-assigned and user-assigned, and the three steps to use one.',
        'What is a managed identity, and when do you use system-assigned versus user-assigned?',
        body, CR_ID + ['<span class="cur">Managed identities</span>'], '', search_title='Managed Identities')
