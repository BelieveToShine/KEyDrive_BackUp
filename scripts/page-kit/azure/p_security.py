from kit import *
from p_storage import CR

DOCS_POL = ('Azure Policy overview', 'https://learn.microsoft.com/en-us/azure/governance/policy/overview')
DOCS_EFF = ('Azure Policy effects', 'https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-basics')
DOCS_REM = ('Remediate non-compliant resources', 'https://learn.microsoft.com/en-us/azure/governance/policy/how-to/remediate-resources')
DOCS_DFC = ('Microsoft Defender for Cloud overview', 'https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction')
DOCS_WAF = ('Azure Web Application Firewall', 'https://learn.microsoft.com/en-us/azure/web-application-firewall/overview')
DOCS_ZT = ('Zero Trust security in Azure', 'https://learn.microsoft.com/en-us/azure/security/fundamentals/zero-trust')
FOOT = 'Security products and plans change often. This page teaches the ideas; for current plans, rule sets and prices, check the official docs.'

def d_layers():
    d = Diagram('sg1', 640, 372, 'Defense in depth: identity, network, compute and data layers, each guarded by its own Azure tools')
    d.text(130, 22, 'LAYER', size=9.5, mono=True)
    d.text(510, 22, 'GUARDED BY', size=9.5, mono=True)
    rows = [
      ('🪪 Identity','who is asking','Entra ID, MFA, RBAC','Conditional Access, least privilege','violet'),
      ('🕸️ Network','what can reach what','NSGs, Private Endpoints','WAF at the edge and DDoS Protection','cyan'),
      ('🖥️ Compute and apps','what is running','Defender for Cloud','threat detection on servers, containers','amber'),
      ('🗄️ Data','what is worth stealing','Encryption, Key Vault','backups, access only by identity','emerald'),
    ]
    for i,(a,b,c,e,col) in enumerate(rows):
        y = 40 + i*86
        d.box(20, y, 220, 62, [(a,'t'),(b,'s')], 'n')
        d.box(400, y, 220, 62, [(c,'t'),(e,'s')], col)
        d.arrow([(240,y+31),(400,y+31)], col, label='guarded by', at=(320,y+31))
    return d

def d_effects():
    d = Diagram('sg2', 640, 330, 'Azure Policy checks each request against a rule and then denies, audits, modifies or deploys what is missing')
    d.box(10, 128, 110, 60, [('🧑‍💻 Request','t'),('create or change','s')], 'n')
    d.box(230, 128, 110, 60, [('📜 Azure Policy','t'),('your rules','s')], 'amber')
    outs = [
      ('⛔ Deny','stops the request','rose'),
      ('📋 Audit','logs it, allows it','amber'),
      ('✏️ Modify','fixes it on the way in','cyan'),
      ('DeployIfNotExists','adds what is missing','emerald'),
    ]
    d.arrow([(120,158),(230,158)], 'amber', label='evaluated', at=(175,158))
    labels = ['blocks','logs','changes','deploys']
    for i,((t,s_,c),lab) in enumerate(zip(outs,labels)):
        y = 20 + i*75
        d.box(490, y, 140, 52, [(t,'t'),(s_,'s')], c)
        d.arrow([(340,158),(400,158),(400,y+26),(490,y+26)], c, label=lab, at=(445,y+26))
    return d

def d_scope():
    d = Diagram('sg3', 640, 300, 'A policy assigned at a management group is inherited by the subscriptions and resource groups below it')
    d.box(210, 10, 220, 56, [('🏛️ Management group','t'),('policy assigned here','s')], 'amber')
    d.box(40, 120, 200, 52, [('📦 Subscription A','t')], 'n')
    d.box(400, 120, 200, 52, [('📦 Subscription B','t')], 'n')
    d.box(40, 226, 200, 52, [('🗂️ Resource groups','t'),('and their resources','s')], 'n')
    d.box(400, 226, 200, 52, [('🗂️ Resource groups','t'),('and their resources','s')], 'n')
    d.arrow([(270,66),(270,93),(140,93),(140,120)], 'amber', label='inherited', at=(205,93))
    d.arrow([(370,66),(370,93),(500,93),(500,120)], 'amber', label='inherited', at=(435,93))
    d.arrow([(140,172),(140,226)], 'amber', label='inherited', at=(200,199))
    d.arrow([(500,172),(500,226)], 'amber', label='inherited', at=(560,199))
    return d

def build_security_governance():
    body = ''
    body += see(figure(d_layers(),
        'security is built in <b>layers</b>, so that breaking one does not open everything. <b>Identity</b> is the first line: who is asking, and what may they do. The <b>network</b> limits what can reach what. <b>Compute and apps</b> are watched for threats. <b>Data</b> is encrypted and reachable only by identity. '
        'Each layer has its own Azure tools — and you already met some of them in earlier concepts.'))
    body += one('Security is layers, not a wall; governance is guardrails that apply to every resource, so the rules hold even when nobody is watching.')
    body += why([
      'Secrets were one slice. But look at the whole system now: dozens of resources, many people deploying, pipelines creating things at night. <b>What stops someone creating a storage account open to the internet?</b> What shows you that a server is under attack? What protects the web app from common web attacks?',
      'The answer is not one product. Microsoft\'s <b>Zero Trust</b> model says: <i>verify explicitly</i> (check identity, device and location every time), <i>use least privilege</i> (just enough access, just in time), and <i>assume breach</i> (limit the damage with segmentation, encryption and monitoring). Azure gives you tools for each — and <b>governance</b>, so the guardrails apply to everything, consistently.'])
    body += block('🧰 The tools', pick_cards([
      dict(icon='📜', name='Azure Policy', tag='guardrails for every resource', color='#fbbf24',
           use=['Stop or flag resources that break your rules', 'Apply rules across a whole management group or subscription', 'Prove compliance with a report'],
           skip=['Deciding who may do things — that is RBAC (concept 3)']),
      dict(icon='🛡️', name='Defender for Cloud', tag='see your posture, detect threats', color='#22d3ee',
           use=['A secure score and recommendations across subscriptions', 'Threat protection plans for servers, containers, storage, databases', 'A free foundational posture tier, with a paid tier for more'],
           skip=['You expect it to fix everything by itself — recommendations still need action']),
      dict(icon='🧱', name='Web Application Firewall', tag='block common web attacks', color='#34d399',
           use=['Public web apps and APIs', 'On Application Gateway (regional) or Front Door (edge)', 'Rules based on OWASP, custom rules, rate limiting'],
           skip=['Volumetric network floods — pair it with DDoS Protection']),
      dict(icon='🔒', name='Private access', tag='keep services off the internet', color='#a78bfa',
           use=['Databases, storage and vaults that only your apps need', 'Private Endpoints and NSGs from concept 4', 'Shrink what can be attacked'],
           skip=['Treating the network as the only defense — identity is still the first line']),
    ]), label_cls='see')
    body += block('📜 How Azure Policy acts', figure(d_effects(),
        'every create or update is checked against the policy. The <b>effect</b> decides what happens. <b>Deny</b> stops the request. <b>Audit</b> allows it but records it as non-compliant. <b>Modify</b> changes the resource as it is created or updated (for example, adding a tag). <b>DeployIfNotExists</b> deploys something that is missing (for example, a diagnostic setting). '
        'Microsoft advises starting with <b>audit</b> to see the impact before you enforce with deny or the others.'), label_cls='see')
    body += block('🏛️ Where a policy applies', figure(d_scope(),
        'a policy is assigned at a <b>scope</b> — a management group, subscription or resource group — and everything below that scope inherits it (this is the hierarchy from concept 1 doing real work). '
        'Assign the important guardrails high, at the management group, so no new subscription can start without them. Policies with Modify or DeployIfNotExists change <em>new</em> resources; to fix existing ones, you run a <b>remediation task</b>.'), label_cls='see')
    body += block('📊 Policy vs RBAC', table(['','Question it answers','Example','Applies to'], [
      ['🪪 RBAC','Who may do what?','"The deploy team may create web apps"','People and identities'],
      ['📜 Policy','What is allowed to exist?','"Storage accounts must not allow public access"','Resources, whoever creates them'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🚫','Nobody should create resources outside two regions','The rule must hold for every team.','Azure Policy: deny'),
      ('🏷️','Every resource must carry a cost-center tag','Fix it automatically when missing.','Policy: modify'),
      ('📈','"How safe are we?" from the board','One number, plus a to-do list.','Defender for Cloud secure score'),
      ('🌐','Public API is being probed','Block SQL injection and similar patterns.','WAF on Application Gateway or Front Door'),
      ('🗄️','The database must not be reachable from the internet','Only the app subnet may connect.','Private Endpoint + NSG'),
      ('🔥','A flood of junk traffic','Not a single bad request — just volume.','DDoS Protection together with the WAF'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — rolling out guardrails safely', '''      <p><b>Roll out in stages.</b> A deny rule applied everywhere on day one can break deployments. Start with <b>audit</b>, read the compliance report, fix the real problems, then switch to deny. Microsoft recommends exactly this order.</p>
      <p><b>Evaluation order.</b> Deny is evaluated before audit, so an undesired resource is not logged twice.</p>
      <p><b>Remediation needs identity.</b> Modify and DeployIfNotExists run with a managed identity, which must have the minimum role it needs to make the change. With an initiative (a group of policies), remediation tasks are created per policy.</p>
      <p><b>The WAF and DDoS split.</b> A WAF understands web requests (layer 7) but is not built for volumetric network floods. Microsoft recommends using DDoS Protection and a WAF together for web workloads. On Front Door, only the Premium tier offers managed rule sets; Standard supports custom rules.</p>
      <p><b>Posture vs protection.</b> Defender for Cloud has two jobs: <i>posture management</i> (find weak settings, give a score) and <i>workload protection</i> (detect attacks on servers, containers, databases). Resource locks can also protect critical resources from accidental deletion.</p>''')
    body += recall([
      'Zero Trust: verify explicitly, least privilege, assume breach. Security is layers: identity, network, compute/apps, data.',
      'RBAC = who may do what; Azure Policy = what is allowed to exist. Policy effects: deny, audit, modify, deployIfNotExists.',
      'Start a new policy with audit, then enforce. Policy is inherited down the hierarchy; assign guardrails at the management group.',
      'Defender for Cloud = posture (secure score, recommendations) plus workload protection plans.',
      'WAF blocks web-layer attacks (OWASP-based rules); DDoS Protection handles volumetric floods — use both for web workloads.'])
    body += saythis('"I think of security as layers — identity first, then network, compute and data — guided by Zero Trust: verify explicitly, least privilege, assume breach. '
      'For governance I use Azure Policy at the management group: audit first, then deny, with modify and deployIfNotExists to fix gaps and a remediation task for existing resources. Defender for Cloud gives posture and threat detection, and a WAF with DDoS Protection guards public web apps."')
    body += trap([
      '<b>Assigning a deny policy everywhere on day one.</b> It can block legitimate deployments and halt teams. Audit first, fix, then enforce.',
      'Second trap: <b>trusting the network as the only defense.</b> A private network does not help if a stolen identity can reach everything. Identity is the first line of defense; the network supports it.'])
    body += confuse('🪪 RBAC', 'Controls who can perform actions. Attached to people and identities.', '📜 Azure Policy', 'Controls what resources may look like. Applies to the resource, no matter who creates it.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># assign a built-in policy at a management group, in audit mode first</span>
az policy assignment create --name audit-allowed-locations \\
    --policy &lt;built-in-policy-id&gt; --scope /providers/Microsoft.Management/managementGroups/&lt;mg-id&gt; \\
    --params '{ "effect": { "value": "Audit" } }\'''',
      'Illustrative shape only — the policy ID and parameter names depend on the built-in policy you choose, and the flags can change.'))
    body += next_box('Guardrails say what <b>should</b> happen. You still need to see what <b>actually</b> happens — including for the guardrails themselves. Next: Monitoring &amp; Observability.', None)
    body += fact_note(FOOT, [DOCS_POL, DOCS_EFF, DOCS_REM, DOCS_DFC, DOCS_WAF, DOCS_ZT])
    return page('security-governance', 'Security & Governance', 'Concept 16 of 19 · 🛠️ Shipping and operating',
        'Security is layers, not a wall — and governance is <span class="grad-text">guardrails that hold for every resource, even when nobody is watching.</span>',
        'Zero Trust, defense in depth, Azure Policy, Defender for Cloud, WAF and private access: how an architect applies protection consistently across everything.',
        'How would you secure and govern an Azure environment at scale?',
        body, CR + ['<span class="cur">Security &amp; Governance</span>'], '', search_title='Security & Governance')
