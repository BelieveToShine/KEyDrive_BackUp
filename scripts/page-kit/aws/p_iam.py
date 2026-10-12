from kit import *
from p_common import CR

DOCS_IAM = ('AWS IAM user guide', 'https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html')
DOCS_BP = ('Security best practices in IAM', 'https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html')
DOCS_ROOT = ('Root user best practices', 'https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html')
DOCS_IDC = ('IAM Identity Center', 'https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html')
DOCS_ROLES = ('IAM roles', 'https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html')
DOCS_EC2R = ('IAM roles for Amazon EC2', 'https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html')
DOCS_STS = ('AssumeRole (AWS STS)', 'https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits and new features, check the official AWS docs.'

def d_who():
    d = Diagram('ia1', 640, 280, 'Three kinds of caller reach AWS: people through Identity Center, workloads through roles, and the rarely used root user; IAM checks policies and allows only what a policy allows')
    d.box(10, 24, 150, 62, [('👤 A person','t'),('Identity Center','s')], 'cyan')
    d.box(10, 108, 150, 62, [('🤖 A workload','t'),('an IAM role','s')], 'emerald')
    d.box(10, 192, 150, 62, [('👑 Root user','t'),('rare tasks only','s')], 'rose')
    d.box(300, 70, 130, 120, [('🧾 IAM','t'),('checks the','s'),('policies on','s'),('every request','s')], 'violet')
    d.arrow([(160,55),(230,55),(230,110),(300,110)], 'cyan', label='temporary', at=(230,82))
    d.arrow([(160,139),(300,139)], 'emerald', label='temporary', at=(230,139))
    d.arrow([(160,223),(230,223),(230,170),(300,170)], 'rose', label='avoid', at=(230,196), dash=True)
    d.box(520, 36, 110, 52, [('✅ Allowed','t')], 'emerald')
    d.box(520, 172, 110, 52, [('⛔ Denied','t')], 'rose')
    d.arrow([(430,100),(475,100),(475,62),(520,62)], 'emerald', label='allow', at=(475,81))
    d.arrow([(430,160),(475,160),(475,198),(520,198)], 'rose', label='no allow', at=(475,179))
    return d

def d_policy():
    d = Diagram('ia2', 640, 252, 'A policy statement is made of an effect, an action and a resource; each part narrows what is allowed')
    d.code_box(10, 24, 340, 176, [
        (0,'{','') , (14,'"Effect": "Allow",','k'), (14,'"Action": "s3:GetObject",','k'),
        (14,'"Resource": "arn:aws:s3:::reports/*"','k'), (0,'}','')], 'violet', size=9.5, lh=18)
    d.text(180, 226, 'Read one kind of object, in one bucket — and nothing else.', size=9.5, weight=700)
    d.box(470, 24, 160, 50, [('✅ Effect','t'),('Allow or Deny','s')], 'emerald')
    d.box(470, 84, 160, 50, [('🔧 Action','t'),('which API call','s')], 'cyan')
    d.box(470, 144, 160, 50, [('🎯 Resource','t'),('which thing','s')], 'amber')
    d.arrow([(470,49),(350,49)], 'emerald', label='sets', at=(410,49))
    d.arrow([(470,109),(350,109)], 'cyan', label='names', at=(410,109))
    d.arrow([(470,169),(350,169)], 'amber', label='limits', at=(410,169))
    return d

def d_eval():
    d = Diagram('ia3', 640, 346, 'How IAM decides: an explicit deny always wins; otherwise something must allow the request; otherwise it is denied by default')
    d.box(190, 8, 260, 34, [('🤔 A request arrives','t')], 'cyan')
    qs = [
     ('🚫 Any explicit Deny that applies?', 'in any policy, anywhere', 'Denied', 'a Deny always wins', 'rose'),
     ('✅ Does a policy allow it?', 'and no SCP blocks it', 'Allowed', 'least privilege in action', 'emerald'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 272
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 272, 330, 54, [('⛔ Nothing allows it','t'),('denied by default','s')], 'rose')
    return d

def build_identity_access():
    body = ''
    body += see(figure(d_who(),
        'every call to AWS comes from somebody: a <b>person</b> (who should sign in through IAM Identity Center and get temporary credentials), a <b>workload</b> (which gets temporary credentials from an IAM <b>role</b>), or — rarely — the <b>root user</b>. '
        '<b>IAM</b> checks the policies on every request. If a policy allows it, it goes through; if nothing allows it, it is denied. Notice the word <i>temporary</i>: long-lived keys are what you try to avoid.'))
    body += one('IAM answers "who may do what to which thing?" — and the safe default is that nobody may do anything until a policy says so, using temporary credentials for people and for apps.')
    body += why([
      'You now have accounts and Regions, and resources are about to be created in many places. The next question is not "can it be reached?" but <b>"who or what is allowed to create, read or change each thing?"</b> That includes your apps, not just people — an app that can read a database is an identity too.',
      'AWS answers with <b>IAM</b> (Identity and Access Management). Everything is denied by default; you grant access with <b>policies</b>; and AWS pushes you toward <b>temporary credentials</b> — roles for workloads, federation for people — instead of long-lived keys that can leak. This page is the map; the Roles deep dive shows the mechanics.'])
    body += block('🧰 The pieces', pick_cards([
      dict(icon='🎭', name='IAM role', tag='an identity with temporary credentials', color='#34d399',
           use=['Apps and services (EC2, Lambda, containers) that need AWS access', 'Cross-account access', 'Anything that should not have a permanent key'],
           skip=['A person who needs everyday access — use Identity Center instead']),
      dict(icon='🧑‍🤝‍🧑', name='IAM Identity Center', tag='sign-in for your workforce', color='#22d3ee',
           use=['AWS\'s recommended way to give people access to accounts', 'One place for users and their permissions across accounts', 'People get temporary credentials'],
           skip=['Workloads — those use roles']),
      dict(icon='📜', name='IAM policy', tag='a JSON document of allowed or denied actions', color='#a78bfa',
           use=['Say exactly which actions on which resources', 'Start from AWS managed policies, then tighten to your own', 'Pair with last-accessed data to remove unused permissions'],
           skip=['Wildcards for everything ("*") — that is not least privilege']),
      dict(icon='👑', name='Root user', tag='the all-powerful account owner', color='#fb7185',
           use=['Only the few tasks that really need it', 'Turn on MFA; do not create root access keys'],
           skip=['Daily work — never use root for that']),
    ]), label_cls='see')
    body += block('📜 What a policy says', figure(d_policy(),
        'a policy is a list of <b>statements</b>. Each says: an <b>Effect</b> (Allow or Deny), an <b>Action</b> (which API call, such as reading an object) and a <b>Resource</b> (which thing). Statements can also have conditions. '
        'Least privilege means writing the narrowest statement that still lets the job work — here, reading objects in one bucket and nothing else. IAM Access Analyzer can even draft policies from what a role actually used.'), label_cls='see')
    body += block('⚖️ How IAM decides', figure(d_eval(),
        'a request is judged in a fixed order. If any applicable policy has an <b>explicit Deny</b>, it is denied — a Deny always wins. Otherwise something must <b>allow</b> it, and no service control policy (concept 1) may block it. If nothing allows it, it is denied by default. '
        'So permissions are the <em>overlap</em> of what the organization lets the account do and what the identity\'s own policies grant.'), label_cls='see')
    body += block('📊 People, apps and root', table(['','How they get access','Credentials','Rule of thumb'], [
      ['👤 People','IAM Identity Center (federation)','Temporary','Avoid IAM users with long-lived passwords and keys'],
      ['🤖 Apps and services','An IAM role on the compute service','Temporary, rotated automatically','Never put access keys in code'],
      ['🔗 Another account','A role that the other account may assume','Temporary','Trust a specific account, not everyone'],
      ['👑 Root user','Email and password with MFA','Long-lived','Use only for tasks that require it'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🖥️','A web server must read files from storage','Nobody should type a key into the server.','A role on the instance, read-only to that bucket'),
      ('👩‍💻','A new developer joins','They need access to two accounts.','Identity Center with a permission set'),
      ('🔁','A pipeline deploys to production','It runs in another account.','A role it can assume, with just the deploy rights'),
      ('🔑','An access key is found on a public repository','It can act as a person forever.','Rotate or delete it; move to roles'),
      ('🧹','A role has more permissions than it uses','Nobody remembers why.','Check last-accessed data and tighten'),
      ('👑','Someone wants to "just use root"','It works everywhere, too well.','Say no; use a role with the right rights'),
    ]), label_cls='see')
    body += block('🔬 Go deeper', deep_cards([('Deep dive · IAM', 'IAM Roles: trust, permissions and temporary credentials', 'How a role is assumed, what a trust policy is, how an EC2 instance gets its credentials, and how cross-account access works.', 'iam-roles.html')]), label_cls='next')
    body += zoom('Go one level deeper (60 seconds) — habits AWS recommends', '''      <p><b>Temporary credentials first.</b> AWS recommends that people reach accounts through federation (temporary credentials) and that workloads use roles. Where long-term keys are unavoidable, rotate them when needed, for example when someone leaves.</p>
      <p><b>Root user.</b> Use it only for the few tasks that require it. Do not create root access keys, turn on MFA, and in a multi-account organization remove root credentials from member accounts so nobody can sign in as root there.</p>
      <p><b>Least privilege.</b> Grant only what a task needs. Start with AWS managed policies, then move to customer managed policies that fit. IAM Access Analyzer can generate a policy from the access activity it sees, and last-accessed data shows permissions nobody uses.</p>
      <p><b>Guardrails above IAM.</b> Service control policies in an organization limit what accounts can do whatever their own IAM says — they filter and never grant.</p>
      <p><b>Groups and users.</b> IAM users and groups still exist, but for people, Identity Center is the recommended door.</p>''')
    body += recall([
      'IAM: who may do what to which resource. Everything is denied by default; policies grant access.',
      'A policy statement has Effect, Action, Resource (and optional Condition). An explicit Deny always wins.',
      'People: IAM Identity Center and temporary credentials. Workloads: IAM roles. Avoid long-lived access keys.',
      'Root user: only for tasks that need it, with MFA and no root access keys.',
      'Effective permission = what SCPs allow ∩ what the identity\'s policies allow. Use IAM Access Analyzer and last-accessed data to tighten.'])
    body += saythis('"IAM is deny-by-default: access exists only where a policy allows it, and an explicit deny always wins. People sign in through IAM Identity Center and get temporary credentials; workloads use IAM roles, so no access keys live in code. '
      'I write least-privilege policies with the help of Access Analyzer, keep root locked away with MFA, and use service control policies as guardrails above the accounts."')
    body += trap([
      '<b>Putting an access key in the code, an environment file or a pipeline variable.</b> It is a permanent password for your account. Give the workload a role and let AWS hand it temporary credentials.',
      'Second trap: <b>fixing a permission error by giving administrator access.</b> It works, and it quietly turns every bug and every leaked token into a full-account incident. Add the one missing action instead.'])
    body += confuse('👤 IAM user', 'A permanent identity with long-lived credentials. Avoid for people when you can.', '🎭 IAM role', 'An identity you assume for a while and get temporary credentials for. The default for workloads.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># see who you are right now — a quick way to check which identity the CLI is using</span>
aws sts get-caller-identity''',
      'Illustrative shape only — the output shows an account ID, a user ID and an ARN, which differ for every caller.'))
    body += next_box('Identity says who may call what. <b>Networking</b> decides what can physically reach what. Resources need isolation and controlled paths before they hold real traffic. Next: VPC Networking.', 'vpc-networking.html', 'VPC Networking')
    body += fact_note(FOOT, [DOCS_IAM, DOCS_BP, DOCS_ROOT, DOCS_IDC, DOCS_ROLES])
    return page('identity-access', 'Identity & Access (IAM)', 'Concept 3 of 19 · 🏗️ Foundations',
        'IAM answers "who may do what to which thing?" — and the safe default is <span class="grad-text">nobody, until a policy says so.</span>',
        'IAM policies, roles, Identity Center and the root user: how access works on AWS and why temporary credentials beat long-lived keys.',
        'How does IAM work, and how would you give an application access to AWS resources safely?',
        body, CR + ['<span class="cur">Identity &amp; Access (IAM)</span>'], '', search_title='Identity & Access (IAM)')

# ------------------------------------------------------------------ deep dive: IAM roles
def d_assume():
    d = Diagram('ir1', 640, 300, 'An EC2 instance gets temporary credentials from its role through an instance profile and the metadata service, with no key stored on the server')
    d.box(10, 110, 120, 70, [('🖥️ EC2 instance','t'),('runs your app','s')], 'n')
    d.box(250, 110, 130, 70, [('🏷️ Instance','t'),('profile','t')], 'amber')
    d.box(510, 110, 120, 70, [('🎭 IAM role','t'),('the permissions','s')], 'emerald')
    d.arrow([(130,145),(250,145)], 'amber', label='has', at=(190,145))
    d.arrow([(380,145),(510,145)], 'emerald', label='carries one', at=(445,145))
    d.arrow([(570,110),(570,52),(70,52),(70,110)], 'cyan', label='temporary credentials via instance metadata', at=(320,52))
    d.text(320, 236, 'The app (or the AWS SDK) reads fresh credentials from the metadata service.', size=9.5)
    d.text(320, 254, 'They are rotated automatically, so there is nothing to store or rotate by hand.', size=9.5, weight=700)
    return d

def d_trust():
    d = Diagram('ir2', 640, 300, 'A role has two policies: a trust policy saying who may assume it and a permissions policy saying what it can do')
    d.box(10, 108, 120, 64, [('👤 Caller','t'),('person or service','s')], 'n')
    d.box(250, 40, 150, 64, [('🤝 Trust policy','t'),('who may assume','s')], 'amber')
    d.box(250, 176, 150, 64, [('📜 Permissions policy','t'),('what it may do','s')], 'violet')
    d.box(510, 108, 120, 64, [('🎭 The role','t')], 'emerald')
    d.arrow([(130,125),(190,125),(190,72),(250,72)], 'amber', label='checked by', at=(190,98))
    d.arrow([(400,72),(455,72),(455,125),(510,125)], 'amber', label='lets it in', at=(455,98))
    d.arrow([(510,155),(455,155),(455,208),(400,208)], 'violet', label='then limits', at=(455,182))
    d.text(320, 278, 'Without a trust policy that names the caller, nobody can use the role.', size=9.5, weight=700)
    return d

def d_cross():
    d = Diagram('ir3', 640, 292, 'Cross-account access: a caller in account A asks STS to assume a role in account B, STS checks the role trusts the caller, and returns temporary credentials')
    d.zone(10, 8, 250, 240, 'cyan', 'ACCOUNT A')
    d.box(34, 104, 100, 60, [('🧑‍💻 Caller','t'),('wants access','s')], 'n')
    d.box(270, 104, 100, 60, [('🎟️ STS','t'),('issues tokens','s')], 'amber')
    d.zone(380, 8, 250, 240, 'emerald', 'ACCOUNT B')
    d.box(470, 104, 140, 60, [('🎭 Role','t'),('trusts account A','s')], 'emerald')
    d.arrow([(134,122),(270,122)], 'amber', label='1 · assume', at=(202,122))
    d.arrow([(370,134),(470,134)], 'emerald', label='2 · trust?', at=(420,134))
    d.arrow([(270,150),(134,150)], 'amber', label='3 · keys', at=(202,150))
    d.text(320, 272, 'Temporary credentials: an access key ID, a secret key and a session token.', size=9.5, weight=700)
    return d

def build_iam_roles():
    body = ''
    body += see(figure(d_assume(),
        'an EC2 instance is linked to a role through an <b>instance profile</b> — a small wrapper that holds one role. The app on the instance (usually through the AWS SDK) asks the <b>instance metadata service</b> for credentials and gets short-lived ones that AWS renews on its own. '
        'No access key is ever written to the disk, so there is nothing to leak or forget to rotate.'))
    body += one('A role is an identity with no password: something trusted can step into it for a while, and AWS hands out temporary credentials that match its permissions.')
    body += why([
      'The IAM page said: use roles, not keys. This page shows <b>how a role actually works</b>, because the same few ideas explain EC2, Lambda, containers, pipelines and cross-account access.',
      'A role has two policies with two different jobs: a <b>trust policy</b> (who may become this role) and a <b>permissions policy</b> (what the role may do). Learn that split and most "access denied" mysteries become easy to read.'])
    body += block('🧰 The vocabulary', pick_cards([
      dict(icon='🤝', name='Trust policy', tag='who may assume the role', color='#fbbf24',
           use=['Names the service or account allowed to use the role', 'For EC2 the trusted principal is the EC2 service'],
           skip=['Expecting it to grant any permission — it only lets someone in']),
      dict(icon='📜', name='Permissions policy', tag='what the role may do', color='#a78bfa',
           use=['The actions and resources, like any IAM policy', 'Keep it to least privilege'],
           skip=['Making it "admin" so the app stops failing']),
      dict(icon='🏷️', name='Instance profile', tag='the wrapper that carries a role to EC2', color='#22d3ee',
           use=['Holds exactly one role', 'The console creates it for you when you make the role for EC2'],
           skip=['Looking for it with Lambda or ECS — those attach roles directly']),
      dict(icon='🎟️', name='AWS STS', tag='the service that issues temporary credentials', color='#34d399',
           use=['AssumeRole returns an access key ID, a secret and a session token', 'Used for cross-account access and for people switching roles'],
           skip=['Calling it on EC2 to re-assume the instance\'s own role — not needed']),
    ]), label_cls='see')
    body += block('🤝 Two policies, two jobs', figure(d_trust(),
        'when something tries to use the role, AWS first checks the <b>trust policy</b>: is this caller on the list of who may assume it? Only then does the <b>permissions policy</b> decide what the session can do. '
        'If you can\'t assume the role, read the trust policy. If you can assume it but get "access denied" on an action, read the permissions policy.'), label_cls='see')
    body += block('🔁 Crossing accounts', figure(d_cross(),
        'a caller in account A asks <b>STS</b> to assume a role that lives in account B. STS checks that B\'s role trusts A, and hands back <b>temporary credentials</b>: an access key ID, a secret key and a session token. '
        'The caller\'s permissions in B are exactly the role\'s — nothing else from account A carries over. This is how one account\'s pipeline deploys into another account without any shared password.'), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🖥️','An EC2 app reads from storage','No key on the disk.','Instance profile with a read-only role'),
      ('⚡','A Lambda function writes to a table','It needs only that table.','An execution role'),
      ('🏗️','A CI pipeline deploys to production','It lives in a tools account.','A cross-account role it assumes'),
      ('🧑‍💻','An admin needs powerful rights for 30 minutes','Not all day.','Assume an admin role, then drop it'),
      ('🚀','You launch an instance with a role','The launch fails with "not authorized to pass role".','Allow iam:PassRole for that role'),
      ('🔄','You change the role on a running server','Is it instant?','Replace the instance profile; changes can take time'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — details that bite', '''      <p><b>Credentials renew themselves.</b> For EC2, the SDK reads credentials from the instance metadata path for the role. They are temporary and AWS issues new ones at least five minutes before the old ones expire.</p>
      <p><b>PassRole.</b> The person or pipeline that launches an instance with a role needs permission to <i>pass</i> that role (iam:PassRole), not only permission to launch. Scope it to the one role and the one service it may be passed to.</p>
      <p><b>Session permissions.</b> The effective permissions of an assumed-role session are the overlap of the role\'s permissions and any session policy passed in, so a session can be narrower than the role.</p>
      <p><b>Do not re-assume.</b> A workload on EC2 does not need to call AssumeRole for the role already on the instance; it only needs it for other roles, or to add session tags or a session policy.</p>
      <p><b>Changing a role on a running instance.</b> Replace the instance profile rather than removing the role; removing a role from a profile is discouraged because the change can take a long time to take effect.</p>''')
    body += recall([
      'A role is assumed, not signed into: callers get temporary credentials from STS (access key ID, secret, session token).',
      'Trust policy = who may assume. Permissions policy = what the role may do.',
      'EC2 uses an instance profile (holds one role); the app reads rotating credentials from the instance metadata service.',
      'Cross-account: the caller assumes a role in the other account; that role must trust the caller.',
      'Launching with a role needs iam:PassRole, scoped to that role.'])
    body += saythis('"A role has a trust policy that says who may assume it and a permissions policy that says what it can do. On EC2 an instance profile carries the role and the SDK reads temporary credentials from the metadata service, which AWS rotates. '
      'For cross-account access the caller assumes a role in the other account through STS and gets temporary keys. Launching with a role also needs iam:PassRole."')
    body += trap([
      '<b>Mixing up the two policies.</b> Adding a permission to the trust policy does nothing for what the role can do, and adding it to the permissions policy does nothing for who can assume it.',
      'Second trap: <b>trusting "the whole account" when you meant one role.</b> A trust policy that names an entire account lets every identity there with the right permission assume the role. Name the narrowest principal you can.'])
    body += confuse('🤝 Trust policy', 'Answers "who may become this role?" Attached to the role itself.', '📜 Permissions policy', 'Answers "what may this role do?" Written like any other IAM policy.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># ask STS for temporary credentials for a role in another account</span>
aws sts assume-role --role-arn arn:aws:iam::111122223333:role/deploy --role-session-name pipeline''',
      'Illustrative shape only — the account ID is a placeholder, and the output holds an access key ID, a secret and a session token that expire.'))
    body += next_box('That is how roles work. Back to the IAM page for the whole map — and on to the next concept: VPC Networking.', 'identity-access.html', 'Back to IAM')
    body += fact_note(FOOT, [DOCS_ROLES, DOCS_EC2R, DOCS_STS, DOCS_BP])
    return page('iam-roles', 'IAM Roles', 'Deep dive · IAM · 🎭 Roles',
        'A role is an identity with no password — <span class="grad-text">something trusted steps into it, and AWS hands out temporary credentials.</span>',
        'Trust policies, permissions policies, instance profiles and STS: how roles really work, for EC2 and across accounts.',
        'How does an EC2 instance or another account get permissions through an IAM role?',
        body, CR + ['<a href="identity-access.html">Identity &amp; Access (IAM)</a>', '<span class="cur">IAM Roles</span>'], '', search_title='IAM Roles')
