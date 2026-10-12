from kit import *
from p_common import CR

DOCS_VPC = ('Amazon VPC user guide', 'https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html')
DOCS_HOW = ('How Amazon VPC works', 'https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html')
DOCS_SG = ('Security groups', 'https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html')
DOCS_NACL = ('Network ACLs', 'https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html')
DOCS_PEER = ('VPC peering', 'https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html')
DOCS_TGW = ('AWS Transit Gateway', 'https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html')
DOCS_PL = ('AWS PrivateLink and VPC endpoints', 'https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html')
FOOT = 'Cloud services change often. This page teaches the ideas; for exact limits, prices and new features, check the official AWS docs.'

def d_vpc():
    d = Diagram('vp1', 640, 360, 'A VPC with a public subnet that has a route to the internet gateway and a private subnet that reaches the internet only outbound through a NAT gateway')
    d.box(220, 6, 200, 34, [('🌐 Internet','t')], 'n')
    d.box(220, 66, 200, 34, [('🚪 Internet gateway','t')], 'cyan')
    d.arrow([(320,40),(320,66)], 'cyan', label='in and out', at=(405,53), both=True)
    d.zone(10, 124, 620, 228, 'n', 'VPC · your private network')
    d.zone(24, 150, 592, 76, 'emerald', 'PUBLIC SUBNET')
    d.zone(24, 252, 592, 88, 'violet', 'PRIVATE SUBNET')
    d.box(60, 176, 200, 40, [('🖥️ Web server','t')], 'emerald')
    d.box(380, 176, 200, 40, [('🔁 NAT gateway','t')], 'amber')
    d.box(60, 280, 200, 44, [('⚙️ App server','t')], 'violet')
    d.box(380, 280, 200, 44, [('🗄️ Database','t')], 'violet')
    d.arrow([(160,216),(160,280)], 'emerald', label='calls', at=(200,248))
    d.arrow([(200,176),(200,128),(260,128),(260,100)], 'cyan', label='web', at=(230,128))
    d.arrow([(230,280),(230,238),(440,238),(440,216)], 'amber', label='outbound only', at=(335,238))
    d.arrow([(260,302),(380,302)], 'violet', label='reads', at=(320,302))
    d.arrow([(480,176),(480,88),(420,88)], 'amber', label='to the internet', at=(480,112))
    return d

def d_sg():
    d = Diagram('vp2', 640, 292, 'A security group is stateful so replies need no rule; a network ACL is stateless so every packet is checked in both directions')
    d.zone(10, 8, 305, 276, 'emerald', 'SECURITY GROUP · around a resource')
    d.box(24, 84, 70, 60, [('👤 Client','t')], 'n')
    d.box(210, 84, 90, 60, [('🖥️ Server','t'),('protected','s')], 'emerald')
    d.arrow([(94,102),(210,102)], 'emerald', label='request in', at=(152,102))
    d.arrow([(210,126),(94,126)], 'emerald', label='reply: auto', at=(152,126))
    d.text(162, 192, 'Stateful: it remembers the request,', size=9.5)
    d.text(162, 208, 'so the reply needs no rule.', size=9.5)
    d.text(162, 232, 'Allow rules only.', size=9.5, weight=700)
    d.zone(325, 8, 305, 276, 'amber', 'NETWORK ACL · around a subnet')
    d.box(339, 84, 70, 60, [('👤 Client','t')], 'n')
    d.box(525, 84, 90, 60, [('📦 Subnet','t'),('protected','s')], 'amber')
    d.arrow([(409,102),(525,102)], 'amber', label='rules checked', at=(467,102))
    d.arrow([(525,126),(409,126)], 'amber', label='checked again', at=(467,126))
    d.text(477, 192, 'Stateless: every packet is checked,', size=9.5)
    d.text(477, 208, 'so replies need their own rule.', size=9.5)
    d.text(477, 232, 'Allow and deny; rules in order.', size=9.5, weight=700)
    return d

def d_connect():
    d = Diagram('vp3', 640, 312, 'VPC peering connects two VPCs one-to-one and does not pass traffic through a middle VPC, while a transit gateway is a hub that connects many VPCs')
    d.zone(10, 8, 305, 296, 'rose', 'PEERING · one-to-one, not transitive')
    d.box(100, 44, 100, 44, [('🕸️ VPC A','t')], 'n')
    d.box(100, 124, 100, 44, [('🕸️ VPC B','t')], 'n')
    d.box(100, 204, 100, 44, [('🕸️ VPC C','t')], 'n')
    d.arrow([(150,88),(150,124)], 'cyan', label='peering', at=(225,106), both=True)
    d.arrow([(150,168),(150,204)], 'cyan', label='peering', at=(225,186), both=True)
    d.arrow([(200,66),(270,66),(270,226),(200,226)], 'rose', label='no transit', at=(270,146), dash=True)
    d.text(162, 272, 'A cannot reach C through B.', size=9.5, weight=700)
    d.zone(325, 8, 305, 296, 'emerald', 'TRANSIT GATEWAY · a hub')
    d.box(340, 44, 100, 44, [('🕸️ VPC A','t')], 'n')
    d.box(340, 124, 100, 44, [('🕸️ VPC B','t')], 'n')
    d.box(340, 204, 100, 44, [('🕸️ VPC C','t')], 'n')
    d.box(520, 104, 100, 84, [('🔀 Transit','t'),('Gateway','t'),('the hub','s')], 'emerald')
    d.arrow([(440,66),(480,66),(480,125),(520,125)], 'emerald', label='attach', at=(480,96))
    d.arrow([(440,146),(520,146)], 'emerald', label='attach', at=(480,146))
    d.arrow([(440,226),(480,226),(480,167),(520,167)], 'emerald', label='attach', at=(480,196))
    d.text(477, 272, 'Any attached network can reach the others.', size=9.5, weight=700)
    return d

def build_vpc_networking():
    body = ''
    body += see(figure(d_vpc(),
        'a <b>VPC</b> is your own private network inside AWS. You cut it into <b>subnets</b>. A <b>public subnet</b> has a route to the <b>internet gateway</b>, so things in it (like a web server) can be reached from the internet. A <b>private subnet</b> has no route in from the internet — the app and the database live there. '
        'If a private server needs to reach out (to download updates, say), it goes through a <b>NAT gateway</b> that allows outbound connections and blocks unsolicited inbound ones.'))
    body += one('A VPC is your own walled network in AWS — and what lives in a public or private subnet, and which rules guard it, decides what can reach what.')
    body += why([
      'IAM says who may call what. But before any caller arrives, there is a more basic question: can the packet even get there? A database that the whole internet can reach is a problem no policy fixes after the fact. <b>Networking decides what can physically reach what.</b>',
      'So resources get a <b>VPC</b>: an isolated network you define, with <b>subnets</b> in specific Availability Zones, <b>route tables</b> that decide where traffic goes, and <b>firewalls</b> at two levels. The habit to build: put only what must be public in a public subnet — and everything else in a private one.'])
    body += block('🧰 The pieces', pick_cards([
      dict(icon='🕸️', name='VPC and subnets', tag='your network, cut into pieces', color='#22d3ee',
           use=['A VPC is your isolated network; a subnet lives in one Availability Zone', 'Make several subnets across zones for resilience', 'Public subnet = a route to the internet gateway; private = no direct route'],
           skip=['Putting databases in a public subnet "to make it easy"']),
      dict(icon='🧭', name='Route tables, internet gateway, NAT gateway', tag='where traffic goes', color='#fbbf24',
           use=['A route table pairs a destination range with a target', 'Internet gateway: lets public resources talk to the internet', 'NAT gateway: private resources start outbound connections; unsolicited inbound is blocked'],
           skip=['Expecting a NAT gateway to let the internet in — it does not']),
      dict(icon='🛡️', name='Security groups', tag='a firewall around a resource', color='#34d399',
           use=['Your main tool: allow rules only, stateful', 'Reference another security group as the source ("only the web tier")'],
           skip=['Trying to write a deny rule — security groups only allow']),
      dict(icon='🚧', name='Network ACLs', tag='a firewall around a subnet', color='#a78bfa',
           use=['Stateless, with allow and deny rules checked in order', 'AWS suggests them as a secondary control or subnet-level guardrails'],
           skip=['Forgetting the reply rule — stateless means replies need their own rule']),
    ]), label_cls='see')
    body += block('🛡️ Two firewalls, two behaviours', figure(d_sg(),
        'a <b>security group</b> (left) is <em>stateful</em>: if it let the request in, the reply goes out without another rule. It only has <em>allow</em> rules, and AWS evaluates all of them. A <b>network ACL</b> (right) is <em>stateless</em>: every packet in each direction is checked, so replies need their own rule. '
        'It has allow and deny rules, checked in number order until one matches. In most cases security groups are enough; ACLs add a layer.'), label_cls='see')
    body += block('🔗 Connecting networks', figure(d_connect(),
        'when one VPC is not enough, you connect them. <b>VPC peering</b> (left) joins exactly two VPCs and is not transitive: A↔B and B↔C does not give A↔C, and a VPN or Direct Connect on one VPC cannot be borrowed by its peer. With many VPCs the peerings pile up. '
        'A <b>transit gateway</b> (right) is a hub: you attach each VPC, and the hub routes between them, including to VPNs and Direct Connect.'), label_cls='see')
    body += block('📊 Side by side', table(['','Level','Stateful?','Rules','Use it for'], [
      ['🛡️ Security group','A resource (like an instance)','Yes','Allow only','Your main firewall; reference other groups'],
      ['🚧 Network ACL','A subnet','No','Allow and deny, in order','Subnet-level guardrails, explicit blocks'],
      ['🔁 NAT gateway','A subnet\'s outbound path','—','—','Private servers that must reach out'],
      ['🔗 Peering','Two VPCs','—','—','A few VPCs that need to talk directly'],
      ['🔀 Transit gateway','Many VPCs and on-premises links','—','Route tables','A growing hub-and-spoke network'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('🛒','A public website with a database','The database must not face the internet.','Web tier in public subnets, database in private subnets'),
      ('📦','Private servers must download updates','But nobody may connect in.','A NAT gateway'),
      ('🧱','Only the web tier may reach the app tier','Not the whole network.','A security group that allows the web tier\'s group'),
      ('🚫','Block one bad address range right now','An explicit deny.','A network ACL rule'),
      ('🔗','Two teams\' VPCs need to talk','Just those two.','VPC peering'),
      ('🏢','Thirty VPCs and a data center','Peering would be a mess.','A transit gateway'),
    ]), label_cls='see')
    body += block('🔬 Go deeper', deep_cards([('Deep dive · VPC', 'VPC Endpoints: reaching AWS services privately', 'How private subnets reach S3, DynamoDB and other AWS services without going out to the internet: gateway endpoints, interface endpoints and PrivateLink.', 'vpc-endpoints.html')]), label_cls='next')
    body += zoom('Go one level deeper (60 seconds) — what AWS says', '''      <p>A public subnet has a direct route to an internet gateway; a private subnet does not, so its resources need a NAT device to reach the internet. A route table holds routes; each route pairs a destination range with a target such as a gateway.</p>
      <p>Security groups act at the resource level and are stateful; network ACLs act at the subnet level and are stateless. AWS suggests using network ACLs as a secondary control or high-level subnet guardrails, because security groups meet most needs.</p>
      <p>VPC peering is point-to-point and does not support transitive routing. For a full mesh of many VPCs you would need a huge number of peerings, so AWS points to Transit Gateway, which supports transitive routing and can attach VPNs and Direct Connect.</p>
      <p><b>Spread across zones.</b> A subnet lives in a single Availability Zone, so make subnets in several zones and put copies of your app in each (concept 2).</p>
      <p><b>Pricing.</b> NAT gateways and some connectivity options are billed by the hour and by data processed; check the pricing page before you design around many of them.</p>''')
    body += recall([
      'VPC = your isolated network; subnets live in one AZ. Public subnet = route to an internet gateway; private = no direct route.',
      'NAT gateway lets private resources start outbound connections and blocks unsolicited inbound ones.',
      'Security group: resource-level, stateful, allow rules only. Network ACL: subnet-level, stateless, allow and deny, rules in order.',
      'Peering is one-to-one and not transitive; a transit gateway is a hub with transitive routing.',
      'Only what must be public goes in a public subnet; databases go in private subnets.'])
    body += saythis('"I build a VPC with subnets in several Availability Zones. Anything that must face the internet sits in a public subnet with a route to the internet gateway; apps and databases sit in private subnets, with a NAT gateway for outbound-only access. '
      'Security groups are my main firewall — stateful, allow-only — and network ACLs are a stateless subnet-level layer. For many VPCs I use a transit gateway, because peering is not transitive."')
    body += trap([
      '<b>Putting the database in a public subnet.</b> Even with a good password, you have made it reachable by the world. A private subnet takes it off the map.',
      'Second trap: <b>writing network ACL rules for one direction.</b> They are stateless, so the reply traffic needs its own rule. Most "it works in a security group but not here" bugs are this.'])
    body += confuse('🛡️ Security group', 'Around a resource. Stateful and allow-only. Your everyday firewall.', '🚧 Network ACL', 'Around a subnet. Stateless, with allow and deny rules in order. An extra layer.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># create a VPC and one subnet inside it</span>
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 create-subnet --vpc-id &lt;vpc-id&gt; --cidr-block 10.0.1.0/24 --availability-zone eu-west-1a''',
      'Illustrative shape only — the address ranges, Region and zone are examples, and a real network also needs route tables, gateways and firewall rules.'))
    body += next_box('The network is ready. Now your code needs somewhere to <b>run</b> — and how much of the machine you manage (a server, a container, a function) is the first big trade-off. Next: Compute.', 'compute.html', 'Compute')
    body += fact_note(FOOT, [DOCS_VPC, DOCS_HOW, DOCS_SG, DOCS_NACL, DOCS_PEER, DOCS_TGW])
    return page('vpc-networking', 'VPC Networking', 'Concept 4 of 19 · 🏗️ Foundations',
        'A VPC is your own walled network in AWS — <span class="grad-text">and the subnet a resource sits in decides what can reach it.</span>',
        'VPCs, subnets, route tables, internet and NAT gateways, security groups, network ACLs, peering and transit gateways: how to keep private things private.',
        'How would you design a VPC for a web app with a database on AWS?',
        body, CR + ['<span class="cur">VPC Networking</span>'], '', search_title='VPC Networking')

# ------------------------------------------------------------------ deep dive: VPC endpoints
def d_path():
    d = Diagram('ve1', 640, 292, 'Without an endpoint a private server reaches S3 over the NAT gateway and the internet gateway; with an endpoint the traffic stays on the AWS network')
    d.zone(10, 8, 305, 276, 'rose', 'WITHOUT AN ENDPOINT')
    d.box(24, 40, 120, 44, [('⚙️ Private app','t')], 'violet')
    d.box(24, 120, 120, 44, [('🔁 NAT gateway','t')], 'amber')
    d.box(24, 200, 120, 44, [('🚪 Internet gw','t')], 'cyan')
    d.box(230, 200, 70, 44, [('🪣 S3','t')], 'emerald')
    d.arrow([(84,84),(84,120)], 'rose', label='out', at=(130,102))
    d.arrow([(84,164),(84,200)], 'rose', label='out', at=(130,182))
    d.arrow([(144,222),(230,222)], 'rose', label='public', at=(187,222))
    d.text(235, 120, 'Leaves your VPC, uses', size=9.5)
    d.text(235, 136, 'the NAT gateway and', size=9.5)
    d.text(235, 152, 'the internet path.', size=9.5)
    d.zone(325, 8, 305, 276, 'emerald', 'WITH AN ENDPOINT')
    d.box(339, 40, 120, 44, [('⚙️ Private app','t')], 'violet')
    d.box(339, 120, 120, 44, [('🔌 VPC endpoint','t')], 'emerald')
    d.box(515, 200, 100, 44, [('🪣 S3','t')], 'emerald')
    d.arrow([(399,84),(399,120)], 'emerald', label='private', at=(449,102))
    d.arrow([(459,142),(565,142),(565,200)], 'emerald', label='AWS network', at=(520,142))
    d.text(477, 262, 'No internet path, no NAT gateway needed.', size=9.5, weight=700)
    return d

def d_types():
    d = Diagram('ve2', 640, 292, 'A gateway endpoint adds a route in your route table for S3 and DynamoDB; an interface endpoint puts a network interface with a private IP in your subnet')
    d.zone(10, 8, 305, 276, 'cyan', 'GATEWAY ENDPOINT · S3 and DynamoDB only')
    d.box(24, 70, 100, 50, [('🧭 Route table','t')], 'amber')
    d.box(210, 70, 90, 50, [('🪣 S3 or','t'),('DynamoDB','t')], 'emerald')
    d.arrow([(124,95),(210,95)], 'cyan', label='route', at=(167,95))
    d.text(162, 168, 'A route that points at the service.', size=9.5)
    d.text(162, 184, 'No extra charge for the endpoint.', size=9.5)
    d.text(162, 208, 'Only works from inside this VPC.', size=9.5, weight=700)
    d.zone(325, 8, 305, 276, 'violet', 'INTERFACE ENDPOINT · many services (PrivateLink)')
    d.box(339, 70, 100, 50, [('🔌 Network','t'),('interface','s')], 'violet')
    d.box(545, 70, 75, 50, [('☁️ AWS','t'),('service','s')], 'emerald')
    d.arrow([(439,95),(545,95)], 'violet', label='PrivateLink', at=(492,95))
    d.text(477, 168, 'A private IP address in your subnet.', size=9.5)
    d.text(477, 184, 'Billed by the hour plus data.', size=9.5)
    d.text(477, 208, 'Reachable from on-premises and peered VPCs.', size=9.5, weight=700)
    return d

def d_choose_ep():
    d = Diagram('ve3', 640, 336, 'Decision tree: gateway endpoint for S3 or DynamoDB from inside the VPC, interface endpoint for other services or for access from outside the VPC')
    d.box(190, 8, 260, 34, [('🤔 Reaching an AWS service?','t')], 'cyan')
    qs = [
     ('🪣 S3 or DynamoDB, from inside this VPC?', 'the simple, free-to-run case', 'Gateway endpoint', 'a route in the route table', 'emerald'),
     ('🔌 Another service, or from on-premises?', 'or from a peered VPC or transit gateway', 'Interface endpoint', 'private IP via PrivateLink', 'violet'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 272
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 272, 330, 54, [('🌐 Neither?','t'),('the service stays reachable over the internet path','s')], 'n')
    return d

def build_vpc_endpoints():
    body = ''
    body += see(figure(d_path(),
        'a private server that talks to S3 has two ways to get there. <b>Without an endpoint</b> (left) the traffic leaves the VPC through a NAT gateway and the internet gateway — it works, but it uses the internet path and costs NAT charges. '
        '<b>With a VPC endpoint</b> (right) the traffic goes privately to the service over the AWS network. The server stays in a private subnet and nothing needs to be exposed.'))
    body += one('A VPC endpoint is a private door from your network to an AWS service — so private subnets can use S3, DynamoDB and more without ever going out to the internet.')
    body += why([
      'The VPC page put databases and apps in private subnets and gave them a NAT gateway for outbound access. But much of what private servers call is <b>AWS itself</b>: storage, queues, secrets. Sending that traffic through a NAT gateway and out to the internet is slower to reason about, costs money, and widens what must be allowed out.',
      'A <b>VPC endpoint</b> keeps that traffic inside AWS. There are two kinds that work differently, and choosing between them is the whole skill.'])
    body += block('🧰 The two kinds', pick_cards([
      dict(icon='🚪', name='Gateway endpoint', tag='S3 and DynamoDB only', color='#34d399',
           use=['You are reaching S3 or DynamoDB from inside the VPC', 'Routes are added to the route tables you choose', 'No additional cost for the endpoint'],
           skip=['Reaching them from on-premises, from a peered VPC in another Region or through a transit gateway — it does not reach those']),
      dict(icon='🔌', name='Interface endpoint', tag='built on AWS PrivateLink', color='#a78bfa',
           use=['Many AWS services (and services shared by others through PrivateLink)', 'A network interface with a private IP in your subnet', 'Reachable from on-premises over VPN or Direct Connect, and from peered VPCs or transit gateways'],
           skip=['Cost-sensitive S3 traffic from inside the VPC — a gateway endpoint is free to run']),
    ]), label_cls='see')
    body += block('🔍 How they differ', figure(d_types(),
        'a <b>gateway endpoint</b> (left) is a target in your <em>route table</em>: traffic to S3 or DynamoDB is routed to it. It exists only for those two services, has no extra charge, and works only inside the VPC. '
        'An <b>interface endpoint</b> (right) is an actual network interface with a private IP address from your subnet, using PrivateLink. It supports many services, is billed hourly plus per data processed, and can be reached from on-premises and from peered networks.'), label_cls='see')
    body += block('🧭 Which one?', figure(d_choose_ep(),
        'for S3 or DynamoDB from inside the VPC, use a <b>gateway endpoint</b>. For other services, or when access must come from on-premises, a peered VPC or a transit gateway, use an <b>interface endpoint</b>. '
        'You can use both for S3 in the same VPC: private DNS can send in-VPC traffic through the free gateway endpoint while on-premises traffic uses the interface endpoint, which can lower costs.'), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('📦','Private servers upload to S3 all day','NAT data charges add up.','A gateway endpoint for S3'),
      ('📚','A private app reads a DynamoDB table','No internet path is wanted.','A gateway endpoint for DynamoDB'),
      ('🔑','Private servers read secrets from a secrets service','Not an S3 or DynamoDB service.','An interface endpoint'),
      ('🏢','The office network must reach S3 privately','Over VPN or Direct Connect.','An interface endpoint for S3'),
      ('🧪','Both inside the VPC and on-premises use S3','Keep costs down inside.','Both endpoint types, with private DNS'),
      ('🛡️','Only some buckets should be reachable','Limit what the door allows.','An endpoint policy'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — details to know', '''      <p><b>Gateway endpoints</b> work only with S3 and DynamoDB and do not use PrivateLink. They add routes to route tables you associate with the endpoint, and have no additional cost. They do not extend to on-premises networks, to peered VPCs in other Regions or to transit gateways.</p>
      <p><b>Interface endpoints</b> use AWS PrivateLink and elastic network interfaces with private IP addresses from your subnets. You pay an hourly charge while the endpoint runs, plus data processing.</p>
      <p><b>Endpoint policies</b> can restrict what an endpoint may be used for, adding one more guardrail next to IAM and bucket policies.</p>
      <p><b>Security groups</b> attach to interface endpoints, so you can control which of your resources may use them.</p>''')
    body += recall([
      'VPC endpoint = a private path from your VPC to an AWS service, without the internet or a NAT gateway.',
      'Gateway endpoint: S3 and DynamoDB only, a route in the route table, no extra charge, VPC-only.',
      'Interface endpoint: PrivateLink, a network interface with a private IP, many services, hourly plus data charges, reachable from on-premises and peered VPCs.',
      'You can use both for S3 in one VPC.',
      'Endpoints do not replace IAM or bucket policies — they add a network-level guardrail.'])
    body += saythis('"For private subnets I use VPC endpoints so AWS traffic does not go out through a NAT gateway. For S3 and DynamoDB inside the VPC a gateway endpoint is a route table entry with no extra charge. '
      'For other services, or when access comes from on-premises or a peered network, I use interface endpoints, which are PrivateLink network interfaces billed by the hour and by data."')
    body += trap([
      '<b>Assuming a gateway endpoint reaches from on-premises.</b> It does not; it works only from inside the VPC. For on-premises access use an interface endpoint.',
      'Second trap: <b>thinking an endpoint replaces permissions.</b> It only changes the network path. IAM and resource policies still decide who may do what.'])
    body += confuse('🚪 Gateway endpoint', 'A route-table target for S3 and DynamoDB. Free to run, VPC-only.', '🔌 Interface endpoint', 'A network interface with a private IP, via PrivateLink. More services and reach, billed by hour and data.')
    body += zoom('💻 Tiny illustrative example', code_block(
'''<span class="cmt"># create a gateway endpoint for S3 and attach it to a route table</span>
aws ec2 create-vpc-endpoint --vpc-id &lt;vpc-id&gt; --service-name com.amazonaws.eu-west-1.s3 \\
    --route-table-ids &lt;rtb-id&gt;''',
      'Illustrative shape only — the Region in the service name is an example, and flags and endpoint types vary by service.'))
    body += next_box('That is how private subnets reach AWS services. Back to the VPC page for the whole map — and on to the next concept: Compute.', 'vpc-networking.html', 'Back to VPC Networking')
    body += fact_note(FOOT, [DOCS_PL, DOCS_VPC, DOCS_NACL])
    return page('vpc-endpoints', 'VPC Endpoints', 'Deep dive · VPC · 🔌 Endpoints',
        'A VPC endpoint is a private door from your network to an AWS service — <span class="grad-text">so private subnets never need the internet to reach AWS.</span>',
        'Gateway endpoints for S3 and DynamoDB, interface endpoints with PrivateLink, and how to choose between them.',
        'What is a VPC endpoint, and what is the difference between a gateway and an interface endpoint?',
        body, CR + ['<a href="vpc-networking.html">VPC Networking</a>', '<span class="cur">VPC Endpoints</span>'], '', search_title='VPC Endpoints')
