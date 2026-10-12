from kit import *
from p_common import CR

DOCS_SRA = ('AWS Security Reference Architecture', 'https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html')
DOCS_SEC = ('Apply security services across your AWS organization', 'https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/security-services.html')
DOCS_SCP = ('Service control policies', 'https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html')
DOCS_SH = ('AWS Security Hub documentation', 'https://docs.aws.amazon.com/securityhub/')
DOCS_GD = ('Amazon GuardDuty documentation', 'https://docs.aws.amazon.com/guardduty/')
DOCS_CFG = ('AWS Config documentation', 'https://docs.aws.amazon.com/config/')
DOCS_PER = ('Perimeter security (AWS SRA)', 'https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/perimeter-security.html')
FOOT = 'Security products and plans change often. This page teaches the ideas; for current services, rule sets and prices, check the official AWS docs.'

def d_layers():
    d = Diagram('sg1', 640, 372, 'Defense in depth on AWS: guardrails across the organization, identity, network and edge, detection, and data protection')
    d.text(130, 22, 'LAYER', size=9.5, mono=True)
    d.text(510, 22, 'GUARDED BY', size=9.5, mono=True)
    rows = [
      ('🏛️ Organization','guardrails on every account','SCPs in Organizations','limit what accounts may do','amber'),
      ('🪪 Identity','who is asking','IAM, Identity Center','roles, MFA, least privilege','violet'),
      ('🕸️ Network and edge','what can reach what','Security groups, WAF','Shield for DDoS, endpoints','cyan'),
      ('🔎 Detection','what is actually happening','GuardDuty, Config','Security Hub gathers findings','rose'),
    ]
    for i,(a,b,c,e,col) in enumerate(rows):
        y = 40 + i*86
        d.box(20, y, 220, 62, [(a,'t'),(b,'s')], 'n')
        d.box(400, y, 220, 62, [(c,'t'),(e,'s')], col)
        d.arrow([(240,y+31),(400,y+31)], col, label='guarded by', at=(320,y+31))
    return d

def d_scp():
    d = Diagram('sg2', 640, 300, 'An action is allowed only when the service control policy allows it and an IAM policy allows it; the SCP only filters and never grants')
    d.box(10, 40, 160, 64, [('🛡️ SCP','t'),('what the account may use','s')], 'amber')
    d.box(10, 180, 160, 64, [('🪪 IAM policy','t'),('what this role may do','s')], 'violet')
    d.box(260, 100, 130, 70, [('⚖️ Both must','t'),('allow it','t')], 'n')
    d.box(500, 100, 130, 70, [('✅ Allowed','t'),('the overlap','s')], 'emerald')
    d.arrow([(170,72),(215,72),(215,125),(260,125)], 'amber', label='filters', at=(215,98))
    d.arrow([(170,212),(215,212),(215,150),(260,150)], 'violet', label='grants', at=(215,184))
    d.arrow([(390,135),(500,135)], 'emerald', label='only then', at=(445,135))
    d.text(320, 280, 'An SCP never grants permissions; it limits what permissions can be used.', size=9.5, weight=700)
    return d

def d_detect():
    d = Diagram('sg3', 640, 296, 'GuardDuty and Config send findings to Security Hub, which gathers them in one place for people and automation to act on')
    d.box(10, 40, 150, 56, [('🕵️ GuardDuty','t'),('threat detection','s')], 'rose')
    d.box(10, 120, 150, 56, [('📋 Config','t'),('settings vs rules','s')], 'cyan')
    d.box(10, 200, 150, 56, [('🔍 Other tools','t'),('more findings','s')], 'n')
    d.box(290, 100, 150, 76, [('🧭 Security Hub','t'),('one view of findings','s')], 'amber')
    d.box(520, 100, 110, 76, [('⚡ Response','t'),('people or code','s')], 'emerald')
    d.arrow([(160,68),(225,68),(225,125),(290,125)], 'rose', label='findings', at=(225,96))
    d.arrow([(160,148),(290,148)], 'cyan', label='findings', at=(225,148))
    d.arrow([(160,228),(225,228),(225,170),(290,170)], 'n', label='findings', at=(225,200))
    d.arrow([(440,138),(520,138)], 'emerald', label='acts', at=(480,138))
    return d

def build_security_governance():
    body = ''
    body += see(figure(d_layers(),
        'security is built in <b>layers</b>, so breaking one does not open everything. <b>Guardrails</b> across the whole organization limit what any account may do. <b>Identity</b> says who is asking. The <b>network and edge</b> limit what can reach what. <b>Detection</b> shows what is actually happening. '
        'Each layer has its own AWS tools — and you already met several in earlier concepts.'))
    body += one('Security is layers, not a wall; governance is guardrails that hold for every account, even when nobody is watching.')
    body += why([
      'Secrets were one slice. But look at the whole system now: many accounts, many people deploying, pipelines creating things at night. <b>What stops someone creating a bucket open to the world?</b> What shows you that a server is under attack? What protects the web app from common web attacks?',
      'The answer is not one product. AWS describes <b>layers</b>: preventive guardrails across the organization, centralized detection, and protection at the edge. Security services are administered from a separate security account, not from the management account that holds the bill.'])
    body += block('🧰 The tools', pick_cards([
      dict(icon='🛡️', name='Service control policies', tag='guardrails for whole accounts', color='#fbbf24',
           use=['Limit what accounts may do across an organization, OU or account', 'Block regions or services you never use', 'Work as deny lists in the default Organizations setup'],
           skip=['Granting permission — an SCP never grants; IAM does']),
      dict(icon='🧭', name='AWS Security Hub', tag='one place for findings and checks', color='#22d3ee',
           use=['Collect findings from several security services', 'Check accounts against standards such as the Foundational Security Best Practices'],
           skip=['Expecting it to fix things — findings still need action']),
      dict(icon='🕵️', name='Amazon GuardDuty and AWS Config', tag='detect threats; track configuration', color='#fb7185',
           use=['GuardDuty findings flow into Security Hub', 'Config tracks resource settings against rules; start in monitoring mode, then enforce once trusted', 'Config is a prerequisite for Security Hub CSPM'],
           skip=['Switching on enforcement before you have seen the findings']),
      dict(icon='🧱', name='AWS WAF, Shield and Firewall Manager', tag='protect the edge', color='#34d399',
           use=['WAF: managed rules for common web attacks; keep them in default mode so they update', 'Shield Advanced for load balancers, Elastic IPs and CloudFront', 'Firewall Manager applies WAF, Shield and security group rules across accounts'],
           skip=['Treating the network as the only defense — identity is still the first line']),
    ]), label_cls='see')
    body += block('⚖️ Guardrails and permissions together', figure(d_scp(),
        'a request is allowed only in the <b>overlap</b>: the service control policy must allow it <em>and</em> an IAM policy must grant it. The SCP is a filter on what the account may use; it never gives anyone access. '
        'This is why guardrails and IAM do different jobs — the SCP sets the outer limit for everyone, IAM gives each identity its own slice inside it.'), label_cls='see')
    body += block('🔎 Gathering what detection finds', figure(d_detect(),
        'detection services send <b>findings</b> to <b>Security Hub</b>, which collects them in one view. GuardDuty findings flow in automatically, and AWS Config is the prerequisite for the posture checks. '
        'You can then drive <b>automated response</b> from findings — for example, blocking a suspicious address at the edge while people investigate. Delegated administration keeps these tools in a separate security account.'), label_cls='see')
    body += block('📊 Prevent, detect, respond', table(['','Question it answers','Examples','Acts when?'], [
      ['🛡️ Prevent','What is not allowed at all?','SCPs, IAM, security groups, WAF rules','Before the action'],
      ['🔎 Detect','What is happening or wrong?','GuardDuty, Config, Security Hub','After or as it happens'],
      ['⚡ Respond','What do we do about it?','Automation driven by findings','On a finding'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🚫','Nobody should use a Region the company does not operate in','The rule must hold in every account.','An SCP on the OU'),
      ('📈','"How safe are we?" from the board','One list of findings and checks.','Security Hub'),
      ('🕵️','A server starts talking to a known bad address','You need to know now.','GuardDuty findings'),
      ('🧾','A bucket was made public by mistake','Catch configuration drift.','AWS Config rules'),
      ('🌐','A public API is probed for common attacks','Block before it reaches the app.','AWS WAF managed rules'),
      ('🏢','Many accounts, one set of web rules','Apply once, everywhere.','Firewall Manager'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — rolling out guardrails safely', '''      <p><b>Start in monitoring mode.</b> AWS Config rules can run in a monitoring mode and later move to enforcement once their behaviour is trusted. The same idea applies to any new guardrail: watch, fix real problems, then enforce.</p>
      <p><b>Use a security account.</b> AWS\'s reference architecture recommends delegating administration of security services to a Security Tooling account, which separates security work from the management account that pays the bills.</p>
      <p><b>Management account.</b> Service control policies do not apply to the management account, so keep workloads out of it (concept 1).</p>
      <p><b>Edge.</b> Select AWS managed rules for WAF based on your needs and use them in default mode so they update automatically. Shield Advanced can protect Application Load Balancers, Elastic IP addresses and CloudFront distributions.</p>
      <p><b>Automate response.</b> Findings can trigger automation, for example updating a WAF IP set to block a suspicious host.</p>''')
    body += recall([
      'Layers: organization guardrails (SCPs), identity (IAM), network and edge (security groups, WAF, Shield), detection (GuardDuty, Config, Security Hub).',
      'SCPs filter; IAM grants; the effective permission is the overlap. SCPs do not apply to the management account.',
      'GuardDuty findings flow into Security Hub; Config is a prerequisite for the posture checks.',
      'Start Config rules in monitoring mode, then enforce. Administer security services from a delegated security account.',
      'Identity is the first line of defense; the network supports it.'])
    body += saythis('"I treat security as layers. SCPs in AWS Organizations are the outer guardrail on every account; IAM grants within it. Security groups and WAF guard the network and edge, and GuardDuty, Config and Security Hub detect and gather findings, with response automated from them. '
      'I roll guardrails out in monitoring mode first, and run the security services from a delegated security account."')
    body += trap([
      '<b>Turning on a deny guardrail everywhere on day one.</b> It can block legitimate deployments and stop teams. Watch first, fix, then enforce.',
      'Second trap: <b>trusting the network as the only defense.</b> A private network does not help if a stolen identity can reach everything. Identity first; the network supports it.'])
    body += confuse('🪪 IAM policy', 'Grants an identity permission to do specific things.', '🛡️ SCP', 'Limits what an account may use at all. Never grants; works with IAM, not instead of it.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt">{ "Version": "2012-10-17", "Statement": [{</span>
<span class="cmt">    "Effect": "Deny", "Action": "*", "Resource": "*",</span>
<span class="cmt">    "Condition": { "StringNotEquals": { "aws:RequestedRegion": ["eu-west-1","eu-central-1"] } } }] }</span>''',
      'Illustrative only — an SCP shaped like this denies actions outside two example Regions; real ones exempt global services and need careful testing.'))
    body += next_box('Guardrails say what <b>should</b> happen. You still need to see what <b>actually</b> happens — including for the guardrails themselves. Next: Monitoring &amp; Observability.', 'monitoring-observability.html', 'Monitoring &amp; Observability')
    body += fact_note(FOOT, [DOCS_SRA, DOCS_SEC, DOCS_SCP, DOCS_SH, DOCS_GD, DOCS_CFG, DOCS_PER])
    return page('security-governance', 'Security & Governance', 'Concept 16 of 19 · 🛠️ Shipping and operating',
        'Security is layers, not a wall — and governance is <span class="grad-text">guardrails that hold for every account, even when nobody is watching.</span>',
        'SCPs, IAM, WAF, Shield, GuardDuty, Config and Security Hub: how an architect applies protection consistently across everything.',
        'How would you secure and govern an AWS environment at scale?',
        body, CR + ['<span class="cur">Security &amp; Governance</span>'], '', search_title='Security & Governance')
