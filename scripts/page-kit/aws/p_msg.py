from kit import *
from p_common import CR

DOCS_DG = ('Amazon SQS, Amazon SNS, or Amazon EventBridge? (decision guide)', 'https://docs.aws.amazon.com/decision-guides/latest/sns-or-sqs-or-eventbridge/sns-or-sqs-or-eventbridge.html')
DOCS_INT = ('Choosing an AWS application integration service', 'https://docs.aws.amazon.com/decision-guides/latest/application-integration-on-aws-how-to-choose/application-integration-on-aws-how-to-choose.html')
DOCS_SQS = ('Amazon SQS documentation', 'https://docs.aws.amazon.com/sqs/')
DOCS_SNS = ('Amazon SNS documentation', 'https://docs.aws.amazon.com/sns/')
DOCS_EB = ('Amazon EventBridge documentation', 'https://docs.aws.amazon.com/eventbridge/')
DOCS_KDS = ('Amazon Kinesis Data Streams developer guide', 'https://docs.aws.amazon.com/streams/latest/dev/introduction.html')
DOCS_KEY = ('Kinesis Data Streams terminology and concepts', 'https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html')
DOCS_MODE = ('Choose the right Kinesis capacity mode', 'https://docs.aws.amazon.com/streams/latest/dev/how-do-i-size-a-stream.html')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official AWS docs.'

def d_three():
    d = Diagram('ms1', 640, 300, 'Three shapes of asynchronous communication: a message waits in a queue for one worker, an event is announced to whoever listens, and a stream is a log many readers replay')
    d.box(10, 40, 200, 150, [('📬 Message','t'),('SQS · SNS','s'),('"do this job"','s'),('one consumer handles it','s'),('removed once processed','s')], 'violet')
    d.box(220, 40, 200, 150, [('📣 Event','t'),('EventBridge · SNS','s'),('"this happened"','s'),('many may react','s'),('fire and route','s')], 'cyan')
    d.box(430, 40, 200, 150, [('🌊 Stream','t'),('Kinesis Data Streams','s'),('a long ordered log','s'),('many readers, replay','s'),('kept for a retention period','s')], 'amber')
    d.arrow([(110,190),(110,230),(530,230),(530,190)], 'n', label='pick by what the data means', at=(320,230))
    d.text(320, 278, 'Do not make parts of your app wait for each other — put something in between.', size=9.5, weight=700)
    return d

def d_choose():
    d = Diagram('ms2', 640, 524, 'Decision tree: a job for one worker use SQS, announce to many use SNS or EventBridge, route by content use EventBridge, a huge ordered stream use Kinesis')
    d.box(190, 8, 260, 34, [('🤔 What are you sending?','t')], 'cyan')
    qs = [
     ('📬 A job one worker must finish?', 'process an order, resize an image', 'SQS queue', 'buffers; consumers pull', 'violet'),
     ('📣 Tell many subscribers at once?', 'email, SMS, queues, functions', 'SNS topic', 'push to every subscriber', 'cyan'),
     ('🧭 Route events by their content?', 'rules decide the target', 'EventBridge', 'event bus with rules', 'emerald'),
     ('🌊 A flood of ordered events to replay?', 'clickstreams, logs, telemetry', 'Kinesis', 'shards and retention', 'amber'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 460
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 460, 330, 54, [('🤝 Often you combine them','t'),('SNS or EventBridge → SQS buffer','s')], 'n')
    return d

def d_combo():
    d = Diagram('ms3', 640, 292, 'A common combination: an order event goes to EventBridge, which routes it to separate SQS queues so each consumer works at its own pace')
    d.box(10, 108, 90, 64, [('🛒 Orders','t'),('service','s')], 'n')
    d.box(210, 108, 140, 64, [('🧭 EventBridge','t'),('rules route','s')], 'emerald')
    d.box(480, 30, 150, 56, [('📬 Billing queue','t'),('SQS','s')], 'violet')
    d.box(480, 118, 150, 56, [('📬 Email queue','t'),('SQS','s')], 'violet')
    d.box(480, 206, 150, 56, [('📬 Stock queue','t'),('SQS','s')], 'violet')
    d.arrow([(100,140),(210,140)], 'emerald', label='publishes', at=(155,140))
    d.arrow([(350,126),(415,126),(415,58),(480,58)], 'violet', label='rule', at=(415,92))
    d.arrow([(350,146),(480,146)], 'violet', label='rule', at=(415,146))
    d.arrow([(350,158),(415,158),(415,234),(480,234)], 'violet', label='rule', at=(415,196))
    return d

def build_messaging():
    body = ''
    body += see(figure(d_three(),
        'three shapes of "do not wait for each other". A <b>message</b> says "do this job" and waits in a queue until one worker handles it (SQS, SNS). An <b>event</b> says "this happened" and is announced to whoever cares (EventBridge, SNS). '
        'A <b>stream</b> is a long ordered log that many readers can replay (Kinesis). Choosing the right shape is most of the skill.'))
    body += one('When one part of your system calls another and waits, they fail together — put a queue, topic or stream in between so each side can scale and fail on its own.')
    body += why([
      'Caching and scaling help a request finish faster. But some work does not belong in the request at all: sending an email, resizing an image, charging a card, updating stock. If the web request waits for all of that, it is slow — and if one step fails, the whole request fails.',
      'The fix is to <b>decouple</b>. The web app drops a message or event into a service in the middle and carries on. Workers pick it up when they can. Under load, work queues up instead of failing; when a worker crashes, the message is still there. AWS offers several services because "send something" means different things.'])
    body += block('🧰 The four services', pick_cards([
      dict(icon='📬', name='Amazon SQS', tag='a queue — pull-based', color='#a78bfa',
           use=['A job for one worker; messages wait until processed or expired', 'A buffer so a slow consumer does not slow the producer', 'FIFO queues when strict order matters'],
           skip=['You need to notify many subscribers at once → SNS or EventBridge']),
      dict(icon='📣', name='Amazon SNS', tag='topics — push to subscribers', color='#22d3ee',
           use=['Fan-out: one message to many subscribers', 'Subscribers include SQS queues, Lambda functions, HTTP endpoints, email, SMS and mobile push', 'SNS FIFO topics when order matters'],
           skip=['You need messages to wait for slow consumers — SNS does not store them; put an SQS queue behind it']),
      dict(icon='🧭', name='Amazon EventBridge', tag='an event bus with rules', color='#34d399',
           use=['Route events by their content to one or more targets', 'Many topics and filters between microservices', 'AWS and SaaS events'],
           skip=['You need ordering guarantees — EventBridge does not provide message ordering']),
      dict(icon='🌊', name='Amazon Kinesis Data Streams', tag='a stream — a replayable log', color='#fbbf24',
           use=['Huge volumes of ordered events: clicks, logs, telemetry', 'Many readers, each with their own position; replay within retention'],
           skip=['A simple job queue — SQS is simpler']),
    ]), label_cls='see')
    body += block('🧭 When to pick what', figure(d_choose(),
        'ask in order. <b>A job for one worker?</b> SQS. <b>Tell many subscribers at once?</b> SNS. <b>Route by event content?</b> EventBridge. <b>A flood of ordered events to replay?</b> Kinesis. '
        'The fifth box is the real-world answer: combine them — for example, SNS or EventBridge delivering into an SQS queue as a buffer for each consumer.'), label_cls='see')
    body += block('🤝 Using them together', figure(d_combo(),
        'an orders service publishes one event. <b>EventBridge</b> rules route it to a separate <b>SQS queue</b> for billing, email and stock. Each consumer reads its own queue at its own pace, and if one is down its messages simply wait. '
        'This is the "event bus in front, queues behind" pattern AWS describes: EventBridge or SNS for routing, SQS as the buffer.'), label_cls='see')
    body += block('📊 Side by side', table(['','Model','Delivery','Order','Keeps messages?'], [
      ['📬 SQS','Pull from a queue','Consumers fetch','FIFO queues guarantee order','Yes, until processed or expired'],
      ['📣 SNS','Push to subscribers','Pushed in real time','FIFO topics guarantee order','No — not persisted'],
      ['🧭 EventBridge','Rules route events','To targets','No ordering guarantee','Not as a queue; targets can buffer'],
      ['🌊 Kinesis','Readers pull from shards','Consumers read the log','Per shard','For a retention period'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('📧','Send a welcome email after sign-up','The sign-up page must not wait.','SQS queue + a worker'),
      ('📢','An order is placed','Billing, shipping and analytics all need to know.','SNS or EventBridge to queues'),
      ('🧭','Only "premium order" events go to the VIP team','Route by content.','An EventBridge rule'),
      ('🏦','Process transactions in strict order per account','Order matters.','SQS FIFO'),
      ('📈','Millions of clicks a minute','Many analysis jobs read the same flow.','Kinesis Data Streams'),
      ('⚠️','A message keeps failing','It should not block the others.','A dead-letter queue'),
    ]), label_cls='see')
    body += block('🔬 Go deeper', deep_cards([
      ('Deep dive · Messaging', 'SQS, SNS and EventBridge', 'Queues versus topics versus event buses: pull and push, ordering, fan-out, filtering and the combinations that real systems use.', 'sqs-sns-eventbridge.html'),
      ('Deep dive · Messaging', 'Kinesis Data Streams', 'Shards, partition keys, retention, capacity modes and enhanced fan-out: when a stream beats a queue.', 'kinesis.html')]), label_cls='next')
    body += zoom('Go one level deeper (60 seconds) — habits for async systems', '''      <p><b>Expect duplicates.</b> Messaging infrastructure can deliver the same message more than once, and EventBridge targets get events at least once. Make consumers <i>idempotent</i>: doing the work twice has the same result as once.</p>
      <p><b>Dead-letter queues.</b> When a message fails repeatedly, move it aside so it does not block healthy messages, and look at it later.</p>
      <p><b>Retention.</b> SQS keeps messages until they are processed or expire (up to a fixed maximum retention); Kinesis keeps data for its retention period; SNS does not persist messages.</p>
      <p><b>Message, event, stream.</b> A message is a command for one handler. An event is a fact many may use. A stream is a log you read at your own position. The words matter because they decide who is responsible for what happens next.</p>''')
    body += recall([
      'Message (SQS/SNS) = a job; event (EventBridge) = a fact to route; stream (Kinesis) = a replayable log.',
      'SQS is pull-based and persists until processed or expired; SNS is push-based and does not persist; EventBridge routes by rules and has no ordering guarantee.',
      'FIFO queues and FIFO topics give strict ordering.',
      'Combine: SNS or EventBridge → SQS buffer per consumer. Add dead-letter queues.',
      'Consumers must be idempotent — duplicates happen.'])
    body += saythis('"I decouple with the right shape: SQS for a job one worker handles, SNS for fan-out to many subscribers, EventBridge to route events by content, and Kinesis for a replayable ordered stream. '
      'In practice I put EventBridge or SNS in front and an SQS queue behind each consumer as a buffer, add dead-letter queues, and make consumers idempotent because duplicates happen."')
    body += trap([
      '<b>Treating SNS like a queue.</b> It pushes to subscribers and does not persist messages; a subscriber that is down can miss them. Put an SQS queue behind it.',
      'Second trap: <b>assuming order everywhere.</b> Only FIFO queues, FIFO topics and a single Kinesis shard give ordering. EventBridge does not.'])
    body += confuse('📨 Message', 'A command for one handler. Removed once handled. You care that it was processed.', '📣 Event', 'A fact that something happened. Many may react, or none. The sender does not care who.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># send a message to an SQS queue</span>
aws sqs send-message --queue-url https://sqs.eu-west-1.amazonaws.com/111122223333/orders \\
    --message-body '{"order_id": 1001}\'''',
      'Illustrative shape only — the queue URL, account ID and body are placeholders.'))
    body += next_box('Messages and events now have a home. Next: running small pieces of code only when a message or event arrives — Serverless &amp; Orchestration.', 'serverless-orchestration.html', 'Serverless &amp; Orchestration')
    body += fact_note(FOOT, [DOCS_DG, DOCS_INT, DOCS_SQS, DOCS_SNS, DOCS_EB, DOCS_KDS])
    return page('messaging', 'Messaging & Events', 'Concept 11 of 19 · ⚙️ Handling load',
        'When one part of your system waits for another, they fail together — <span class="grad-text">put a queue, topic or stream in between.</span>',
        'SQS, SNS, EventBridge and Kinesis: messages, events and streams, what each is for and how they combine.',
        'When would you use SQS, SNS, EventBridge or Kinesis?',
        body, CR + ['<span class="cur">Messaging &amp; Events</span>'], '', search_title='Messaging & Events')

# ------------------------------------------------------ deep dive: SQS / SNS / EventBridge
def d_pull_push():
    d = Diagram('sq1', 640, 292, 'SQS holds messages until a consumer pulls them; SNS pushes each message to every subscriber at once and does not keep it')
    d.zone(10, 8, 305, 276, 'violet', 'SQS · pull from a queue')
    d.box(22, 100, 76, 56, [('📱 Send','t')], 'n')
    d.box(118, 100, 76, 56, [('📬 Queue','t'),('holds','s')], 'violet')
    d.box(214, 100, 80, 56, [('Worker','t'),('pulls','s')], 'n')
    d.arrow([(98,128),(118,128)], 'violet')
    d.arrow([(214,128),(194,128)], 'violet')
    d.text(162, 196, 'Messages wait. The worker pulls', size=9.5)
    d.text(162, 212, 'one when ready; a slow worker just', size=9.5)
    d.text(162, 228, 'means a longer queue.', size=9.5, weight=700)
    d.zone(325, 8, 305, 276, 'cyan', 'SNS · push to subscribers')
    d.box(337, 100, 72, 56, [('📱 Send','t')], 'n')
    d.box(437, 100, 90, 56, [('📣 Topic','t'),('pushes','s')], 'cyan')
    d.arrow([(409,128),(437,128)], 'cyan')
    d.arrow([(527,112),(540,112),(540,62),(555,62)], 'cyan')
    d.arrow([(527,128),(555,128)], 'cyan')
    d.arrow([(527,144),(540,144),(540,194),(555,194)], 'cyan')
    d.box(555, 40, 70, 44, [('Email','t')], 'n')
    d.box(555, 100, 70, 56, [('Lambda','t')], 'n')
    d.box(555, 172, 70, 44, [('SQS','t')], 'n')
    d.text(477, 244, 'Not persisted: a subscriber that is down can miss it.', size=9.5, weight=700)
    return d

def d_choose2():
    d = Diagram('sq2', 640, 424, 'Decision tree: one consumer and buffering means SQS; many subscribers means SNS; routing by event content or many sources means EventBridge')
    d.box(190, 8, 260, 34, [('🤔 Who needs it?','t')], 'cyan')
    qs = [
     ('👤 One consumer, and it may be slow?', 'work should wait its turn', 'SQS', 'queue, pull, retain', 'violet'),
     ('👥 Many subscribers, same message?', 'large fan-out', 'SNS', 'topic, push', 'cyan'),
     ('🧭 Route by content, from many sources?', 'AWS and SaaS events, filters', 'EventBridge', 'bus and rules', 'emerald'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 366
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 366, 330, 50, [('🤝 More than one answer?','t'),('combine: topic or bus, then queues','s')], 'n')
    return d

def d_dlq():
    d = Diagram('sq3', 640, 270, 'A message that keeps failing is moved to a dead-letter queue so it does not block the healthy messages behind it')
    d.box(10, 90, 110, 64, [('📬 Main queue','t'),('SQS','s')], 'violet')
    d.box(250, 90, 130, 64, [('⚙️ Consumer','t'),('processes','s')], 'n')
    d.box(510, 90, 120, 64, [('☠️ Dead-letter','t'),('queue','t')], 'rose')
    d.arrow([(120,122),(250,122)], 'violet', label='pulled', at=(185,122))
    d.arrow([(380,122),(510,122)], 'rose', label='fails often', at=(437,122), dash=True)
    d.text(320, 206, 'The visibility timeout hides a message while a consumer works on it;', size=9.5)
    d.text(320, 222, 'if it is not deleted in time, it becomes visible again and is retried.', size=9.5)
    d.text(320, 248, 'After repeated failures it goes to the dead-letter queue for a human to inspect.', size=9.5, weight=700)
    return d

def build_sqs_sns_eventbridge():
    body = ''
    body += see(figure(d_pull_push(),
        '<b>SQS</b> (left) is <em>pull</em>: the sender drops a message into a queue, it waits, and a worker pulls it when ready — a slow worker just means a longer queue. '
        '<b>SNS</b> (right) is <em>push</em>: the topic delivers each message to every subscriber right away (email, a function, a queue) and does not keep it, so a subscriber that is down can miss it.'))
    body += one('SQS stores and waits, SNS announces to everyone, EventBridge routes by content — and real systems chain them so each does what it is best at.')
    body += why([
      'The Messaging page showed the shapes. This page compares the three services you will use most, because they overlap and are often confused. The difference is <b>who pulls, who pushes, and who decides where it goes</b>.',
      'AWS\'s guidance in short: SQS persists messages until they are processed or expire. SNS pushes to a wide range of subscribers and does not persist. EventBridge matches events with rules and sends them to targets. FIFO queues and FIFO topics give strict order; EventBridge does not.'])
    body += block('⚖️ Strengths and watch-outs', proscons('📬 SQS',
      ['Messages persist until processed or expired', 'A buffer that absorbs spikes', 'FIFO queues for strict ordering; dead-letter queues for failures'],
      ['Pull-based: consumers must poll', 'One message is handled by one consumer of the queue', 'Standard queues can deliver duplicates, so consumers must be idempotent'])
      + proscons('📣 SNS',
      ['Fan-out to a large number of subscribers', 'Many subscriber types: queues, functions, HTTP, email, SMS, mobile push', 'Per-subscriber filters; FIFO topics available'],
      ['Messages are not persisted', 'Filtering is configured per subscriber, not in one central place'])
      + proscons('🧭 EventBridge',
      ['Rules match events by content and choose targets', 'Central routing for many microservices and sources', 'AWS and SaaS events'],
      ['No message ordering guarantee', 'Delivery to targets is at least once, so duplicates can occur']), label_cls='see')
    body += block('🧭 Which one?', figure(d_choose2(),
        'one consumer that may be slow → <b>SQS</b>. Many subscribers for the same message → <b>SNS</b>. Routing by event content from many sources → <b>EventBridge</b>. And when you need several of those at once, put a topic or bus in front and a queue behind each consumer.'), label_cls='see')
    body += block('☠️ When a message keeps failing', figure(d_dlq(),
        'SQS hides a message for a <b>visibility timeout</b> while a consumer works on it. If the consumer does not delete it in time, it reappears and is retried. If it fails repeatedly, a <b>dead-letter queue</b> catches it so one bad message does not block the rest, and a person can inspect it later.'), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('📧','Email each new user, even if the mail system is slow','Spikes must not fail sign-ups.','SQS in between'),
      ('📢','One order triggers billing, shipping and analytics','Same message, three listeners.','SNS topic with queues behind'),
      ('🧭','Route "refund over a limit" events to a review team','Content-based rule.','EventBridge'),
      ('🏦','Per-account transactions must stay in order','Order matters.','SQS FIFO (or SNS FIFO)'),
      ('☠️','One malformed message crashes the worker','It blocks the queue.','Dead-letter queue'),
      ('🔔','Alert people by SMS and email','Push to people.','SNS'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — what AWS says', '''      <p>AWS describes SQS as pull-based with messages kept until processed or they expire (up to a fixed maximum retention), SNS as push-based with no persistence, and EventBridge as event-driven with rules that match event content and deliver to targets.</p>
      <p>SNS filters are set per subscriber, whereas EventBridge rules are central. AWS suggests SNS when you have a large number of subscribers to a topic, and EventBridge when many topics, subscriptions and filters route messages between microservices.</p>
      <p>Where strict order is required, use SQS FIFO queues or SNS FIFO topics. EventBridge delivers to targets at least once, so design for duplicates.</p>''')
    body += recall([
      'SQS = pull, persists until processed or expired. SNS = push, no persistence. EventBridge = rules route events to targets.',
      'FIFO queues/topics give strict order; EventBridge has no ordering guarantee.',
      'SNS or EventBridge in front, SQS behind each consumer, is the common pattern.',
      'Visibility timeout hides a message during processing; a dead-letter queue catches repeated failures.',
      'Design consumers to be idempotent.'])
    body += saythis('"SQS is a pull-based queue that keeps messages until they are processed; SNS pushes to many subscribers without storing messages; EventBridge routes events by rules. '
      'I combine them — a topic or bus in front, a queue behind each consumer — and use FIFO when order matters, dead-letter queues for poison messages, and idempotent consumers."')
    body += trap([
      '<b>Using SNS where you needed durability.</b> A subscriber that is down misses the message. Subscribe an SQS queue so messages wait.',
      'Second trap: <b>an endless retry loop.</b> A message that always fails keeps returning after the visibility timeout. Set a dead-letter queue.'])
    body += confuse('📬 SQS', 'Consumers pull. The queue keeps the message until it is handled.', '📣 SNS', 'The topic pushes. It does not keep the message; subscribers get it as it happens.')
    body += next_box('That is SQS, SNS and EventBridge. Back to the Messaging page for the big picture — or on to the Kinesis deep dive for streams.', 'messaging.html', 'Back to Messaging')
    body += fact_note(FOOT, [DOCS_DG, DOCS_SQS, DOCS_SNS, DOCS_EB])
    return page('sqs-sns-eventbridge', 'SQS, SNS and EventBridge', 'Deep dive · Messaging · 📨 Queues, topics, buses',
        'SQS stores and waits, SNS announces to everyone, EventBridge routes by content — <span class="grad-text">and real systems chain them.</span>',
        'Pull versus push, ordering, fan-out, filtering, dead-letter queues and the combinations that work.',
        'What is the difference between SQS, SNS and EventBridge?',
        body, CR + ['<a href="messaging.html">Messaging &amp; Events</a>', '<span class="cur">SQS, SNS and EventBridge</span>'], '', search_title='SQS, SNS and EventBridge')

# ------------------------------------------------------ deep dive: Kinesis
def d_shards():
    d = Diagram('kn1', 640, 300, 'Producers write records with a partition key; Kinesis hashes the key to pick a shard, and consumers read each shard in order')
    d.box(10, 110, 110, 64, [('📱 Producers','t'),('write records','s')], 'n')
    d.box(210, 110, 130, 64, [('🔑 Partition key','t'),('hashed','s')], 'amber')
    d.zone(430, 8, 200, 284, 'amber', 'STREAM · shards')
    for i in range(3):
        d.box(446, 48 + i*76, 168, 56, [(f'📦 Shard {i+1}','t'),('ordered records','s')], 'n')
    d.arrow([(120,142),(210,142)], 'amber', label='record', at=(165,142))
    d.arrow([(340,142),(385,142),(385,76),(446,76)], 'amber', label='hash picks', at=(385,108))
    d.arrow([(340,142),(385,142),(385,152),(446,152)], 'amber')
    d.arrow([(340,142),(385,142),(385,228),(446,228)], 'amber')
    return d

def d_consumers():
    d = Diagram('kn2', 640, 280, 'Several consumers each read the same stream at their own position; enhanced fan-out gives a registered consumer its own dedicated throughput')
    d.box(10, 100, 120, 64, [('🌊 Stream','t'),('records kept','s')], 'amber')
    d.box(300, 30, 140, 56, [('📊 Analytics','t'),('reads from here','s')], 'cyan')
    d.box(300, 112, 140, 56, [('🚨 Alerting','t'),('reads from here','s')], 'cyan')
    d.box(300, 194, 140, 56, [('🗃️ Archive','t'),('reads from here','s')], 'cyan')
    d.arrow([(130,120),(215,120),(215,58),(300,58)], 'cyan', label='reads', at=(215,89))
    d.arrow([(130,132),(300,140)], 'cyan')
    d.arrow([(130,144),(215,144),(215,222),(300,222)], 'cyan')
    d.text(540, 120, 'Reading does not delete.', size=9.5, weight=700)
    d.text(540, 138, 'Each consumer keeps', size=9.5)
    d.text(540, 154, 'its own position.', size=9.5)
    return d

def d_choose3():
    d = Diagram('kn3', 640, 346, 'Decision tree: a job for one worker use SQS; many independent readers or replay of ordered events use Kinesis')
    d.box(190, 8, 260, 34, [('🤔 Queue or stream?','t')], 'cyan')
    qs = [
     ('📬 Each item handled once, then gone?', 'a to-do list for workers', 'SQS', 'a queue', 'violet'),
     ('🌊 Many readers, replay, ordered flow?', 'clickstreams, logs, telemetry', 'Kinesis', 'a stream', 'amber'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 272
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 272, 330, 54, [('🤔 Not sure?','t'),('start with SQS — it is simpler','s')], 'emerald')
    return d

def build_kinesis():
    body = ''
    body += see(figure(d_shards(),
        'producers write <b>records</b>, each with a <b>partition key</b>. Kinesis hashes the key to choose a <b>shard</b>, and records on one shard stay in order. A stream is a set of shards. '
        'This is why the key matters: the same key always lands on the same shard, so the order for that key is kept — and a few very busy keys can overload one shard.'))
    body += one('A Kinesis stream is a log of events that many readers can read at their own pace and replay — the right tool when order, volume and several consumers matter.')
    body += why([
      'A queue is a to-do list: one worker takes a task and it is gone. But some data is a <b>flow</b>: clicks, logs, sensor readings. Many different systems want the same flow — one for analytics, one for alerts, one for an archive — and sometimes you need to read it again.',
      'A stream keeps the records for a retention period and lets every consumer read at its own position. <b>Reading does not delete.</b> That is a feature (replay), but it means each consumer must remember where it stopped.'])
    body += block('🧰 The vocabulary', pick_cards([
      dict(icon='🔑', name='Partition key', tag='decides the shard', color='#fbbf24',
           use=['Hashed to choose a shard; same key, same shard, so order is kept per key', 'Pick a key with many distinct values to spread load'],
           skip=['A key with a few values — it overloads some shards']),
      dict(icon='📦', name='Shard', tag='the unit of capacity', color='#a78bfa',
           use=['Each shard has fixed read and write limits', 'More shards, more throughput'],
           skip=['Expecting unlimited speed from one shard']),
      dict(icon='🕰️', name='Retention', tag='how long records are kept', color='#22d3ee',
           use=['Default is 24 hours after creation, extendable up to 365 days', 'Replay inside the window'],
           skip=['Treating the stream as permanent storage']),
      dict(icon='🎚️', name='Capacity modes', tag='on-demand or provisioned', color='#34d399',
           use=['On-demand: Kinesis manages the shard count', 'Provisioned: you set and change the shard count, and can split a hot shard yourself'],
           skip=['On-demand does not isolate a single very hot key — use provisioned for highly uneven keys']),
    ]), label_cls='see')
    body += block('👥 Many readers, one stream', figure(d_consumers(),
        'analytics, alerting and an archive all read the <em>same</em> stream, each at its own position. Standard consumers share the shard\'s read throughput. With <b>enhanced fan-out</b>, a registered consumer gets its own dedicated throughput; there is a limit on how many consumers can be registered, which depends on the capacity mode.'), label_cls='see')
    body += block('🧭 Queue or stream?', figure(d_choose3(),
        'if each item is handled once and then gone, use <b>SQS</b>. If many readers need the same ordered flow, or you need to replay, use <b>Kinesis</b>. When unsure, start with SQS: it is simpler.'), label_cls='see')
    body += block('📊 Queue vs stream', table(['','SQS queue','Kinesis stream'], [
      ['Reading','Message is removed once processed','Records stay until retention ends'],
      ['Readers','Consumers share the work','Each consumer reads everything, at its own position'],
      ['Order','FIFO queues; standard queues do not guarantee it','Per shard, by partition key'],
      ['Replay','No','Yes, within retention'],
      ['Scaling','Managed by the service','By shards, in provisioned or on-demand mode'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🖱️','Website clicks, millions a minute','Analytics, alerts and an archive all need them.','Kinesis Data Streams'),
      ('🧾','Every record for one customer must stay in order','Same key, same shard.','Use the customer ID as the partition key'),
      ('🔁','A bug corrupted yesterday\'s results','You need to reprocess.','Replay the stream within retention'),
      ('🔥','One celebrity account gets most of the traffic','A hot key overloads a shard.','Provisioned mode and shard splitting, or a better key'),
      ('📬','Resize each uploaded image once','A to-do item, handled once.','SQS, not Kinesis'),
      ('🧪','Not sure which to use','Start simple.','SQS first'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — limits and modes', '''      <p><b>Shard limits.</b> Each shard has fixed limits for writes (a records-per-second and a megabytes-per-second cap) and for reads. Check the current numbers in the developer guide; they differ by mode and change over time.</p>
      <p><b>Hot shards.</b> Uneven partition keys can still cause throttling. Provisioned mode lets you split a hot shard manually. On-demand mode spreads evenly and does not detect and isolate a hot hash key.</p>
      <p><b>Retention.</b> The default retention is 24 hours, extendable up to 365 days.</p>
      <p><b>Consumers.</b> Standard consumers use shared read throughput; enhanced fan-out gives registered consumers dedicated throughput, with a cap on registered consumers that depends on the mode.</p>''')
    body += recall([
      'A stream is a replayable ordered log; reading does not delete.',
      'Partition key → hashed → shard; same key, same shard, ordered per key.',
      'Retention: 24 hours by default, up to 365 days.',
      'On-demand vs provisioned capacity; provisioned lets you split a hot shard.',
      'Queue for one-time jobs; stream for many readers and replay.'])
    body += saythis('"A Kinesis stream is a replayable log. Producers choose a partition key that hashes to a shard, so order is kept per key. Records stay for the retention period, many consumers read at their own position, and enhanced fan-out gives a consumer dedicated throughput. '
      'I use SQS for one-time jobs and Kinesis when many readers or replay matter, and I watch for hot shards."')
    body += trap([
      '<b>A bad partition key.</b> Using a key with few values sends most records to a few shards, which throttle while others sit idle.',
      'Second trap: <b>forgetting that reading does not delete.</b> Each consumer must track its own position, and records disappear when retention ends.'])
    body += confuse('📬 SQS', 'A to-do list: one consumer takes an item and it is gone.', '🌊 Kinesis', 'A log: every consumer can read everything, at its own pace, and replay it.')
    body += next_box('That is Kinesis. Back to the Messaging page for the big picture — and on to the next concept: Serverless &amp; Orchestration.', 'messaging.html', 'Back to Messaging')
    body += fact_note(FOOT, [DOCS_KDS, DOCS_KEY, DOCS_MODE])
    return page('kinesis', 'Kinesis Data Streams', 'Deep dive · Messaging · 🌊 Kinesis',
        'A Kinesis stream is a log many readers can read at their own pace — <span class="grad-text">the right tool when order, volume and replay matter.</span>',
        'Shards, partition keys, retention, capacity modes and enhanced fan-out: when a stream beats a queue.',
        'What is Kinesis Data Streams, and when would you choose it over SQS?',
        body, CR + ['<a href="messaging.html">Messaging &amp; Events</a>', '<span class="cur">Kinesis Data Streams</span>'], '', search_title='Kinesis Data Streams')
