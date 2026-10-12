from kit import *
from p_common import CR

DOCS_CD = ('What is AWS CodeDeploy?', 'https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html')
DOCS_CFG = ('CodeDeploy deployment configurations', 'https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html')
DOCS_PIPE = ('AWS CodePipeline documentation', 'https://docs.aws.amazon.com/codepipeline/')
DOCS_BUILD = ('AWS CodeBuild documentation', 'https://docs.aws.amazon.com/codebuild/')
DOCS_OIDC = ('OIDC federation in IAM', 'https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html')
DOCS_OIDCR = ('Create a role for OpenID Connect federation', 'https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html')
FOOT = 'Tools and features change often. This page teaches the ideas; for current services, actions and limits, check the official AWS docs.'

def d_pipeline():
    d = Diagram('cd1', 640, 352, 'A deployment pipeline: a commit triggers build and test, deploy to a new version beside the old, then shift traffic, with a way back')
    rows = [
      ('💻 Commit to Git','the pipeline starts by itself','n'),
      ('🧪 Build and test','the same package every time','cyan'),
      ('🚦 Deploy beside the old version','production is untouched','amber'),
      ('🔁 Shift traffic to the new version','shift back to roll back','emerald'),
    ]
    labels = ['triggers', 'tests pass', 'new version is ready']
    for i,(t,s_,c) in enumerate(rows):
        y = 10 + i*86
        d.box(20, y, 600, 52, [(t,'t'),(s_,'s')], c)
        if i < 3:
            d.arrow([(320,y+52),(320,y+86)], 'n', label=labels[i], at=(420,y+69))
    return d

def d_strategies():
    d = Diagram('cd2', 640, 252, 'All-at-once shifts every user to the new version together; canary sends a small share first; linear increases the share in equal steps')
    d.zone(10, 8, 305, 236, 'emerald', 'ALL AT ONCE · blue/green')
    d.box(24, 96, 70, 50, [('👥 Users','t')], 'n')
    d.box(200, 40, 100, 50, [('🔵 Old','t'),('current','s')], 'n')
    d.box(200, 150, 100, 50, [('🟢 New','t'),('ready','s')], 'emerald')
    d.arrow([(94,121),(147,121),(147,65),(200,65)], 'n', label='before', at=(147,93))
    d.arrow([(250,150),(250,90)], 'emerald', label='switch', at=(282,120), both=True)
    d.text(162, 222, 'Switch back to undo.', size=9.5, weight=700)
    d.zone(325, 8, 305, 236, 'amber', 'CANARY · a small share first')
    d.box(339, 96, 70, 50, [('👥 Users','t')], 'n')
    d.box(515, 40, 100, 50, [('🔵 Old','t'),('most traffic','s')], 'n')
    d.box(515, 150, 100, 50, [('🟢 New','t'),('a small share','s')], 'amber')
    d.arrow([(409,111),(462,111),(462,65),(515,65)], 'n', label='most', at=(462,88))
    d.arrow([(409,131),(462,131),(462,175),(515,175)], 'amber', label='a few', at=(462,153))
    d.text(477, 222, 'Watch it, then send everyone.', size=9.5, weight=700)
    return d

def d_oidc():
    d = Diagram('cd3', 640, 214, 'A pipeline signs in to AWS with a short-lived token through OIDC federation, so no long-lived access key is stored')
    d.box(10, 52, 120, 64, [('🤖 Pipeline','t'),('GitHub Actions','s')], 'n')
    d.box(250, 52, 140, 64, [('🪪 IAM role','t'),('trusts this repo','s')], 'cyan')
    d.box(510, 52, 120, 64, [('☁️ AWS','t'),('deploy allowed','s')], 'emerald')
    d.arrow([(130,84),(250,84)], 'cyan', label='sends a token', at=(190,84))
    d.arrow([(390,84),(510,84)], 'emerald', label='temp keys', at=(450,84))
    d.text(320, 166, 'No long-lived access key is stored in the pipeline to leak.', size=9.5, weight=700)
    d.text(320, 186, 'The role\'s trust policy names the exact repository and branch that may use it.', size=9.5)
    return d

def build_ci_cd_deployment():
    body = ''
    body += see(figure(d_pipeline(),
        'a change goes through the same steps every time. A <b>commit</b> starts the pipeline. It <b>builds and tests</b> the code and makes one package. That package is <b>deployed beside the old version</b>, where it can be checked. '
        'Then <b>traffic shifts</b> to the new version — all at once, or gradually. If something is wrong, shift back.'))
    body += one('CI/CD means every change is built, tested and released by the same automatic steps — so shipping is routine, and undoing a bad release is one move.')
    body += why([
      'The environment is code now. The app is code too. If a person still copies files onto a server by hand, every release is different, every release is slow, and every release is a little scary — so teams release rarely, in big batches, which makes each one riskier.',
      '<b>CI</b> (continuous integration) builds and tests every change automatically. <b>CD</b> (continuous delivery or deployment) takes the tested package and ships it by a repeatable path. The second half of the skill is <b>how</b> it goes live: all at once, to a few users first, or in steps, with a quick way back.'])
    body += block('🧰 The pieces', pick_cards([
      dict(icon='🔗', name='AWS CodePipeline', tag='orchestrates the release stages', color='#22d3ee',
           use=['Source, build, test and deploy stages in order', 'Connects the other services'],
           skip=['You already run everything in another CI system — you can still deploy with it']),
      dict(icon='🧪', name='AWS CodeBuild', tag='builds and tests code', color='#a78bfa',
           use=['Compile, run tests, produce an artifact', 'A managed build service'],
           skip=['Deployment itself — that is CodeDeploy or another tool']),
      dict(icon='🚀', name='AWS CodeDeploy', tag='deploys with a chosen strategy', color='#34d399',
           use=['In-place on EC2 or on-premises; blue/green on EC2, Lambda and ECS', 'Traffic shifting for Lambda and ECS: all at once, canary or linear'],
           skip=['In-place for Lambda and ECS — those platforms use blue/green']),
      dict(icon='🐙', name='GitHub Actions and others', tag='your own pipeline tool', color='#fbbf24',
           use=['Your code is already on GitHub', 'Sign in to AWS with OIDC and a role instead of a stored key'],
           skip=['Storing an access key as a pipeline secret']),
    ]), label_cls='see')
    body += block('🧭 How a release goes live', figure(d_strategies(),
        '<b>Blue/green</b> (left): the new version (green) runs beside the old (blue); when it is ready, traffic switches. Rolling back is switching back. '
        '<b>Canary</b> (right): a small share of traffic goes to the new version first; if it looks healthy, the rest follows. <b>Linear</b> is similar, but the share rises in equal steps with equal waits. '
        'For Lambda and ECS, CodeDeploy offers all-at-once, canary and linear traffic shifting, with predefined and custom configurations.'), label_cls='see')
    body += block('🔑 Deploy without a stored key', figure(d_oidc(),
        'old pipelines kept an access key to log in to AWS — a permanent secret that can leak. With <b>OIDC federation</b> the pipeline presents a short-lived token from its identity provider; an <b>IAM role</b> trusts that provider and returns temporary credentials. '
        'The role\'s trust policy should name the exact repository (and branch) allowed to use it — otherwise workflows you do not control could assume it. This is the role idea from concept 3, applied to the pipeline.'), label_cls='see')
    body += block('📊 Choosing a release style', table(['Style','What happens','Rollback','Best when'], [
      ['🔁 Blue/green, all at once','New version warmed up beside the old, then takes all traffic','Switch back','You want a clean cut-over'],
      ['🐤 Canary','A small share first, then the rest','Send the share back to zero','You are unsure and want real-user proof'],
      ['📈 Linear','The share rises in equal steps with waits','Stop and shift back','You want a gradual, steady rollout'],
      ['🔧 In-place (EC2)','Instances are updated where they are, a few at a time','Redeploy the old version','Simple apps on servers'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🛒','Release the shop on a Friday afternoon','No downtime, and a fast way back.','Blue/green'),
      ('📈','A risky pricing change','Try it on a few users first.','Canary traffic shifting'),
      ('🔑','The team stores an access key as a pipeline secret','It leaked in a log once.','OIDC and a role'),
      ('🧪','Every pull request must be tested','Nothing merges if tests fail.','CI on each change'),
      ('🏗️','Release infrastructure and app together','The template and the code change as one.','One pipeline: deploy the stack, then the app'),
      ('⏪','A bad release reaches production','Customers see errors right now.','Shift traffic back to the old version'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — details that bite', '''      <p><b>Platform differences.</b> In-place deployments are for EC2 and on-premises instances; Lambda and ECS cannot use in-place and use blue/green with traffic shifting.</p>
      <p><b>Build once, deploy the same package everywhere.</b> If each environment builds its own copy, "it worked in staging" proves little.</p>
      <p><b>Health decides.</b> CodeDeploy tracks application health with rules you configure; wire in alarms (concept 17) so a bad canary stops by itself.</p>
      <p><b>OIDC trust.</b> Add the provider to IAM, create a web-identity role with the expected audience, and restrict the trust policy to your repository and branch. AWS recommends matching on immutable identifiers where available, because names can change.</p>''')
    body += recall([
      'CI builds and tests every change automatically; CD ships the tested package by a repeatable path.',
      'CodePipeline orchestrates, CodeBuild builds and tests, CodeDeploy deploys with a strategy.',
      'Blue/green runs the new version beside the old and switches traffic; canary sends a small share first; linear raises it in equal steps.',
      'Lambda and ECS deployments use blue/green traffic shifting; in-place is for EC2 and on-premises.',
      'Prefer OIDC and an IAM role to a stored access key for pipeline sign-in; scope the trust policy to the repo and branch.'])
    body += saythis('"I use a pipeline: every change is built and tested, then deployed beside the current version and traffic is shifted — all at once for a clean cut-over, canary or linear when I want proof from real users — and shifting back is my rollback. '
      'The pipeline signs in with OIDC to an IAM role scoped to the repository, so no access key is stored."')
    body += trap([
      '<b>A stored access key for the pipeline.</b> It is a long-lived secret that leaks through logs, forks and screenshots. Use short-lived credentials through OIDC.',
      'Second trap: <b>an unrestricted OIDC trust policy.</b> If the role trusts the provider without naming your repository and branch, workflows outside your control can assume it.'])
    body += confuse('🔁 Blue/green', 'The new version waits beside the old, then everyone switches together.', '🐤 Canary', 'A small share goes to the new version first, so real users test it before everyone does.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># start a CodeDeploy deployment using a canary traffic-shifting configuration (ECS)</span>
aws deploy create-deployment --application-name shop --deployment-group-name prod \\
    --deployment-config-name CodeDeployDefault.ECSCanary10Percent5Minutes \\
    --revision file://appspec-revision.json''',
      'Illustrative shape only — the names and revision file are placeholders; the predefined configuration here sends 10 percent first, then the rest five minutes later.'))
    body += next_box('You can now ship changes safely. But apps and pipelines need credentials and settings — database passwords, API keys, feature switches — and hard-coding them is the classic leak. Next: Secrets &amp; Configuration.', 'secrets-configuration.html', 'Secrets &amp; Configuration')
    body += fact_note(FOOT, [DOCS_CD, DOCS_CFG, DOCS_PIPE, DOCS_BUILD, DOCS_OIDC, DOCS_OIDCR])
    return page('ci-cd-deployment', 'CI/CD & Deployment Strategies', 'Concept 14 of 19 · 🛠️ Shipping and operating',
        'CI/CD makes every release the same automatic steps — <span class="grad-text">so shipping is routine, and undoing a bad release is one move.</span>',
        'Pipelines, blue/green, canary and linear deployments and passwordless sign-in with OIDC: how to ship to AWS safely and roll back fast.',
        'How would you set up CI/CD to AWS with zero downtime and a safe rollback?',
        body, CR + ['<span class="cur">CI/CD &amp; Deployment</span>'], '', search_title='CI/CD & Deployment Strategies')
