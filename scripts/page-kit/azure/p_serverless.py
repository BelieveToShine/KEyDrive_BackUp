from kit import *
from p_storage import CR

DOCS_FNS = ('Azure Functions hosting options', 'https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale')
DOCS_FLEX = ('Flex Consumption plan', 'https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-plan')
DOCS_DUR = ('Durable Functions overview', 'https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview')
DOCS_LA = ('Azure Logic Apps overview', 'https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview')
DOCS_CMP = ('Integration and automation options in Azure', 'https://learn.microsoft.com/en-us/azure/azure-functions/functions-compare-logic-apps-ms-flow-webjobs')
DOCS_EG = ('Azure Event Grid documentation', 'https://learn.microsoft.com/en-us/azure/event-grid/overview')
FOOT = 'Cloud services change often — hosting plans especially. This page teaches the ideas; for current plans, limits and prices, check the official docs.'

def d_flow():
    d = Diagram('sv1', 640, 262, 'An event is routed by Event Grid to a Function or a Logic App, and a Logic App can call a Function')
    d.box(10, 100, 110, 62, [('📁 Source','t'),('a file lands','s')], 'n')
    d.box(200, 100, 120, 62, [('📣 Event Grid','t'),('routes events','s')], 'cyan')
    d.box(430, 28, 200, 62, [('⚡ Azure Function','t'),('your own code runs','s')], 'amber')
    d.box(430, 172, 200, 62, [('🔀 Logic App','t'),('designer-built workflow','s')], 'violet')
    d.arrow([(120,131),(200,131)], 'cyan', label='event', at=(160,131))
    d.arrow([(320,131),(375,131),(375,59),(430,59)], 'amber', label='triggers', at=(375,95))
    d.arrow([(320,131),(375,131),(375,203),(430,203)], 'violet', label='triggers', at=(375,167))
    d.arrow([(530,172),(530,90)], 'n', label='can call', at=(530,131))
    return d

def d_choose():
    d = Diagram('sv2', 640, 620, 'Decision tree for serverless tools: Event Grid, Functions, Logic Apps, Durable Functions or Service Bus')
    d.box(190, 8, 260, 34, [('🤔 What is the job?','t')], 'cyan')
    qs = [
     ('📣 Tell others that something happened?', 'a file landed, a resource changed', 'Event Grid', 'routes the event', 'cyan'),
     ('⚡ A small piece of your own code?', 'runs when something triggers it', 'Azure Functions', 'code-first', 'amber'),
     ('🔀 Connect many systems, little code?', 'approvals, emails, SaaS tools', 'Logic Apps', 'designer-first', 'violet'),
     ('🎼 Many steps in code that must survive?', 'chains, parallel work, waiting', 'Durable Functions', 'code that remembers', 'emerald'),
     ('📨 Strict order, transactions, safe retry?', 'money, orders, reliable hand-off', 'Service Bus', 'see Messaging', 'n'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 560
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 560, 330, 50, [('🤔 Still unsure?','t'),('start with a Function and grow from there','s')], 'emerald')
    return d

def d_durable():
    d = Diagram('sv3', 640, 292, 'A Durable Functions orchestrator starts several activities in parallel and combines their results')
    d.box(10, 100, 120, 70, [('🎼 Orchestrator','t'),('remembers progress','s')], 'emerald')
    d.zone(220, 12, 210, 240, 'amber', 'ACTIVITIES · in parallel')
    for i in range(3):
        d.box(234, 44 + i*68, 182, 48, [(f'⚡ Activity {i+1}','t'),('one unit of work','s')], 'amber')
    d.box(540, 100, 90, 70, [('🧮 Combined','t'),('result','t')], 'cyan')
    d.arrow([(130,135),(220,135)], 'emerald', label='fan out', at=(175,135))
    d.arrow([(430,135),(540,135)], 'cyan', label='fan in', at=(485,135))
    d.text(320, 278, 'The orchestrator saves a checkpoint as it goes, so a restart does not lose its place.', size=9.5, weight=700)
    return d

def build_serverless_orchestration():
    body = ''
    body += see(figure(d_flow(),
        'something happens — a file lands in storage. <b>Event Grid</b> routes that event to whoever cares. One handler can be an <b>Azure Function</b>, which runs your own code. Another can be a <b>Logic App</b>, a workflow built in a designer. '
        'A Logic App can also call a Function, and the other way round — so you mix them: workflow for the glue, code for the clever part. None of them needs a server that you keep running.'))
    body += one('Serverless means you give Azure a piece of work and a trigger, and Azure runs it only when the trigger fires — so you pay for work done, not for a machine waiting.')
    body += why([
      'Look at what the earlier concepts gave you: an app that scales and is fast. But not all work looks like a web app. A file arrives. A timer fires. An order is approved. Between those moments, <b>nothing happens</b>. Keeping a server running just to wait for them is paying for idle capacity.',
      'Serverless flips that. You write a small unit of work, tell Azure what should start it, and Azure supplies the compute when it fires. When there is a lot to do it scales out; when there is nothing, it can scale to zero. The skill is picking the right tool for <b>what kind of work</b> it is: reacting, coding, connecting, or orchestrating many steps.'])
    body += block('🧰 The four tools', pick_cards([
      dict(icon='📣', name='Event Grid', tag='routes "something happened" events', color='#22d3ee',
           use=['React to changes without polling', 'One event, many interested handlers', 'Azure service and SaaS events'],
           skip=['You need strict order, transactions or duplicate detection → Service Bus']),
      dict(icon='⚡', name='Azure Functions', tag='small code, run on a trigger', color='#fbbf24',
           use=['Your own logic: transform data, call an API, run a job', 'HTTP, timer, queue, event and storage triggers', 'Unique data transformations and utility code'],
           skip=['Long, multi-step flows in plain functions — use Durable Functions']),
      dict(icon='🔀', name='Logic Apps', tag='workflows built in a designer', color='#a78bfa',
           use=['Connect many systems with prebuilt connectors', 'Business processes, approvals, notifications', 'Little or no code'],
           skip=['Heavy custom code or tight performance work → a Function']),
      dict(icon='🎼', name='Durable Functions', tag='code-based orchestration', color='#34d399',
           use=['Several steps in order, or in parallel then combined', 'Work that waits and must survive restarts', 'You prefer to write the flow as code'],
           skip=['A single quick action — a plain Function is enough']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'read from the top and stop at the first "yes". The questions run from <b>telling others</b> (Event Grid), to <b>small code</b> (Functions), to <b>connecting systems</b> (Logic Apps), to <b>code with many steps</b> (Durable Functions). '
        'The last row is a hand-off: when order, transactions and safe retries matter, you want a message broker — that is Service Bus from the Messaging concept. Microsoft also notes these tools are often combined.'), label_cls='see')
    body += block('🎼 What "orchestration" looks like', figure(d_durable(),
        'in Durable Functions the <b>orchestrator</b> is the conductor. It does not do the work; it starts <b>activities</b> (single units of work), here in parallel (<em>fan-out</em>), then waits and combines the answers (<em>fan-in</em>). '
        'The orchestrator checkpoints its progress, so if the host restarts it picks up where it left off. The other common pattern is <em>function chaining</em>: run activity A, pass its output to B, then to C.'), label_cls='see')
    body += block('📊 Functions: which hosting plan?', table(['Plan','How it scales','Good for','Watch out for'], [
      ['Flex Consumption','Event-driven, can scale to zero; Microsoft\'s recommended serverless plan for new apps','New serverless apps; optional always-ready instances to reduce start delay','Code deployments are Linux-only'],
      ['Premium','Event-driven with pre-warmed workers; at least one instance stays running','Apps that run continuously, or nearly so','You pay for the warm capacity'],
      ['Dedicated (App Service)','Does not scale on events — a set number of instances','Spare App Service capacity, steady work','No event-driven scale-out'],
      ['Consumption (legacy)','Event-driven, scales to zero','Existing apps','Microsoft recommends moving to Flex Consumption'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🖼️','A photo is uploaded','Make a thumbnail. Idle most of the day, busy in bursts.','Event Grid + a Function'),
      ('⏰','Every night at 2 AM','Clean up old records. It runs for a minute, then nothing.','A timer-triggered Function'),
      ('✅','New hire onboarding','Notify HR, create accounts in three SaaS tools, wait for approval.','Logic Apps'),
      ('🧬','Process 500 files in parallel','Then build one summary report from all the results.','Durable Functions (fan-out / fan-in)'),
      ('💳','Process a payment order','Order matters, and a message must never be lost or doubled.','Service Bus (not Event Grid)'),
      ('🔗','Workflow with one smart step','Mostly connectors, but one step needs custom code.','Logic App calling a Function'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — habits that keep serverless safe', '''      <p><b>Triggers and bindings.</b> A Function starts from a <i>trigger</i> (a message, a timer, an HTTP call) and can read or write other services through <i>bindings</i>, so you write less plumbing code.</p>
      <p><b>Cold start.</b> When nothing is running and a trigger fires, the platform must start an instance first, which adds a delay. Plans differ: Flex Consumption can keep always-ready instances, Premium keeps pre-warmed workers, and Dedicated runs continuously. Pick based on how much delay the user can accept.</p>
      <p><b>Be idempotent.</b> Events and messages can arrive more than once, and retries happen. Design the work so doing it twice is safe.</p>
      <p><b>Keep functions short and stateless.</b> Anything that needs to remember something between steps belongs in a database, storage, or a Durable Functions orchestrator — not in the function\'s memory.</p>
      <p><b>Use managed identity</b> (concept 3) so a Function can reach storage, databases and other services without secrets in its settings.</p>''')
    body += recall([
      'Serverless = you supply the work and the trigger; Azure supplies compute only while it runs, and it can scale to zero.',
      'Event Grid routes events. Functions = code-first. Logic Apps = designer-first with many connectors. Durable Functions = code-based orchestration that checkpoints progress.',
      'Fan-out/fan-in = start activities in parallel then combine; function chaining = run steps in order.',
      'Flex Consumption is the recommended serverless plan for new Functions apps; Premium keeps pre-warmed workers; Dedicated does not scale on events.',
      'Need order, transactions or duplicate detection → Service Bus, not Event Grid.'])
    body += saythis('"Serverless means I provide the code or workflow and a trigger, and Azure runs it only when needed. Event Grid routes events, Functions run my own code, Logic Apps connect systems with a designer, and Durable Functions orchestrate multi-step work in code with checkpoints. '
      'For new Functions apps I start with the Flex Consumption plan, and I make the work idempotent. When I need ordering or transactions I use Service Bus instead."')
    body += trap([
      '<b>"Serverless" does not mean "no servers" — and it is not always the right tool.</b> There are still servers; you just do not manage them. Long-running, steady, heavy work may fit a plan with always-on capacity better than one built for short bursts.',
      'Second trap: <b>using Event Grid where you need guarantees.</b> Event Grid routes events; it does not give ordering, transactions or duplicate detection. When losing or reordering a message would hurt, use Service Bus.'])
    body += confuse('⚡ Azure Functions', 'You write code. Great for custom logic and transformations; you decide how it is structured.', '🔀 Logic Apps', 'You design a workflow with connectors. Great for gluing systems together with little code.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># create a Function app on the Flex Consumption plan — Azure runs it only when triggered</span>
az functionapp create --name func-thumbs --resource-group rg-shop-prod \\
    --flexconsumption-location westeurope --runtime python --runtime-version 3.11 \\
    --storage-account stfuncthumbs''',
      'Illustrative shape only — real setups also add identity, networking and deployment, and the flags and supported runtimes change.'))
    body += next_box('Your system now has many parts: apps, databases, networks, functions, workflows. Clicking them together in the portal is slow and cannot be repeated or reviewed. Next: Infrastructure as Code.', 'infrastructure-as-code.html', 'Infrastructure as Code')
    body += fact_note(FOOT, [DOCS_FNS, DOCS_FLEX, DOCS_DUR, DOCS_LA, DOCS_CMP, DOCS_EG])
    return page('serverless-orchestration', 'Serverless & Orchestration', 'Concept 12 of 19 · ⚙️ Handling load',
        'Serverless runs your work only when something triggers it — <span class="grad-text">so you pay for work done, not for a machine waiting.</span>',
        'Event Grid, Azure Functions, Logic Apps and Durable Functions: what each one is for, how they work together, and how to choose.',
        'When would you use Azure Functions, Logic Apps, Durable Functions or Event Grid?',
        body, CR + ['<span class="cur">Serverless &amp; Orchestration</span>'], '', search_title='Serverless & Orchestration')
