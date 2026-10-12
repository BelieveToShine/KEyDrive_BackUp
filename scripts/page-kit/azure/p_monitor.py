from kit import *
from p_storage import CR

DOCS_AM = ('Azure Monitor overview', 'https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview')
DOCS_AI = ('Application Insights overview', 'https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview')
DOCS_LOGS = ('Azure Monitor Logs overview', 'https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-platform-logs')
DOCS_DS = ('Diagnostic settings', 'https://learn.microsoft.com/en-us/azure/azure-monitor/platform/diagnostic-settings')
DOCS_AL = ('Azure Monitor alerts overview', 'https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview')
DOCS_MET = ('Metrics in Azure Monitor', 'https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/data-platform-metrics')
FOOT = 'Monitoring features change often, and some OpenTelemetry paths are still in preview. This page teaches the ideas; for current features and prices, check the official docs.'

def d_signals():
    d = Diagram('mo1', 640, 330, 'Metrics, logs and traces flow into Azure Monitor, where you can query them, alert on them and chart them')
    d.box(10, 44, 130, 62, [('📈 Metrics','t'),('numbers over time','s')], 'cyan')
    d.box(10, 134, 130, 62, [('📜 Logs','t'),('events with detail','s')], 'violet')
    d.box(10, 224, 130, 62, [('🧵 Traces','t'),('one request\'s path','s')], 'amber')
    d.box(300, 44, 120, 242, [('📡 Azure','t'),('Monitor','t'),('one place for','s'),('every signal','s')], 'emerald')
    d.arrow([(140,75),(300,75)], 'cyan', label='automatic', at=(220,75))
    d.arrow([(140,165),(300,165)], 'violet', label='diagnostic setting', at=(220,165))
    d.arrow([(140,255),(300,255)], 'amber', label='instrumented', at=(220,255))
    d.box(510, 44, 120, 62, [('🔍 Query','t'),('KQL, logs','s')], 'n')
    d.box(510, 134, 120, 62, [('🚨 Alerts','t'),('notify or fix','s')], 'n')
    d.box(510, 224, 120, 62, [('📊 Charts','t'),('see it at a glance','s')], 'n')
    d.arrow([(420,75),(510,75)], 'emerald', label='ask', at=(465,75))
    d.arrow([(420,165),(510,165)], 'emerald', label='notify', at=(465,165))
    d.arrow([(420,255),(510,255)], 'emerald', label='show', at=(465,255))
    return d

def d_alert():
    d = Diagram('mo2', 640, 272, 'An alert rule watches a signal; when its condition is met it fires an action group, which notifies people, runs automation or opens a ticket')
    d.box(10, 40, 110, 60, [('📊 Signal','t'),('metric or log','s')], 'cyan')
    d.box(230, 40, 130, 60, [('🚨 Alert rule','t'),('condition + window','s')], 'amber')
    d.box(480, 40, 150, 60, [('🔔 Action group','t'),('who or what to call','s')], 'violet')
    d.arrow([(120,70),(230,70)], 'cyan', label='watched by', at=(175,70))
    d.arrow([(360,70),(480,70)], 'amber', label='fires', at=(420,70))
    d.box(230, 176, 120, 52, [('✉️ A person','t'),('email, SMS, push','s')], 'n')
    d.box(360, 176, 120, 52, [('⚡ Automation','t'),('Function, Logic App','s')], 'emerald')
    d.box(490, 176, 120, 52, [('🎫 A ticket','t'),('ITSM incident','s')], 'n')
    d.arrow([(555,100),(555,138),(290,138),(290,176)], 'violet', label='notifies', at=(330,138))
    d.arrow([(555,100),(555,138),(420,138),(420,176)], 'emerald', label='runs', at=(470,138))
    d.arrow([(555,100),(555,176)], 'violet', label='opens', at=(555,119))
    d.text(320, 256, 'Every alert needs an owner who acts on it — otherwise it becomes noise.', size=9.5, weight=700)
    return d

def d_choose():
    d = Diagram('mo3', 640, 524, 'Decision tree: which question needs which Azure Monitor tool')
    d.box(190, 8, 260, 34, [('🤔 What do you need to know?','t')], 'cyan')
    qs = [
     ('🧑‍💻 Is the app slow or failing for users?', 'requests, errors, dependencies, traces', 'Application Insights', 'app performance', 'amber'),
     ('📜 What did a resource do, in detail?', 'needs its resource logs turned on', 'Log Analytics', 'query logs with KQL', 'violet'),
     ('📈 Is a number out of range right now?', 'CPU, queue length, latency', 'Metrics + alert', 'collected automatically', 'cyan'),
     ('🕵️ Who changed this resource?', 'create, update, delete operations', 'Activity log', 'collected automatically', 'emerald'),
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
        'three kinds of signal flow into one place, <b>Azure Monitor</b>. <b>Metrics</b> are numbers over time (is CPU high?). <b>Logs</b> are detailed records of what happened. <b>Traces</b> follow one request through the parts of your app. '
        'Once they are together you can <b>query</b> them, <b>alert</b> on them and <b>chart</b> them. Note the labels: metrics arrive by themselves, logs need a diagnostic setting turned on, and traces need your app to be instrumented.'))
    body += one('Monitoring tells you something is wrong; observability lets you work out why — and both need metrics, logs and traces gathered in one place before the incident.')
    body += why([
      'Guardrails say what <i>should</i> happen. They do not tell you what <i>did</i> happen. The app is fast today and slower next week; a deployment looks fine and customers still see errors; the cost climbs and nobody knows which part grew. Without signals, every problem becomes guessing.',
      'The skill is deciding <b>what to collect before you need it</b>. Metrics answer "is something off?". Logs answer "what exactly happened?". Traces answer "where did this one request spend its time?". Then <b>alerts</b> turn the signals into action, so a person (or an automatic fix) hears about trouble before the customers do.'])
    body += block('🧰 The pieces', pick_cards([
      dict(icon='📡', name='Azure Monitor', tag='the platform for all signals', color='#34d399',
           use=['Metrics, logs, traces and events in one service', 'Platform metrics and the activity log are collected automatically', 'Alerts, dashboards and workbooks on top'],
           skip=['Nothing — it is the base for the rest']),
      dict(icon='🔎', name='Log Analytics', tag='query logs with KQL', color='#a78bfa',
           use=['Search and join logs from many resources', 'Resource logs, after you create a diagnostic setting', 'Investigate an incident after the fact'],
           skip=['Resource logs are not collected until you turn them on']),
      dict(icon='🧑‍💻', name='Application Insights', tag='application performance monitoring', color='#fbbf24',
           use=['Requests, failures, dependencies and traces inside your app', 'Instrument with OpenTelemetry, a vendor-neutral framework', 'Distributed tracing across services'],
           skip=['Only watching the VM or the platform — add resource metrics and logs too']),
      dict(icon='🚨', name='Alerts and action groups', tag='turn a signal into action', color='#fb7185',
           use=['Metric, log and activity-log alerts', 'Action groups: email, SMS, push, automation runbooks, Functions, Logic Apps, ITSM tickets, webhooks'],
           skip=['Alert on everything — people will start ignoring them']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'start from the <b>question</b>, not the tool. If users report slowness or errors, look at <b>Application Insights</b>. If you need detail about what a resource did, query its <b>logs</b> in Log Analytics. If you only need to know when a number leaves its normal range, use <b>metrics with an alert</b>. '
        'If the question is "who changed this?", the <b>activity log</b> has it. Most real investigations use several of these together.'), label_cls='see')
    body += block('🔔 From signal to action', figure(d_alert(),
        'an <b>alert rule</b> watches a signal against a condition and a time window. When the condition is met it <b>fires</b> an <b>action group</b>, which can notify people, run automation, or open a ticket in an IT service tool. '
        'Splitting the rule (when to fire) from the action group (what to do) lets many alerts share one set of contacts and automation.'), label_cls='see')
    body += block('📊 Metrics, logs and traces', table(['','Answers','Looks like','Collected'], [
      ['📈 Metrics','Is something off, and since when?','Numbers in a time series; platform metrics arrive about every minute','Platform metrics automatically'],
      ['📜 Logs','What exactly happened?','Records with fields, queried with KQL','Resource logs need a diagnostic setting'],
      ['🧵 Traces','Where did this request go and slow down?','A request followed across services','Your app, instrumented (Application Insights, OpenTelemetry)'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🐢','Checkout feels slow since Tuesday','Which call inside the request is taking the time?','Application Insights traces'),
      ('📉','CPU on the web tier keeps spiking','Know about it before users do.','Metric alert + action group'),
      ('🔍','A firewall rule blocked a partner','What exactly was denied, and when?','Resource logs in Log Analytics'),
      ('🕵️','A setting changed overnight','Find out who changed it.','Activity log'),
      ('🧯','A disk is almost full','Fix it before the app stops.','Alert that runs an automation'),
      ('🏗️','Every new resource must send logs','Do not rely on people remembering.','Azure Policy deploys diagnostic settings'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — workspaces, settings and the traps', '''      <p><b>Two kinds of workspace.</b> A <i>Log Analytics workspace</i> holds logs and traces, queried with KQL. An <i>Azure Monitor workspace</i> holds Prometheus and OpenTelemetry metrics, queried with PromQL. Application Insights data is stored in a Log Analytics workspace, so you can query it like other logs.</p>
      <p><b>Diagnostic settings.</b> Platform metrics and the activity log are collected automatically, but <b>resource logs are not</b>. A diagnostic setting sends them to a Log Analytics workspace, an event hub or storage. For new settings, Microsoft recommends the resource-specific table mode. You can roll them out at scale with built-in Azure Policy (concept 16).</p>
      <p><b>Keep monitoring itself monitored.</b> The guardrails from concept 16 need signals too: send Policy, Defender and Key Vault logs to the same place, and alert when something important turns off.</p>
      <p><b>Cost.</b> Logs are billed by volume, and a diagnostic setting cannot filter inside a category; collect what you will use. (Cost Management is the next concept.)</p>''')
    body += recall([
      'Three signals: metrics (numbers over time), logs (detailed records), traces (a request across services). Azure Monitor gathers them.',
      'Platform metrics and the activity log are automatic; resource logs need a diagnostic setting; traces need instrumentation (Application Insights, OpenTelemetry).',
      'Log Analytics workspace = logs/traces queried with KQL. Application Insights = application performance monitoring.',
      'Alert rule (condition + window) fires an action group (notify, run automation, open ticket).',
      'Decide what to collect before the incident; alerts without an owner become noise.'])
    body += saythis('"I collect the three signals — metrics, logs and traces — in Azure Monitor. Metrics and the activity log are automatic, resource logs need diagnostic settings, and the app is instrumented with Application Insights and OpenTelemetry for traces. '
      'I query logs with KQL in Log Analytics, and I turn signals into action with alert rules and action groups. I deploy the diagnostic settings with Azure Policy so nothing is forgotten."')
    body += trap([
      '<b>Assuming logs are on by default.</b> Platform metrics and the activity log are, but resource logs are not collected until you create a diagnostic setting — so the one time you need them, they are missing.',
      'Second trap: <b>an alert for everything.</b> A flood of alerts trains people to ignore them. Alert on symptoms users feel, give each alert an owner, and use dashboards for the rest.'])
    body += confuse('📈 Metrics', 'Cheap, fast numbers over time. Tell you that something is off.', '📜 Logs and traces', 'Detailed records and request journeys. Tell you why and where.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt">// KQL: failed requests per hour in Application Insights, last day</span>
requests
| where timestamp &gt; ago(1d) and success == false
| summarize failures = count() by bin(timestamp, 1h)
| order by timestamp asc''',
      'Illustrative only — table and column names depend on how the workspace and the app are set up.'))
    body += next_box('You can now see what your system does. Everything above is also <b>metered</b> — and a good design can still be an unaffordable one. Next: Cost Management.', 'cost-management.html', 'Cost Management')
    body += fact_note(FOOT, [DOCS_AM, DOCS_AI, DOCS_LOGS, DOCS_DS, DOCS_AL, DOCS_MET])
    return page('monitoring-observability', 'Monitoring & Observability', 'Concept 17 of 19 · 🛠️ Shipping and operating',
        'Monitoring tells you something is wrong; observability helps you find why — <span class="grad-text">but only if you collected the signals before the incident.</span>',
        'Metrics, logs and traces in Azure Monitor, Log Analytics and Application Insights — plus alerts that turn signals into action.',
        'How would you monitor an Azure application and get alerted before users notice?',
        body, CR + ['<span class="cur">Monitoring &amp; Observability</span>'], '', search_title='Monitoring & Observability')
