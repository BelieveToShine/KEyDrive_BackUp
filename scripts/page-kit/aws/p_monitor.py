from kit import *
from p_common import CR

DOCS_CHOOSE = ('Choosing an AWS monitoring and observability service', 'https://docs.aws.amazon.com/decision-guides/latest/monitoring-on-aws-how-to-choose/monitoring-on-aws-how-to-choose.html')
DOCS_CTCW = ('AWS CloudTrail or Amazon CloudWatch?', 'https://docs.aws.amazon.com/decision-guides/latest/cloudtrail-or-cloudwatch/cloudtrail-or-cloudwatch.html')
DOCS_CW = ('Amazon CloudWatch documentation', 'https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html')
DOCS_XR = ('AWS X-Ray documentation', 'https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html')
DOCS_CT = ('AWS CloudTrail documentation', 'https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html')
DOCS_TOOLS = ('AWS observability tools', 'https://docs.aws.amazon.com/wellarchitected/latest/management-and-governance-guide/aws-observability-tools.html')
FOOT = 'Monitoring features change often. This page teaches the ideas; for current features and prices, check the official AWS docs.'

def d_signals():
    d = Diagram('mo1', 640, 330, 'Metrics, logs and traces flow into CloudWatch and X-Ray, where you can query, alarm and visualize them')
    d.box(10, 44, 130, 62, [('📈 Metrics','t'),('numbers over time','s')], 'cyan')
    d.box(10, 134, 130, 62, [('📜 Logs','t'),('events with detail','s')], 'violet')
    d.box(10, 224, 130, 62, [('🧵 Traces','t'),('one request\'s path','s')], 'amber')
    d.box(300, 44, 120, 242, [('📡 CloudWatch','t'),('and X-Ray','t'),('one place for','s'),('every signal','s')], 'emerald')
    d.arrow([(140,75),(300,75)], 'cyan', label='automatic', at=(220,75))
    d.arrow([(140,165),(300,165)], 'violet', label='sent by you', at=(220,165))
    d.arrow([(140,255),(300,255)], 'amber', label='instrumented', at=(220,255))
    d.box(510, 44, 120, 62, [('🔍 Query','t'),('Logs Insights','s')], 'n')
    d.box(510, 134, 120, 62, [('🚨 Alarms','t'),('notify or act','s')], 'n')
    d.box(510, 224, 120, 62, [('🗺️ Maps','t'),('see the flow','s')], 'n')
    d.arrow([(420,75),(510,75)], 'emerald', label='ask', at=(465,75))
    d.arrow([(420,165),(510,165)], 'emerald', label='notify', at=(465,165))
    d.arrow([(420,255),(510,255)], 'emerald', label='show', at=(465,255))
    return d

def d_alarm():
    d = Diagram('mo2', 640, 272, 'A CloudWatch alarm watches a metric and when it crosses its threshold it triggers an action such as a notification or automation')
    d.box(10, 40, 110, 60, [('📊 Metric','t'),('CPU, queue age','s')], 'cyan')
    d.box(230, 40, 130, 60, [('🚨 Alarm','t'),('threshold + period','s')], 'amber')
    d.box(480, 40, 150, 60, [('🔔 Action','t'),('who or what to call','s')], 'violet')
    d.arrow([(120,70),(230,70)], 'cyan', label='watched by', at=(175,70))
    d.arrow([(360,70),(480,70)], 'amber', label='fires', at=(420,70))
    d.box(230, 176, 120, 52, [('✉️ A person','t'),('notification','s')], 'n')
    d.box(360, 176, 120, 52, [('⚡ Automation','t'),('Lambda, scaling','s')], 'emerald')
    d.box(490, 176, 120, 52, [('🎫 A ticket','t'),('or runbook','s')], 'n')
    d.arrow([(555,100),(555,138),(290,138),(290,176)], 'violet', label='notifies', at=(330,138))
    d.arrow([(555,100),(555,138),(420,138),(420,176)], 'emerald', label='runs', at=(470,138))
    d.arrow([(555,100),(555,176)], 'violet', label='opens', at=(555,119))
    d.text(320, 256, 'Every alarm needs an owner who acts on it — otherwise it becomes noise.', size=9.5, weight=700)
    return d

def d_choose():
    d = Diagram('mo3', 640, 524, 'Decision tree: which question needs which AWS monitoring service')
    d.box(190, 8, 260, 34, [('🤔 What do you need to know?','t')], 'cyan')
    qs = [
     ('🧑‍💻 Where is this request slow or failing?', 'across several services', 'X-Ray', 'distributed traces', 'amber'),
     ('📜 What did a resource do, in detail?', 'application and system logs', 'CloudWatch Logs', 'search with Logs Insights', 'violet'),
     ('📈 Is a number out of range right now?', 'CPU, latency, queue age', 'Metrics + alarm', 'CloudWatch', 'cyan'),
     ('🕵️ Who made this change, and when?', 'API calls in the account', 'CloudTrail', 'audit and compliance', 'emerald'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 460
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 460, 330, 50, [('🤔 Still unsure?','t'),('start with metrics, then add logs','s')], 'emerald')
    return d

def build_monitoring_observability():
    body = ''
    body += see(figure(d_signals(),
        'three kinds of signal flow into one place. <b>Metrics</b> are numbers over time (is CPU high?). <b>Logs</b> are detailed records of what happened. <b>Traces</b> follow one request through the parts of your app. '
        'In AWS that is <b>CloudWatch</b> for metrics, logs and alarms and <b>X-Ray</b> for traces. Once they are together you can <b>query</b> them, <b>alarm</b> on them and see the <b>map</b> of what talks to what.'))
    body += one('Monitoring tells you something is wrong; observability lets you work out why — and both need metrics, logs and traces gathered in one place before the incident.')
    body += why([
      'Guardrails say what <i>should</i> happen. They do not tell you what <i>did</i> happen. The app is fast today and slower next week; a deployment looks fine and customers still see errors; the bill climbs and nobody knows which part grew. Without signals, every problem becomes guessing.',
      'The skill is deciding <b>what to collect before you need it</b>. Metrics answer "is something off?". Logs answer "what exactly happened?". Traces answer "where did this one request spend its time?". And a fourth source, <b>CloudTrail</b>, answers "who changed what?". Then <b>alarms</b> turn signals into action.'])
    body += block('🧰 The pieces', pick_cards([
      dict(icon='📡', name='Amazon CloudWatch', tag='metrics, logs and alarms', color='#34d399',
           use=['The main monitoring and observability service for metrics, logs and alarms', 'Logs Insights to query logs', 'Service Map and dashboards to see the flow'],
           skip=['Auditing who made API calls — that is CloudTrail']),
      dict(icon='🧵', name='AWS X-Ray', tag='distributed tracing', color='#fbbf24',
           use=['An end-to-end view of a request as it travels through your application', 'A map of the underlying components'],
           skip=['Only watching a single server — add metrics and logs too']),
      dict(icon='🕵️', name='AWS CloudTrail', tag='API activity for audit', color='#a78bfa',
           use=['Who made a call, when, and which resources were affected', 'Compliance and investigations', 'Event history covers recent management events by default'],
           skip=['Watching performance — use CloudWatch']),
      dict(icon='🚨', name='CloudWatch alarms', tag='turn a signal into action', color='#fb7185',
           use=['Alarm on a metric crossing a threshold', 'Notify people or start automation, such as scaling'],
           skip=['Alarm on everything — people will start ignoring them']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'start from the <b>question</b>, not the tool. Slow or failing across services? <b>X-Ray</b>. What did a resource do in detail? <b>CloudWatch Logs</b>. A number out of range? <b>A metric and an alarm</b>. Who changed this? <b>CloudTrail</b>. '
        'AWS\'s decision guide sums up the split: CloudTrail is for auditing and compliance; CloudWatch is for monitoring operational health and performance.'), label_cls='see')
    body += block('🔔 From signal to action', figure(d_alarm(),
        'an <b>alarm</b> watches a metric against a threshold over a period. When the condition is met it triggers an <b>action</b>: notify a person, run automation (for example, scaling or a function) or open a ticket. '
        'You already saw this loop in Scaling &amp; Resilience, where a metric drives Auto Scaling.'), label_cls='see')
    body += block('📊 Metrics, logs, traces and audit', table(['','Answers','Looks like','Service'], [
      ['📈 Metrics','Is something off, and since when?','Numbers in a time series','CloudWatch'],
      ['📜 Logs','What exactly happened?','Records with fields, searched with Logs Insights','CloudWatch Logs'],
      ['🧵 Traces','Where did this request go and slow down?','A request followed across services','X-Ray'],
      ['🕵️ Audit','Who changed what, when?','A record of API calls','CloudTrail'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🐢','Checkout feels slow since Tuesday','Which call inside the request takes the time?','X-Ray traces'),
      ('📉','CPU on the web tier keeps spiking','Know about it before users do.','Metric alarm + action'),
      ('🔍','A firewall rule blocked a partner','What exactly was denied, and when?','CloudWatch Logs'),
      ('🕵️','A setting changed overnight','Find out who changed it.','CloudTrail'),
      ('🧯','A disk is almost full','Fix it before the app stops.','Alarm that triggers automation'),
      ('🏗️','Every new resource must send logs','Do not rely on people remembering.','Build it into the infrastructure template'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — habits and traps', '''      <p><b>Three data types.</b> AWS frames observability around logs, metrics and traces. CloudWatch collects metrics and logs; X-Ray provides traces; CloudWatch Service Map and the X-Ray trace map show how services connect.</p>
      <p><b>CloudTrail is audit.</b> It records API activity — who, when and what — and the default event history shows recent management events for your account. Create a trail if you need longer retention.</p>
      <p><b>Decide what to collect before the incident.</b> The one time you need a log is the time it was not turned on. Build logging into your infrastructure templates (concept 13).</p>
      <p><b>Keep monitoring itself monitored.</b> Send security findings (concept 16) to the same place, and alarm when something important turns off. Logs are billed by volume, so collect what you will use (Cost Management is next).</p>''')
    body += recall([
      'Three signals: metrics, logs, traces. CloudWatch = metrics, logs, alarms; X-Ray = traces; CloudTrail = audit of API calls.',
      'CloudTrail for audit and compliance; CloudWatch for operational health and performance.',
      'Alarm = metric + threshold + period → action (notify, automate, ticket).',
      'Logs Insights queries logs; Service Map and the X-Ray map show the flow.',
      'Decide what to collect before the incident; alarms without an owner become noise.'])
    body += saythis('"I collect metrics, logs and traces: CloudWatch for metrics, logs and alarms, X-Ray for distributed traces, and CloudTrail for the audit trail of API calls. '
      'I alarm on symptoms users feel and drive action from the alarms, and I build logging into the infrastructure templates so nothing is forgotten."')
    body += trap([
      '<b>Mixing up CloudWatch and CloudTrail.</b> CloudWatch tells you how the system is performing; CloudTrail tells you who did what. You need both.',
      'Second trap: <b>an alarm for everything.</b> A flood of alarms trains people to ignore them. Alarm on symptoms users feel, give each alarm an owner, and use dashboards for the rest.'])
    body += confuse('📈 CloudWatch', 'How is the system performing right now? Metrics, logs and alarms.', '🕵️ CloudTrail', 'Who did what, and when? A record of API activity for audit and investigation.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># an alarm that fires when average CPU stays high; it notifies an SNS topic</span>
aws cloudwatch put-metric-alarm --alarm-name shop-cpu-high --metric-name CPUUtilization \\
    --namespace AWS/EC2 --statistic Average --period 300 --threshold 80 \\
    --comparison-operator GreaterThanThreshold --evaluation-periods 2 --alarm-actions &lt;topic-arn&gt;''',
      'Illustrative shape only — the metric, threshold and periods are examples and must match your workload.'))
    body += next_box('You can now see what your system does. Everything above is also <b>metered</b> — and a good design can still be an unaffordable one. Next: Cost Management.', 'cost-management.html', 'Cost Management')
    body += fact_note(FOOT, [DOCS_CHOOSE, DOCS_CTCW, DOCS_CW, DOCS_XR, DOCS_CT, DOCS_TOOLS])
    return page('monitoring-observability', 'Monitoring & Observability', 'Concept 17 of 19 · 🛠️ Shipping and operating',
        'Monitoring tells you something is wrong; observability helps you find why — <span class="grad-text">but only if you collected the signals before the incident.</span>',
        'CloudWatch, X-Ray and CloudTrail: metrics, logs, traces and audit, plus alarms that turn signals into action.',
        'How would you monitor an AWS application and get alerted before users notice?',
        body, CR + ['<span class="cur">Monitoring &amp; Observability</span>'], '', search_title='Monitoring & Observability')
