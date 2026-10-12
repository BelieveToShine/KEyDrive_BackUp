from kit import *
from p_storage import CR

DOCS_SLOTS = ('Set up staging slots in App Service', 'https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots')
DOCS_BP = ('App Service deployment best practices', 'https://learn.microsoft.com/en-us/azure/app-service/deploy-best-practices')
DOCS_AP = ('CI/CD with Azure Pipelines for App Service', 'https://learn.microsoft.com/en-us/azure/app-service/deploy-azure-pipelines')
DOCS_GH = ('Continuous deployment for App Service', 'https://learn.microsoft.com/en-us/azure/app-service/deploy-continuous-deployment')
DOCS_TR = ('az webapp traffic-routing', 'https://learn.microsoft.com/en-us/cli/azure/webapp/traffic-routing')
FOOT = 'Tools and features change often. This page teaches the ideas; for current tasks, actions and limits, check the official docs.'

def d_pipeline():
    d = Diagram('cd1', 640, 352, 'A deployment pipeline: a commit triggers build and test, deploy to a staging slot, then a swap into production that can be reversed')
    rows = [
      ('💻 Commit to Git','the pipeline starts by itself','n'),
      ('🧪 Build and test','the same package every time','cyan'),
      ('🚦 Deploy to a staging slot','production is untouched','amber'),
      ('🔁 Swap into production','swap again to roll back','emerald'),
    ]
    labels = ['triggers', 'tests pass', 'warmed up, checked']
    for i,(t,s_,c) in enumerate(rows):
        y = 10 + i*86
        d.box(20, y, 600, 52, [(t,'t'),(s_,'s')], c)
        if i < 3:
            d.arrow([(320,y+52),(320,y+86)], 'n', label=labels[i], at=(420,y+69))
    return d

def d_strategies():
    d = Diagram('cd2', 640, 252, 'Swap moves all users to the new version at once; a traffic split sends only a small share first')
    d.zone(10, 8, 305, 236, 'emerald', 'SWAP · all at once')
    d.box(24, 96, 70, 50, [('👥 Users','t')], 'n')
    d.box(200, 40, 100, 50, [('🔵 Production','t'),('old version','s')], 'n')
    d.box(200, 150, 100, 50, [('🟢 Staging','t'),('new version','s')], 'emerald')
    d.arrow([(94,121),(147,121),(147,65),(200,65)], 'n', label='all traffic', at=(147,93))
    d.arrow([(250,150),(250,90)], 'emerald', label='swap', at=(282,120), both=True)
    d.text(162, 222, 'Swap back to undo.', size=9.5, weight=700)
    d.zone(325, 8, 305, 236, 'amber', 'SPLIT · a small share first')
    d.box(339, 96, 70, 50, [('👥 Users','t')], 'n')
    d.box(515, 40, 100, 50, [('🔵 Production','t'),('most traffic','s')], 'n')
    d.box(515, 150, 100, 50, [('🟢 Staging','t'),('a small share','s')], 'amber')
    d.arrow([(409,111),(462,111),(462,65),(515,65)], 'n', label='most', at=(462,88))
    d.arrow([(409,131),(462,131),(462,175),(515,175)], 'amber', label='a few', at=(462,153))
    d.text(477, 222, 'Watch it, then send everyone — or no one.', size=9.5, weight=700)
    return d

def d_oidc():
    d = Diagram('cd3', 640, 214, 'A pipeline signs in to Azure with a short-lived token from Microsoft Entra ID instead of a stored password')
    d.box(10, 52, 120, 64, [('🤖 Pipeline','t'),('GitHub Actions','s')], 'n')
    d.box(250, 52, 140, 64, [('🔐 Entra ID','t'),('trusts this repo','s')], 'cyan')
    d.box(510, 52, 120, 64, [('☁️ Azure','t'),('deploy allowed','s')], 'emerald')
    d.arrow([(130,84),(250,84)], 'cyan', label='sends a token', at=(190,84))
    d.arrow([(390,84),(510,84)], 'emerald', label='gets access', at=(450,84))
    d.text(320, 166, 'No long-lived password or key is stored in the pipeline to leak.', size=9.5, weight=700)
    d.text(320, 186, 'This is called workload identity federation (OpenID Connect).', size=9.5)
    return d

def build_ci_cd_deployment():
    body = ''
    body += see(figure(d_pipeline(),
        'a change goes through the same steps every time. A <b>commit</b> starts the pipeline. It <b>builds and tests</b> the code and makes one package. That package is <b>deployed to a staging slot</b> — a second copy of the app next to production — where it is warmed up and checked. '
        'Then a <b>swap</b> puts it into production. If something is wrong, swap again and the old version is back.'))
    body += one('CI/CD means every change is built, tested and released by the same automatic steps — so shipping is routine, and undoing a bad release is one move.')
    body += why([
      'The environment is code now. The app is code too. If a person still copies files onto a server by hand, every release is different, every release is slow, and every release is a little scary — so teams release rarely, in big batches, which makes each one riskier.',
      '<b>CI</b> (continuous integration) builds and tests every change automatically. <b>CD</b> (continuous delivery or deployment) takes the tested package and ships it by a repeatable path. The second half of the skill is <b>how</b> it goes live: all at once, to a few users first, or beside the old version with a quick way back.'])
    body += block('🧰 The pieces', pick_cards([
      dict(icon='🐙', name='GitHub Actions', tag='pipelines in your repository', color='#a78bfa',
           use=['Your code is already on GitHub', 'Workflows live as files next to the code', 'Deploy to App Service, Functions, containers'],
           skip=['Your team already runs everything in Azure DevOps']),
      dict(icon='🔷', name='Azure Pipelines', tag='pipelines in Azure DevOps', color='#22d3ee',
           use=['You use Azure DevOps boards and repos', 'Tasks to deploy to a slot and to swap slots'],
           skip=['You are fully on GitHub and want one place']),
      dict(icon='🚦', name='Deployment slots', tag='a staging copy of an App Service app', color='#34d399',
           use=['Zero-downtime releases: warm up, then swap', 'Fast rollback by swapping back', 'Available on Standard, Premium and Isolated tiers'],
           skip=['Free and basic tiers do not have slots']),
      dict(icon='🔐', name='OIDC sign-in', tag='workload identity federation', color='#fbbf24',
           use=['The pipeline needs to deploy without a stored secret', 'Microsoft recommends it over passwords or publish profiles'],
           skip=['Nothing — treat stored deployment passwords as the thing to avoid']),
    ]), label_cls='see')
    body += block('🧭 How a release goes live', figure(d_strategies(),
        '<b>Swap</b> (left, "blue-green"): the new version waits in a staging slot, gets warmed up and checked, then takes over all traffic at once. Rolling back is swapping again. '
        '<b>Split</b> (right, "canary"): App Service can send a chosen percentage of requests to the staging slot while the rest stay on production. You watch errors and speed, then send everyone — or pull the slot back to zero. '
        'A user routed to a slot stays pinned to it for a while, so their session is consistent.'), label_cls='see')
    body += block('🔑 Deploy without a stored password', figure(d_oidc(),
        'old pipelines kept a password or key to log in to Azure — a secret that can leak. With <b>OpenID Connect</b> the pipeline asks Microsoft Entra ID for a short-lived token, proving who it is (this repo, this workflow). Entra ID trusts it and Azure lets the deployment through. '
        'This is the identity idea from concept 3, applied to the pipeline itself.'), label_cls='see')
    body += block('📊 Choosing a release style', table(['Style','What happens','Rollback','Best when'], [
      ['🔁 Swap (blue-green)','New version warmed up beside the old, then takes all traffic','Swap again','You want zero downtime and a clean cut-over'],
      ['🐤 Traffic split (canary)','A small share of users hits the new version first','Set the share back to zero','You are not sure and want real-user proof'],
      ['⏩ Direct to production','Files replace the running app','Redeploy the old version','Only for tiny, low-risk apps'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🛒','Release the shop on a Friday afternoon','No downtime, and a fast way back if checkout breaks.','Staging slot + swap'),
      ('📈','A risky pricing change','Try it on a few users and watch conversion.','Traffic split to a slot'),
      ('🔑','The team stores a deploy password in a secret','It leaked in a log once.','OIDC sign-in (no stored password)'),
      ('🧪','Every pull request must be tested','Nothing merges if tests fail.','CI on each change'),
      ('🏗️','Release app and infrastructure together','The Bicep file and the code change as one.','One pipeline: deploy infra, then app'),
      ('⏪','A bad release reaches production','Customers see errors right now.','Swap back to the previous slot'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — details that bite', '''      <p><b>Build once, deploy the same package everywhere.</b> If each environment builds its own copy, "it worked in staging" proves little.</p>
      <p><b>Slot settings.</b> Some settings (such as connection strings marked "slot setting") stay with the slot and do not move during a swap. Mark them deliberately, or the swapped app can end up pointing at the wrong database.</p>
      <p><b>Slots share the plan.</b> A staging slot runs on the same App Service plan as production, so it uses the same capacity; scaling the plan affects all slots.</p>
      <p><b>Preview the swap.</b> App Service can apply the target slot\'s settings to the source slot before the swap completes, so you can check behaviour first and then complete or cancel.</p>
      <p><b>Other services.</b> Containers and Functions have their own release features (revisions, slots) — the ideas are the same: ship beside, check, switch, and keep a way back.</p>''')
    body += recall([
      'CI builds and tests every change automatically; CD ships the tested package by a repeatable path.',
      'Deployment slots (Standard tier and above): deploy to staging, warm up, swap into production; swap again to roll back.',
      'Traffic routing can send a percentage of requests to a slot first — a canary-style test in production.',
      'Prefer OIDC / workload identity federation to stored passwords for pipeline sign-in.',
      'Build once and deploy the same package everywhere; mind slot-specific settings.'])
    body += saythis('"I use a pipeline in GitHub Actions or Azure Pipelines: every change is built and tested, then deployed to a staging slot, warmed up, and swapped into production — swapping back is my rollback. '
      'For risky changes I route a small share of traffic to the slot first. The pipeline signs in with OpenID Connect so there is no stored secret, and it deploys the Bicep file and the app together."')
    body += trap([
      '<b>Deploying straight to production.</b> Microsoft\'s guidance is to deploy to a non-production slot and swap, so you can validate first and roll back by swapping again.',
      'Second trap: <b>a stored deployment password.</b> It is a long-lived secret that leaks through logs, forks and screenshots. Use short-lived tokens through OIDC.'])
    body += confuse('🔁 Swap (blue-green)', 'Everyone moves to the new version at the same moment, after it has been warmed up and checked.', '🐤 Traffic split (canary)', 'A small share goes to the new version first, so real users test it before everyone does.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># deploy the new version to the staging slot, then swap it into production</span>
az webapp deploy --resource-group rg-shop-prod --name app-shop --slot staging --src-path app.zip
az webapp deployment slot swap --resource-group rg-shop-prod --name app-shop --slot staging --target-slot production''',
      'Illustrative shape only — a real pipeline builds and tests first, and runs these steps with an OIDC sign-in; flags and options can change.'))
    body += next_box('You can now ship changes safely. But apps and pipelines need credentials and settings — database passwords, API keys, feature switches — and hard-coding them is the classic leak. Next: Secrets &amp; Configuration.', None)
    body += fact_note(FOOT, [DOCS_SLOTS, DOCS_BP, DOCS_AP, DOCS_GH, DOCS_TR])
    return page('ci-cd-deployment', 'CI/CD & Deployment Strategies', 'Concept 14 of 19 · 🛠️ Shipping and operating',
        'CI/CD makes every release the same automatic steps — <span class="grad-text">so shipping is routine, and undoing a bad release is one move.</span>',
        'Pipelines, deployment slots, swaps, traffic splits and passwordless sign-in: how to ship to Azure safely and roll back fast.',
        'How would you set up CI/CD to Azure with zero downtime and a safe rollback?',
        body, CR + ['<span class="cur">CI/CD &amp; Deployment</span>'], '', search_title='CI/CD & Deployment Strategies')
