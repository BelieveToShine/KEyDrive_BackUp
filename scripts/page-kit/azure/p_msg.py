from kit import *
from p_storage import CR

DOCS_SB = ('Service Bus documentation', 'https://learn.microsoft.com/en-us/azure/service-bus-messaging/')
DOCS_EH = ('Event Hubs documentation', 'https://learn.microsoft.com/en-us/azure/event-hubs/')
DOCS_EG = ('Event Grid documentation', 'https://learn.microsoft.com/en-us/azure/event-grid/')
DOCS_MSG = ('Choose an Azure messaging service (Architecture Center)', 'https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/messaging')

def d_why():
    d = Diagram('ms1', 640, 352, 'Without a queue, one broken service stops the whole order; with a queue the web app answers instantly and the worker catches up later')
    d.zone(10, 8, 620, 156, 'rose', 'WITHOUT A QUEUE · everyone waits for everyone')
    d.box(24, 44, 110, 64, [('🛒 Web app','t'),('user clicks Buy','s')], 'n')
    d.box(268, 44, 120, 64, [('💳 Payment','t'),('takes money','s')], 'n')
    d.box(522, 44, 100, 64, [('📧 Email','t'),('💥 is down','s')], 'rose')
    d.arrow([(134,76),(268,76)], 'rose', label='calls and waits', at=(201,76))
    d.arrow([(388,76),(522,76)], 'rose', label='calls and waits', at=(455,76))
    d.text(320, 140, '😞 One slow or broken service holds up the whole order.', size=10)
    d.zone(10, 180, 620, 164, 'emerald', 'WITH A QUEUE · the slow part can catch up later')
    d.box(24, 216, 110, 64, [('🛒 Web app','t'),('answers instantly','s')], 'n')
    d.box(268, 216, 120, 64, [('📬 Queue','t'),('orders wait here','s')], 'emerald')
    d.box(522, 216, 100, 64, [('⚙️ Worker','t'),('sends emails','s')], 'n')
    d.arrow([(134,248),(268,248)], 'emerald', label='sends a message', at=(201,248))
    d.arrow([(388,248),(522,248)], 'emerald', label='worker pulls', at=(455,248))
    d.text(320, 312, '✅ The web app is done in milliseconds. If the worker is down, messages wait safely.', size=10)
    return d

def d_msg_event():
    d = Diagram('ms2', 640, 316, 'A message is a request to do something with one receiver; an event is a fact that anyone can react to')
    d.zone(10, 8, 305, 300, 'cyan', 'MESSAGE · "please do this"')
    d.box(100, 44, 120, 50, [('🛒 Order service','t'),('the sender','s')], 'n')
    d.box(100, 136, 120, 44, [('📬 Queue','t')], 'cyan')
    d.box(100, 224, 120, 50, [('📦 Shipping','t'),('must handle it','s')], 'n')
    d.arrow([(160,94),(160,136)], 'cyan', label='ship order 42', at=(262,115))
    d.arrow([(160,180),(160,224)], 'cyan', label='one receiver', at=(256,202))
    d.text(162, 296, 'The sender expects the job to be done.', size=9.5)
    d.zone(325, 8, 305, 300, 'amber', 'EVENT · "this happened"')
    d.box(415, 44, 130, 50, [('📦 Blob Storage','t'),('the source','s')], 'n')
    d.box(415, 136, 130, 44, [('⚡ Event Grid','t')], 'amber')
    d.arrow([(480,94),(480,136)], 'amber', label='BlobCreated', at=(571,115))
    for x, t, s in ((338,'🖼️ Resize','a thumbnail'),(434,'🛡️ Scan','checks it'),(530,'📝 Audit','logs it')):
        d.box(x, 226, 90, 44, [(t,'t'),(s,'s')], 'n')
    for cx in (383, 479, 575):
        d.arrow([(480,180),(480,203),(cx,203),(cx,226)] if cx != 479 else [(480,180),(480,226)], 'amber')
    d.pill(480, 197, 'pushes to all')
    d.text(477, 296, 'Many handlers may react. The source does not care who.', size=9.5)
    return d

def d_choose_msg():
    d = Diagram('ms3', 640, 540, 'Decision tree for choosing between Event Grid, Event Hubs, Service Bus and Storage Queues')
    d.box(190, 8, 260, 34, [('🤔 What are you sending?','t')], 'cyan')
    qs = [(84,'⚡ A fact: something just happened?','a file arrived, a resource changed','Event Grid','react and push to handlers','emerald'),
          (182,'🌊 A non-stop stream to store and replay?','telemetry, clicks, logs','Event Hubs','a replayable log of events','cyan'),
          (280,'📨 A job that must be handled reliably?','ordering · retries · many subscribers','Service Bus','queues and topics','violet'),
          (378,'📬 Simple background jobs, very cheap?','huge backlog, no special features','Queue Storage','simple queue in a storage account','amber')]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(y,q,qs_,a,as_,col) in enumerate(qs):
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = qs[i+1][0] if i+1 < len(qs) else 476
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 476, 330, 50, [('🔌 Maybe you need no messaging at all','t'),('if the caller needs the answer now, call it directly','s')], 'rose')
    return d

def d_grid():
    d = Diagram('ms4', 640, 392, 'Event Grid: a source publishes an event to a topic; subscriptions filter it and push it to handlers')
    d.box(250, 10, 140, 46, [('📦 Blob Storage','t'),('event source','s')], 'n')
    d.box(250, 100, 140, 46, [('⚡ Event Grid','t'),('system topic','s')], 'amber')
    d.arrow([(320,56),(320,100)], 'amber', label='publishes event', at=(410,78))
    subs = [(10,'🔎 Subscription A','sends to a Function','type = BlobCreated','amber'),(226,'🔎 Subscription B','sends to a Logic App','subject ends .jpg','amber'),(442,'🔎 Subscription C','sends to a webhook','all events','amber')]
    for x, t, s, flt, col in subs:
        cx = x + 94
        d.box(x, 232, 188, 50, [(t,'t'),(s,'s')], col)
        pts = [(320,146),(320,172),(cx,172),(cx,232)] if cx != 320 else [(320,146),(320,232)]
        d.arrow(pts, 'amber', label='matches: ' + flt, at=(cx, 207) if cx != 320 else (cx, 207))
    for x, t, s in ((10,'λ Azure Function','your code runs'),(226,'🔁 Logic App','a no-code workflow'),(442,'🌐 Webhook','any HTTPS endpoint')):
        d.box(x, 340, 188, 44, [(t,'t'),(s,'s')], 'n')
        d.arrow([(x+94,282),(x+94,340)], 'amber', label='pushes event', at=(x+94,311))
    return d

def d_queue_topic():
    d = Diagram('sb1', 640, 512, 'Service Bus queue: each message goes to one competing worker. Topic: every matching subscription gets its own copy')
    d.zone(10, 8, 620, 170, 'violet', 'QUEUE · one message, one worker')
    d.box(24, 60, 100, 56, [('📤 Producer','t'),('sends orders','s')], 'n')
    d.box(200, 60, 150, 56, [('📬 Queue: orders','t'),('M1 · M2 · M3','s')], 'violet')
    d.box(480, 46, 140, 44, [('⚙️ Worker A','t')], 'n')
    d.box(480, 100, 140, 44, [('⚙️ Worker B','t')], 'n')
    d.arrow([(124,88),(200,88)], 'violet', label='sends', at=(162,88))
    d.arrow([(350,88),(436,88),(436,68),(480,68)], 'violet', label='delivers', at=(393,88))
    d.arrow([(350,88),(436,88),(436,122),(480,122)], 'violet')
    d.text(320, 164, 'Each message is handled by ONE worker — the workers compete for it.', size=9.5)
    d.zone(10, 190, 620, 312, 'cyan', 'TOPIC · every subscription gets its own copy')
    d.box(24, 232, 110, 44, [('📢 Publisher','t')], 'n')
    d.box(230, 232, 180, 44, [("📢 Topic: price-updates",'t')], 'cyan')
    d.arrow([(134,254),(230,254)], 'cyan', label='sends', at=(182,254))
    subs = [(24,'🔎 Subscription: EU','filter: region = EU','copy if region = EU'),
            (226,'🔎 Subscription: All','no filter — gets everything','copy of every message'),
            (428,'🔎 Subscription: Urgent','filter: priority = high','copy if priority = high')]
    for x, t, s, lab in subs:
        cx = x + 94
        d.box(x, 340, 188, 50, [(t,'t'),(s,'s')], 'cyan')
        pts = [(320,276),(320,300),(cx,300),(cx,340)] if cx != 320 else [(320,276),(320,340)]
        d.arrow(pts, 'cyan', label=lab, at=(cx, 312))
    for x, t in ((24,'⚙️ Pricing app (EU)'),(226,'📊 Analytics app'),(428,'🔔 Alerts app')):
        d.box(x, 442, 188, 44, [(t,'t')], 'n')
        d.arrow([(x+94,390),(x+94,442)], 'cyan', label='delivers', at=(x+94,416))
    return d

def d_lifecycle():
    d = Diagram('sb2', 640, 304, 'Life of a Service Bus message with peek-lock: waiting, locked, then completed, retried or dead-lettered')
    d.box(10, 100, 140, 60, [('📬 Waiting','t'),('in the queue','s')], 'violet')
    d.box(235, 100, 170, 64, [('🔒 Locked','t'),('a worker is processing','s'),('(peek-lock)','s')], 'amber')
    d.box(520, 20, 110, 56, [('✅ Completed','t'),('message removed','s')], 'emerald')
    d.box(490, 228, 140, 62, [('🧟 Dead-letter','t'),('a side queue for','s'),('bad messages','s')], 'rose')
    d.arrow([(150,130),(235,130)], 'violet', label='receive', at=(192,130))
    d.arrow([(405,118),(460,118),(460,48),(520,48)], 'emerald', label='Complete()', at=(460,83))
    d.arrow([(320,164),(320,200),(80,200),(80,160)], 'violet', label='lock expires or Abandon()', at=(200,200))
    d.arrow([(390,164),(390,259),(490,259)], 'rose', label='max retries', at=(434,259))
    d.text(200, 232, 'every retry adds 1 to the delivery count', size=9.5)
    return d

def d_hub_log():
    d = Diagram('eh1', 640, 424, 'Event Hubs: producers send events into partitions; each consumer group reads the same events at its own position; Capture saves them to storage')
    d.box(180, 10, 280, 44, [('📱 Devices · 🌐 Apps · 📋 Logs','t')], 'n')
    d.zone(10, 100, 620, 186, 'cyan', 'AN EVENT HUB · one stream split into partitions')
    for i in range(4):
        d.box(24, 138 + i*34, 330, 28, [(f'Partition {i} ▸ e0 e1 e2 e3 e4 e5 →','m')], 'cyan')
    d.text(372, 156, '• Same key → same partition', anchor='start', size=9.5)
    d.text(372, 190, '• Order is kept inside a partition', anchor='start', size=9.5)
    d.text(372, 224, '• New events join the end', anchor='start', size=9.5)
    d.text(372, 258, '• Events stay for the retention time', anchor='start', size=9.5)
    d.arrow([(320,54),(320,100)], 'cyan', label='send events', at=(400,77))
    cons = [(10,'📊 Group: analytics','its own position','reads at own pace'),(225,'🚨 Group: alerts','its own position','reads at own pace'),(440,'🗃️ Capture','saves batches to storage','copies to storage')]
    for x, t, s, lab in cons:
        d.box(x, 344, 190, 56, [(t,'t'),(s,'s')], 'n')
        d.arrow([(x+95,286),(x+95,344)], 'cyan', label=lab, at=(x+95,315))
    return d

def d_broker_log():
    d = Diagram('eh2', 640, 296, 'A Service Bus queue removes a message once it is completed; an Event Hubs partition keeps events while each reader tracks its own position')
    d.zone(10, 8, 305, 276, 'violet', 'SERVICE BUS · a post office')
    d.box(90, 44, 140, 56, [('📬 Queue','t'),('M1 · M2 · M3','s')], 'violet')
    d.box(90, 150, 140, 48, [('⚙️ Worker','t'),('takes M1','s')], 'n')
    d.arrow([(160,100),(160,150)], 'violet', label='delivers', at=(262,125))
    d.text(162, 232, 'When the worker completes M1,', size=9.5)
    d.text(162, 248, 'M1 is removed from the queue.', size=9.5, weight=700)
    d.zone(325, 8, 305, 276, 'cyan', 'EVENT HUBS · a log you can replay')
    d.box(340, 44, 275, 56, [('📜 One partition','t'),('E1 · E2 · E3 · E4 · E5 →','m')], 'cyan')
    d.box(340, 150, 125, 48, [('👁️ Reader A','t'),('is at E3','s')], 'n')
    d.box(490, 150, 125, 48, [('👁️ Reader B','t'),('is at E5','s')], 'n')
    d.arrow([(402,100),(402,150)], 'cyan', label='reads', at=(450,125))
    d.arrow([(552,100),(552,150)], 'cyan', label='reads', at=(598,125))
    d.text(477, 232, 'Events stay in the log for the retention time.', size=9.5)
    d.text(477, 248, 'Each reader keeps its own place.', size=9.5, weight=700)
    return d

FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official docs.'

def build_messaging():
    body = ''
    body += see(figure(d_why(),
        '<b>Top:</b> the web app calls Payment, which calls Email, and each call <em>waits for the reply</em>. If Email is down, the whole order is stuck. '
        '<b>Bottom:</b> the web app drops a message into a <b>queue</b> and answers the user at once. A worker picks the message up when it is ready. '
        'If the worker is down for a while, nothing is lost — the messages simply wait.'))
    body += one('Do not make parts of your app wait for each other — put a message in between. The sender drops it and moves on; the receiver picks it up when ready.')
    body += why([
      'At first, parts of an app call each other directly. It is simple, but it has a hidden cost: the <b>slowest</b> part slows everyone, a <b>broken</b> part breaks everyone, '
      'and a sudden rush of traffic hits the weakest part at full force.',
      'Messaging adds a safe waiting room between the parts. Now each part can speed up, slow down or fail <b>on its own</b>. '
      'Azure has four messaging tools because there are really three different needs: <b>messages</b> ("please do this job"), <b>events</b> ("this just happened") and <b>streams</b> (a huge, constant flow of events).'])
    body += block('🧠 First, the big idea: message or event?', figure(d_msg_event(),
        'a <b>message</b> is a request. The sender wants one receiver to do a job, and cares that it gets done ("ship order 42"). '
        'An <b>event</b> is a fact — "a file was created". The source just announces it, and any number of handlers may react or ignore it. '
        'Messages usually go through a queue; events usually go through an event router. This one idea decides which Azure service you need.'), label_cls='see')
    body += block('🧰 The four Azure messaging tools', pick_cards([
      dict(icon='📬', name='Storage Queues', tag='the simple, cheap to-do list', color='#fbbf24',
           use=['Simple background jobs', 'A very large backlog, kept cheap', 'No special features needed'],
           skip=['You need ordering, a bad-message bin or many subscribers → Service Bus', 'Messages larger than about 64 KB → store a file in Blob and send its address']),
      dict(icon='📨', name='Service Bus', tag='the reliable post office for business messages', color='#a78bfa',
           use=['Orders, payments, workflows — losing a message costs money', 'Order must be kept (sessions)', 'Retries and a dead-letter queue', 'One message to many subscribers (topics)'],
           skip=['Millions of tiny telemetry events → Event Hubs', 'Just reacting to "a file was created" → Event Grid']),
      dict(icon='⚡', name='Event Grid', tag='the doorbell that tells everyone something happened', color='#34d399',
           use=['React to things that happen in Azure (a blob was created)', 'Wire services together without polling', 'Serverless, event-driven designs'],
           skip=['You need ordered, guaranteed job processing → Service Bus', 'You need to replay old events later → Event Hubs']),
      dict(icon='🌊', name='Event Hubs', tag='the giant, replayable log for streams', color='#22d3ee',
           use=['Telemetry, clicks and logs at huge volume', 'Many readers each need the whole stream', 'You want to replay or archive the stream'],
           skip=['Single business commands that need per-message handling → Service Bus', 'A few rare events → Event Grid']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose_msg(),
        'read the questions from the top. A <b>fact</b> that something happened → Event Grid. A <b>non-stop stream</b> to store and replay → Event Hubs. '
        'A <b>job that must be handled reliably</b> → Service Bus. <b>Simple, cheap background jobs</b> → Storage Queues. And if none of them fits, you may not need messaging at all: when the caller needs the answer right now, call the service directly.'), label_cls='see')
    body += block('📊 Side by side', table(['','📬 Storage Queues','📨 Service Bus','⚡ Event Grid','🌊 Event Hubs'], [
      ['Think of it as','A simple to-do list','A post office with receipts','A doorbell','A giant tape recorder'],
      ['What you send','Small messages (up to about 64 KB)','Business messages','Events (facts)','A stream of events'],
      ['Who receives it','One worker per message','Queue: one worker. Topic: every subscription','Every subscribed handler (pushed to it)','Any number of reader groups, each reads everything'],
      ['Order','Not guaranteed','First-in-first-out with sessions','Not guaranteed','Kept inside a partition'],
      ['After it is read','Deleted when you finish it','Removed when completed','Retried for a while, then dropped or dead-lettered','Stays for the retention time'],
      ['Bad messages','No built-in dead-letter queue','Built-in dead-letter queue','Can dead-letter','Readers track their own position'],
    ]), label_cls='see')
    body += block('⚡ Event Grid in 10 seconds', figure(d_grid(),
        'a <b>source</b> (here, Blob Storage) publishes an event to a <b>topic</b>. Each <b>subscription</b> says which events it wants — by event type or by subject, such as "ends with .jpg" — and where to send them. '
        'Event Grid then <b>pushes</b> matching events to the <b>handler</b>: a Function, a Logic App, a webhook. Nobody polls and nothing waits.'), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🧾','Order processing','Each order must be handled once, in order for that customer, with retries.','Service Bus queue + sessions'),
      ('📢','Price update to many apps','The pricing app, the website and analytics all need every change.','Service Bus topic'),
      ('📸','Photo uploaded','Make a thumbnail the moment a file lands in storage.','Event Grid → Function'),
      ('🌡️','10,000 sensors','Constant tiny readings, analysed live and archived.','Event Hubs'),
      ('📧','Welcome emails','Send in the background. Cheap, simple, no special rules.','Storage Queue'),
      ('🏪','A whole shop','Service Bus processes orders, Event Hubs collects site telemetry, Event Grid reacts when an item ships.','All of them together'),
    ]), label_cls='see')
    body += block('🔬 Go deeper', deep_cards([
      ('Deep dive · Messaging', 'Service Bus: queues and topics', 'How a queue differs from a topic, what peek-lock does, dead-letter queues, sessions, and which tier to buy.', 'service-bus.html'),
      ('Deep dive · Messaging', 'Event Hubs', 'Partitions, consumer groups, replay, Capture to storage, Kafka support — and why it is not "a bigger Service Bus".', 'event-hubs.html')]), label_cls='next')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Delivery is "at least once".</b> With Service Bus peek-lock, a message that is not completed in time is delivered again. So your handler must be <b>idempotent</b>: doing it twice must be as safe as doing it once.</p>
      <p><b>Big payloads — the claim-check pattern.</b> Do not push big files through a queue. Save the file in Blob Storage and put only its address in the message. Both Storage Queues and Service Bus guides recommend this.</p>
      <p><b>They work together.</b> A common design: Blob Storage emits an event (Event Grid) → a Function reads it and puts a job on a Service Bus queue → workers process the job.</p>''')
    body += recall([
      'Message = "do this job" (expects it done). Event = "this happened" (anyone may react). Stream = a huge constant flow of events.',
      'Storage Queues = simple, cheap. Service Bus = reliable business messaging (queues, topics, sessions, dead-letter). Event Grid = push events to handlers. Event Hubs = replayable stream log.',
      'Messaging lets each part scale and fail independently — the sender does not wait.',
      'Delivery is at-least-once, so handlers must be idempotent. Use the claim-check pattern for big payloads.',
      'Services combine well: Service Bus for orders, Event Hubs for telemetry, Event Grid for reactions.'])
    body += saythis('"Messaging decouples parts of a system so they can scale and fail independently. For commands that must be processed reliably — orders, payments — I use Service Bus: queues for one consumer, topics for many, with sessions for ordering and a dead-letter queue for failures. '
      'For reacting to things that happen, I use Event Grid, which pushes events to handlers. For high-volume telemetry that I need to replay, I use Event Hubs. For simple, cheap background jobs, Storage Queues. And I make handlers idempotent, because delivery is at least once."')
    body += trap([
      '<b>Event Hubs is not "a bigger Service Bus".</b> Service Bus is a broker: it hands each message to a worker and removes it when done. Event Hubs is a log: events stay, and every reader tracks its own position. Using the wrong one means missing features you assumed were there.',
      'Second trap: assuming a message arrives <i>exactly</i> once. It is at least once — so a duplicate must not double-charge a customer.'])
    body += confuse('📨 Service Bus', 'A broker for messages: one message, handed to a worker, removed once handled. Built for reliability.', '🌊 Event Hubs', 'A log for streams: events are kept, many readers each read all of them. Built for volume and replay.')
    body += zoom('💻 Tiny illustrative example — send a message', code_block(
'''<span class="kw">from</span> azure.identity <span class="kw">import</span> DefaultAzureCredential
<span class="kw">from</span> azure.servicebus <span class="kw">import</span> ServiceBusClient, ServiceBusMessage

client = ServiceBusClient(<span class="str">"mynamespace.servicebus.windows.net"</span>, DefaultAzureCredential())
<span class="kw">with</span> client.get_queue_sender(<span class="str">"orders"</span>) <span class="kw">as</span> sender:
    sender.send_messages(ServiceBusMessage(<span class="str">'{"orderId": 42}'</span>))   <span class="cmt"># returns fast — the worker handles it later</span>''',
      'Illustrative shape only — the app\'s identity needs a role such as Azure Service Bus Data Sender, and real code adds error handling.'))
    body += next_box('Messages and events now have a home. Next: running small pieces of code only when a message or event arrives — Serverless &amp; Orchestration.', 'serverless-orchestration.html', 'Serverless &amp; Orchestration')
    body += fact_note(FOOT, [DOCS_MSG, DOCS_SB, DOCS_EH, DOCS_EG])
    return page('messaging', 'Messaging & Events', 'Concept 11 of 19 · ⚙️ Handling load',
        'Messaging lets one part of your app <span class="grad-text">hand off work</span> without waiting — and without crashing together.',
        'When parts of an app call each other directly, the slowest or most broken part drags everyone down. Azure gives you four messaging tools — '
        'and the skill is knowing which one to reach for.',
        'What is the difference between Service Bus, Event Hubs, Event Grid and Storage Queues, and when do you use each?',
        body, CR + ['<span class="cur">Messaging &amp; Events</span>'], '', search_title='Messaging & Events')

def build_service_bus():
    body = ''
    body += see(figure(d_queue_topic(),
        '<b>Top — a queue:</b> a producer sends messages; workers pull them. Each message goes to <b>one</b> worker, so the workers share (compete for) the work. '
        '<b>Bottom — a topic:</b> a publisher sends one message; each <b>subscription</b> checks its filter and, if the message matches, gets <b>its own copy</b>. '
        'So a queue shares jobs between workers, and a topic shares news between apps.'))
    body += one('A queue hands each message to one worker. A topic gives every matching subscription its own copy. Both keep the message until someone confirms it was handled.')
    body += why([
      'Some messages are too important to lose: an order, a payment, a stock change. Dropping one costs money; handling one twice costs trust. A plain queue cannot promise much beyond "it is in there".',
      '<b>Service Bus</b> is the broker for these messages. It holds a message until a worker <b>confirms</b> it was handled, retries if the worker fails, moves messages that keep failing to a side queue, '
      'and can keep messages in order. That is the difference between "a list of jobs" and "a reliable post office".'])
    body += block('🔁 The life of one message', figure(d_lifecycle(),
        'a message waits in the queue. A worker <b>receives</b> it with <b>peek-lock</b>: the message is locked, not deleted, so nobody else takes it. '
        'If the worker finishes, it calls <b>Complete()</b> and the message is removed. If the worker fails or is too slow, the lock expires (or the worker calls Abandon()), the message goes back to waiting, and its <b>delivery count</b> goes up by one. '
        'After too many tries — 10 by default — Service Bus moves it to the <b>dead-letter queue</b>, a side queue where you can look at it and fix the cause.'), label_cls='see')
    body += block('🧰 Features that make it "enterprise"', '''    <div class="taxonomy-strip">
      <div class="tax-item"><h5>🎟️ Sessions</h5><p>Messages with the same session id are handled in order, one session at a time. Use the customer id so each customer\'s steps stay in order.</p></div>
      <div class="tax-item"><h5>🧟 Dead-letter queue</h5><p>Every queue and subscription has one. Bad or expired messages land there instead of blocking everyone.</p></div>
      <div class="tax-item"><h5>🪞 Duplicate detection</h5><p>Drops a message that is sent twice with the same MessageId within a time window. It protects the <b>sending</b> side only.</p></div>
      <div class="tax-item"><h5>⏰ Scheduled delivery</h5><p>Send a message now, deliver it later — "remind the customer in 24 hours".</p></div>
      <div class="tax-item"><h5>🔗 Transactions</h5><p>Group operations so they succeed or fail together.</p></div>
      <div class="tax-item"><h5>➡️ Auto-forwarding</h5><p>Chain queues and subscriptions so messages flow on to another queue automatically.</p></div>
    </div>''', label_cls='see')
    body += block('🏷️ Which tier?', table(['','Basic','Standard','Premium'], [
      ['Queues','✅','✅','✅'],
      ['Topics and subscriptions','❌','✅','✅'],
      ['Capacity','Shared','Shared, billed per operation','Dedicated resources, predictable performance'],
      ['Extras','—','—','Isolation, Private Link, geo-replication, much larger messages'],
      ['Pick it for','Simple queues only','Most apps that need topics','Heavy, steady or sensitive workloads'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🧾','Order processing','Orders go on a queue. Several workers share the load, and failures are retried.','Queue'),
      ('📢','Price update','The website, the app and analytics each need every price change.','Topic + 3 subscriptions'),
      ('🧑','Steps per customer','"Created", "paid", "shipped" must be handled in order for each customer.','Sessions (session id = customer id)'),
      ('🧟','A poison message','One malformed message keeps crashing the worker. It must not block the rest.','Dead-letter queue'),
      ('⏰','Reminder in 24 hours','Send now, deliver tomorrow.','Scheduled message'),
      ('🌍','Regional filter','The EU app only wants EU price changes.','Subscription filter'),
    ]), label_cls='see')
    body += recall([
      'Queue = one message, one worker (competing consumers). Topic = every matching subscription gets its own copy.',
      'Peek-lock: receive → lock → Complete() removes it; failure or lock expiry returns it and raises the delivery count. Too many tries → dead-letter queue (default limit 10).',
      'Sessions keep messages with the same session id in order.',
      'Topics need the Standard or Premium tier; Basic has queues only.',
      'Delivery is at-least-once — make the handler idempotent. Duplicate detection only stops duplicate sends.'])
    body += saythis('"Service Bus is Azure\'s enterprise message broker. A queue delivers each message to one of several competing workers; a topic copies each message to every subscription whose filter matches. '
      'With peek-lock the message is locked while a worker processes it and removed only when completed; repeated failures move it to the dead-letter queue. '
      'I use sessions for ordering, and I make handlers idempotent because delivery is at least once."')
    body += trap([
      '<b>At-least-once means duplicates can happen.</b> If a worker finishes the work but crashes before it calls Complete(), the message comes back. <i>Duplicate detection</i> will not help — it only catches the same message being <b>sent</b> twice. Make the handler safe to run twice.',
      'Second trap: a message that matches <b>no</b> subscription filter on a topic is not delivered to any subscription — it is effectively dropped. Add a catch-all subscription if you need to see everything.'])
    body += confuse('🔒 Peek-lock', 'Receive → locked → you complete it. If you fail, it comes back. At-least-once. The safe default for important work.', '🗑️ Receive-and-delete', 'The message is removed the moment it is received. If you crash, it is gone. At-most-once — only for work you can afford to lose.')
    body += zoom('💻 Tiny illustrative example — receive and complete', code_block(
'''<span class="kw">with</span> client.get_queue_receiver(<span class="str">"orders"</span>) <span class="kw">as</span> receiver:
    <span class="kw">for</span> msg <span class="kw">in</span> receiver:
        handle(str(msg))                 <span class="cmt"># your code — must be safe to run twice</span>
        receiver.complete_message(msg)   <span class="cmt"># tell Service Bus it is done, so it is removed</span>''',
      'Illustrative shape only — real code also handles errors (abandon or dead-letter the message) and renews long locks.'))
    body += next_box('Service Bus is for messages that need care. For huge streams of simple events, you want a different tool: Event Hubs.', 'event-hubs.html', 'Event Hubs')
    body += fact_note(FOOT, [DOCS_SB, DOCS_MSG])
    return page('service-bus', 'Service Bus: Queues & Topics', 'Deep dive · Messaging · 📨 Service Bus',
        'Service Bus is <span class="grad-text">a safe post office</span> for business messages — it holds each one until someone confirms it was handled.',
        'Use it when losing, duplicating or mixing up a message would cost you money or trust: orders, payments, workflows. Learn queues, topics, peek-lock, dead-letter queues and sessions.',
        'What is the difference between a Service Bus queue and a topic, and what happens to a message that keeps failing?',
        body, CR + ['<a href="messaging.html">Messaging &amp; Events</a>', '<span class="cur">Service Bus</span>'], '', search_title='Service Bus: Queues & Topics')

def build_event_hubs():
    body = ''
    body += see(figure(d_hub_log(),
        'devices, apps and logs <b>send events</b> into an event hub. The hub splits the stream into <b>partitions</b> — ordered logs that new events join at the end. Events with the same key land in the same partition, so their order is kept. '
        'Below, several <b>consumer groups</b> read the same events, each from its own position, at its own speed. <b>Capture</b> can also save the stream to Blob Storage or Data Lake automatically.'))
    body += one('Event Hubs is a replayable log: events are appended, kept for a while, and every reader group keeps its own place in the stream.')
    body += why([
      'Service Bus treats each message as a precious job and takes care of it one by one. That care costs throughput. Now imagine 10,000 sensors sending a reading every second, '
      'or every click on a busy website: millions of tiny events, where losing one is fine but <b>keeping up</b> is not — and several teams want to read the same data.',
      '<b>Event Hubs</b> is built for that: very high volume in, many independent readers out, and the ability to <b>replay</b> what happened. It is a log, not a mailbox.'])
    body += block('📬 vs 📜 Mailbox or log?', figure(d_broker_log(),
        '<b>Left:</b> in Service Bus the message is taken by a worker and <em>removed</em> once completed — a mailbox. '
        '<b>Right:</b> in Event Hubs events <em>stay</em> in the partition for the retention time. Reader A is at E3 and Reader B is at E5 — each reads at its own pace, and either can go back and re-read. '
        'That is why Event Hubs suits streams and analytics, and Service Bus suits jobs.'), label_cls='see')
    body += block('📖 The words you need', '''    <div class="taxonomy-strip">
      <div class="tax-item"><h5>🏢 Namespace</h5><p>The container that holds your event hubs, with one address and shared settings.</p></div>
      <div class="tax-item"><h5>📜 Event hub</h5><p>One named stream — for example "telemetry". It is split into partitions.</p></div>
      <div class="tax-item"><h5>🧱 Partition</h5><p>An ordered sequence of events. Order is kept <b>inside</b> a partition, not across them. More partitions = more parallel readers.</p></div>
      <div class="tax-item"><h5>👥 Consumer group</h5><p>An independent view of the whole stream. Analytics and alerts each use their own group, so they never disturb each other.</p></div>
      <div class="tax-item"><h5>📍 Checkpoint</h5><p>A reader\'s saved position, so after a restart it carries on where it stopped.</p></div>
      <div class="tax-item"><h5>🗃️ Capture</h5><p>Automatically saves the stream in batches to Blob Storage or Data Lake for long-term keeping.</p></div>
    </div>''', label_cls='see')
    body += block('🔌 Already using Kafka?', '''    <div class="kd-card">Event Hubs speaks the <b>Apache Kafka</b> protocol, so existing Kafka producers and consumers can usually point at an Event Hubs endpoint instead of running their own Kafka cluster. This is available from the <b>Standard</b> tier up.</div>''', label_cls='see')
    body += block('🏷️ Which tier?', table(['Tier','What it is for','Good to know'], [
      ['Basic','Low-cost entry for simple streaming','No Capture, no Kafka'],
      ['Standard','The general-purpose choice','Capture, Kafka endpoint and geo-disaster-recovery are available'],
      ['Premium','Resource isolation and higher performance','For demanding or sensitive workloads'],
      ['Dedicated','A single-tenant cluster for the very largest workloads','Biggest scale'],
    ]) + '\n    <div class="kd-card" style="margin-top:14px"><b>Plan your partitions early.</b> You choose the partition count when you create the event hub, and only the Premium and Dedicated tiers let you increase it later. Retention is a limited window that depends on the tier, so use Capture if you must keep data longer.</div>', label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🌡️','IoT telemetry','Thousands of devices send readings every second to live dashboards.','Event Hubs'),
      ('🖱️','Website clickstream','Every click flows to analytics and to a recommendation engine — two reader groups.','Event Hubs + 2 consumer groups'),
      ('📋','Logs and metrics','Collect logs from hundreds of servers into one pipeline.','Event Hubs'),
      ('🕵️','Fraud detection','Score card transactions as the stream arrives, and keep a copy for audits.','Event Hubs + Capture'),
      ('🧳','Existing Kafka app','The team already writes Kafka code and wants a managed service.','Event Hubs (Kafka endpoint)'),
      ('🧾','Business orders','Each order must be processed once, with retries.','Not Event Hubs — Service Bus'),
    ]), label_cls='see')
    body += recall([
      'Event Hubs = a partitioned, replayable event log for high-volume streams.',
      'Order is kept inside a partition, not across partitions. Same key → same partition.',
      'Each consumer group has an independent view and its own checkpoint; many groups can read the same events.',
      'Events are not deleted when read — they stay for the retention time. Capture saves them to Blob / Data Lake.',
      'Event Hubs has a Kafka-protocol endpoint (Standard tier and above). Choose the partition count up front.'])
    body += saythis('"Event Hubs is Azure\'s event-streaming service — a partitioned, append-only log built for very high throughput. Producers append events; each consumer group reads the whole stream independently with its own checkpoint, so events can be replayed or processed by several systems. '
      'Order is guaranteed within a partition. I use Capture to archive to Blob or Data Lake, and the Kafka endpoint to migrate Kafka workloads. For per-message reliability like orders and payments I would use Service Bus instead."')
    body += trap([
      '<b>Reading does not delete.</b> Unlike a queue, an event is still there after a reader has processed it — which is a feature (replay) but means <i>you</i> must track progress with checkpoints.',
      'Second trap: expecting order across the whole event hub. Order is kept only <b>inside a partition</b>, so put events that must stay in order (one device, one customer) on the same partition with the same key.'])
    body += confuse('📨 Service Bus', 'Broker: handles each message with care and removes it when done. Built for reliable jobs.', '🌊 Event Hubs', 'Log: appends events, keeps them, lets many readers replay them. Built for volume.')
    body += zoom('💻 Tiny illustrative example — send a batch of events', code_block(
'''<span class="kw">from</span> azure.identity <span class="kw">import</span> DefaultAzureCredential
<span class="kw">from</span> azure.eventhub <span class="kw">import</span> EventHubProducerClient, EventData

producer = EventHubProducerClient(<span class="str">"mynamespace.servicebus.windows.net"</span>,
                                  eventhub_name=<span class="str">"telemetry"</span>, credential=DefaultAzureCredential())
<span class="kw">with</span> producer:
    batch = producer.create_batch()
    batch.add(EventData(<span class="str">'{"deviceId": "d1", "temp": 21.5}'</span>))
    producer.send_batch(batch)           <span class="cmt"># many events go in one efficient call</span>''',
      'Illustrative shape only — real producers choose a partition key, handle errors, and the identity needs a role such as Azure Event Hubs Data Sender.'))
    body += next_box('That is Event Hubs. Back to the Messaging page for the full picture of all four tools — and on to the next concept: Serverless &amp; Orchestration'., 'messaging.html', 'Back to Messaging')
    body += fact_note(FOOT, [DOCS_EH, DOCS_MSG])
    return page('event-hubs', 'Event Hubs', 'Deep dive · Messaging · 🌊 Event Hubs',
        'Event Hubs is <span class="grad-text">a giant, replayable log</span> for huge streams of events — many readers, each at its own position.',
        'When thousands of devices or users send millions of small events, you need a pipe built for volume and replay — not a mailbox for single jobs. '
        'Learn partitions, consumer groups, Capture and when Event Hubs is the right tool.',
        'When would you choose Event Hubs over Service Bus, and what are partitions and consumer groups?',
        body, CR + ['<a href="messaging.html">Messaging &amp; Events</a>', '<span class="cur">Event Hubs</span>'], '', search_title='Event Hubs')
