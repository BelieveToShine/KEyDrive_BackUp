from kit import *
from p_common import CR

DOCS_LAM = ('AWS Lambda documentation', 'https://docs.aws.amazon.com/lambda/latest/dg/welcome.html')
DOCS_SFN = ('What is AWS Step Functions?', 'https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html')
DOCS_CHOOSE = ('Choosing workflow type in Step Functions', 'https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html')
DOCS_FL = ('Fargate or Lambda?', 'https://docs.aws.amazon.com/decision-guides/latest/decision-guides/fargate-or-lambda.html')
DOCS_EB = ('Amazon EventBridge documentation', 'https://docs.aws.amazon.com/eventbridge/')
DOCS_INT = ('Choosing an AWS application integration service', 'https://docs.aws.amazon.com/decision-guides/latest/application-integration-on-aws-how-to-choose/application-integration-on-aws-how-to-choose.html')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official AWS docs.'

def d_flow():
    d = Diagram('sv1', 640, 262, 'A file lands in S3, EventBridge routes the event, and a Lambda function or a Step Functions workflow runs in response')
    d.box(10, 100, 110, 62, [('🪣 S3','t'),('a file lands','s')], 'n')
    d.box(200, 100, 120, 62, [('🧭 EventBridge','t'),('routes events','s')], 'emerald')
    d.box(430, 28, 200, 62, [('λ Lambda function','t'),('your code runs','s')], 'amber')
    d.box(430, 172, 200, 62, [('🔀 Step Functions','t'),('a workflow of steps','s')], 'violet')
    d.arrow([(120,131),(200,131)], 'emerald', label='event', at=(160,131))
    d.arrow([(320,131),(375,131),(375,59),(430,59)], 'amber', label='triggers', at=(375,95))
    d.arrow([(320,131),(375,131),(375,203),(430,203)], 'violet', label='triggers', at=(375,167))
    d.arrow([(530,172),(530,90)], 'n', label='calls', at=(530,131))
    return d

def d_choose():
    d = Diagram('sv2', 640, 524, 'Decision tree for serverless tools: EventBridge to route events, Lambda for small code, Step Functions for multi-step workflows, SQS for buffering')
    d.box(190, 8, 260, 34, [('🤔 What is the job?','t')], 'cyan')
    qs = [
     ('🧭 Tell others that something happened?', 'route events by content', 'EventBridge', 'event bus and rules', 'emerald'),
     ('λ A small piece of your own code?', 'runs when something triggers it', 'AWS Lambda', 'functions', 'amber'),
     ('🔀 Many steps, retries, waiting, branching?', 'a process with state', 'Step Functions', 'orchestrate the steps', 'violet'),
     ('📬 Work must wait its turn and survive spikes?', 'buffer in front of the code', 'SQS + Lambda', 'a queue feeds the function', 'cyan'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 460
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 460, 330, 50, [('🤔 Still unsure?','t'),('start with a Lambda function','s')], 'emerald')
    return d

def d_sfn():
    d = Diagram('sv3', 640, 292, 'A Step Functions workflow runs steps in order, in parallel, and retries or branches on failure; the state machine remembers where it is')
    d.box(10, 110, 110, 64, [('▶️ Start','t'),('an event','s')], 'n')
    d.box(200, 110, 120, 64, [('🔀 Workflow','t'),('remembers state','s')], 'violet')
    d.zone(410, 10, 220, 272, 'amber', 'STEPS · in parallel')
    for i in range(3):
        d.box(424, 44 + i*70, 192, 50, [(f'λ Step {i+1}','t'),('one unit of work','s')], 'amber')
    d.arrow([(120,142),(200,142)], 'violet', label='starts', at=(160,142))
    d.arrow([(320,142),(410,142)], 'amber', label='fans out', at=(365,142))
    return d

def build_serverless_orchestration():
    body = ''
    body += see(figure(d_flow(),
        'something happens — a file lands in S3. <b>EventBridge</b> routes that event to whoever cares. One target can be a <b>Lambda</b> function, which runs your own code. Another can be a <b>Step Functions</b> workflow, which runs many steps in order with retries. '
        'A workflow can call functions, so you mix them: workflow for the flow, code for the clever part. None of them needs a server that you keep running.'))
    body += one('Serverless means you give AWS a piece of work and a trigger, and AWS runs it only when the trigger fires — so you pay for work done, not for a server waiting.')
    body += why([
      'Look at what the earlier concepts gave you: an app that scales and is fast, with queues between its parts. But not all work looks like a web app. A file arrives. A timer fires. An order is approved. Between those moments, <b>nothing happens</b>. Keeping a server running just to wait for them is paying for idle capacity.',
      'Serverless flips that. You write a small unit of work, tell AWS what should start it, and AWS supplies the compute when it fires. When there is a lot to do it scales out; when there is nothing, you pay nothing. The skill is picking the right tool for <b>what kind of work</b> it is: reacting, coding, or orchestrating many steps.'])
    body += block('🧰 The tools', pick_cards([
      dict(icon='λ', name='AWS Lambda', tag='functions that run on a trigger', color='#fbbf24',
           use=['Event-driven work: a file, a message, a timer, an API call', 'Short, bursty tasks where you pay while it runs', 'Fed by queues, streams, topics and event buses'],
           skip=['Long-running steady services — a container service fits better']),
      dict(icon='🔀', name='AWS Step Functions', tag='workflow orchestration', color='#a78bfa',
           use=['Several steps in order, in parallel, with retries and branches', 'Standard workflows: long-running, durable, auditable; exactly-once execution', 'Express workflows: high-rate, short (up to five minutes), at-least-once'],
           skip=['A single quick action — a Lambda function is enough']),
      dict(icon='🧭', name='Amazon EventBridge', tag='routes events by content', color='#34d399',
           use=['React to AWS and SaaS events without polling', 'One event, many targets'],
           skip=['You need ordering guarantees — it does not provide them']),
      dict(icon='📬', name='SQS in front of Lambda', tag='a buffer between event and code', color='#22d3ee',
           use=['Absorb spikes so the function is not overwhelmed', 'Retry and dead-letter failed messages'],
           skip=['Work that must start instantly with no queue']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'read from the top and stop at the first "yes". <b>Tell others something happened?</b> EventBridge. <b>Small code?</b> Lambda. <b>Many steps with retries and waiting?</b> Step Functions. <b>Work must wait its turn?</b> A queue in front of the function. '
        'AWS\'s own guide says the same: Lambda suits short, bursty tasks better than long-running services — for those, containers on Fargate fit better.'), label_cls='see')
    body += block('🔀 What "orchestration" looks like', figure(d_sfn(),
        'a Step Functions <b>workflow</b> (a state machine) is the conductor. It does not do the work; it starts <b>steps</b> — often Lambda functions — here in parallel, and tracks where the process is. If a step fails it can <b>retry</b> or branch. '
        'The two workflow types differ: <b>Standard</b> is durable and exactly-once for long, auditable processes (and non-repeatable actions such as taking a payment); <b>Express</b> is for high-volume, short, repeatable work. The type cannot be changed after you create the workflow.'), label_cls='see')
    body += block('📊 Standard vs Express workflows', table(['','Standard','Express'], [
      ['Good for','Long-running, durable, auditable','High-volume, short event processing'],
      ['Duration','Long','Up to five minutes'],
      ['Execution','Exactly-once','At-least-once (async); design for repeats'],
      ['Best with','Actions that must not repeat, such as payments','Repeatable actions, such as writing a record'],
      ['History','Recorded by Step Functions','Via CloudWatch Logs, best-effort'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🖼️','A photo is uploaded','Make a thumbnail. Idle most of the day.','EventBridge or an S3 event + Lambda'),
      ('⏰','Every night at 2 AM','Clean old records. Runs for a minute.','A scheduled Lambda function'),
      ('✅','An order needs payment, stock, shipping, notification','Steps, retries, a wait for approval.','Step Functions (Standard)'),
      ('📊','Thousands of events a second to transform','Short, repeatable steps.','Step Functions Express, or Lambda directly'),
      ('📬','A spike of image jobs','Do not overload the function.','SQS in front of Lambda'),
      ('🏗️','A steady API busy all day','High, even traffic.','Containers rather than Lambda'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — habits that keep serverless safe', '''      <p><b>Be idempotent.</b> Events and messages can arrive more than once and retries happen. Design the work so doing it twice is safe — especially with Express workflows and EventBridge targets, which are at-least-once.</p>
      <p><b>Keep functions short and stateless.</b> Anything that must be remembered between steps belongs in a database, in storage, or in the workflow\'s state — not in the function\'s memory.</p>
      <p><b>Cold starts.</b> When nothing is warm, a new execution environment must start first, adding a delay. Check the Lambda documentation for the ways to reduce it that suit you.</p>
      <p><b>Use the execution role.</b> A Lambda function gets its permissions from an IAM role (concept 3) — give it only what it needs, and keep secrets in a secrets service (concept 15).</p>''')
    body += recall([
      'Serverless = you supply the work and the trigger; AWS supplies compute only while it runs.',
      'EventBridge routes events; Lambda runs code; Step Functions orchestrates multi-step work with retries and state.',
      'Standard workflows: long, durable, exactly-once. Express: up to five minutes, high rate, at-least-once. The type is fixed after creation.',
      'Lambda fits short, bursty tasks; steady long-running services fit containers better.',
      'Put SQS in front of a function to absorb spikes; make work idempotent.'])
    body += saythis('"Serverless means I provide the code or workflow and a trigger, and AWS runs it only when needed. EventBridge routes events, Lambda runs my own code, and Step Functions orchestrates multi-step work with retries — Standard for long, durable, exactly-once flows, Express for short, high-volume ones. '
      'I put a queue in front of Lambda for spikes, and I make the work idempotent."')
    body += trap([
      '<b>"Serverless" does not mean "no servers" — and it is not always the right tool.</b> A steady, long-running service may fit a container service better than short-lived functions.',
      'Second trap: <b>using Express workflows for work that must never repeat.</b> Express is at-least-once; for payments and other non-repeatable actions use Standard.'])
    body += confuse('λ Lambda', 'You write the code. One function, one trigger; great for small, event-driven work.', '🔀 Step Functions', 'You design the flow of many steps, with retries, branches and waiting; steps are often Lambda functions.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># create a small Lambda function from a zip file; it needs an execution role</span>
aws lambda create-function --function-name make-thumbnail --runtime python3.12 \\
    --role &lt;execution-role-arn&gt; --handler app.handler --zip-file fileb://function.zip''',
      'Illustrative shape only — the runtime version, role and handler are examples, and supported runtimes change over time.'))
    body += next_box('Your system now has many parts: apps, databases, networks, functions, workflows. Clicking them together in the console is slow and cannot be repeated or reviewed. Next: Infrastructure as Code.', 'infrastructure-as-code.html', 'Infrastructure as Code')
    body += fact_note(FOOT, [DOCS_LAM, DOCS_SFN, DOCS_CHOOSE, DOCS_FL, DOCS_EB, DOCS_INT])
    return page('serverless-orchestration', 'Serverless & Orchestration', 'Concept 12 of 19 · ⚙️ Handling load',
        'Serverless runs your work only when something triggers it — <span class="grad-text">so you pay for work done, not for a server waiting.</span>',
        'EventBridge, Lambda and Step Functions: what each is for, how they work together, and how to choose.',
        'When would you use Lambda, Step Functions or EventBridge?',
        body, CR + ['<span class="cur">Serverless &amp; Orchestration</span>'], '', search_title='Serverless & Orchestration')
