from kit import *
from p_common import CR

FOOT = 'AI tooling changes fast. This page teaches the decision, not product features; check the current docs of the model provider you use.'

def d_choose():
    d = Diagram('ch1', 640, 470, 'Decision tree: change the instruction use prompting, supply missing or private facts use RAG, change behaviour that must stick use fine-tuning')
    d.box(190, 8, 260, 34, [('🤔 What is going wrong?','t')], 'cyan')
    qs = [
     ('💬 The answer is fine, the instruction is vague?', 'wrong tone, format or steps', 'Prompting', 'rewrite the instruction', 'cyan'),
     ('📚 The model lacks the facts?', 'private, new or fast-changing data', 'RAG', 'retrieve, then answer', 'emerald'),
     ('🎯 The behaviour must hold every time?', 'a style or skill prompts cannot hold', 'Fine-tuning', 'train it into the weights', 'violet'),
    ]
    d.arrow([(320,42),(320,63),(175,63),(175,84)], 'cyan', label='check in order', at=(247,63))
    for i,(q,qs_,a,as_,col) in enumerate(qs):
        y = 84 + i*94
        d.box(10, y, 330, 54, [(q,'t'),(qs_,'s')], 'n')
        d.box(410, y, 220, 54, [(a,'t'),(as_,'s')], col)
        d.arrow([(340,y+27),(410,y+27)], col, label='yes', at=(375,y+27))
        nxt = y + 94 if i+1 < len(qs) else 372
        d.arrow([(175,y+54),(175,nxt)], 'n', label='no', at=(199,y+72))
    d.box(10, 372, 330, 80, [('🤝 Often you combine them','t'),('prompt for the task, RAG for the facts,','s'),('fine-tune only what still will not hold','s')], 'emerald')
    return d

def d_cost():
    d = Diagram('ch2', 640, 250, 'Effort and permanence rise from prompting to RAG to fine-tuning')
    d.box(10, 50, 190, 90, [('💬 Prompting','t'),('minutes to try','s'),('lasts one request','s')], 'cyan')
    d.box(225, 50, 190, 90, [('📚 RAG','t'),('needs a knowledge base','s'),('facts stay current','s')], 'emerald')
    d.box(440, 50, 190, 90, [('🎯 Fine-tuning','t'),('needs examples + training','s'),('built into the weights','s')], 'violet')
    d.arrow([(105,140),(105,184),(535,184),(535,140)], 'n', label='more effort, more permanent', at=(320,184))
    d.text(320, 230, 'Start on the left; move right only when the left cannot do the job.', size=9.5, weight=700)
    return d

def build_prompt_rag_or_fine_tune():
    body = ''
    body += see(figure(d_choose(),
        'ask <b>what is actually going wrong</b>. If the model has the knowledge but the instruction is vague, fix the <b>prompt</b>. If it lacks the facts — private, new, changing — add <b>RAG</b>. If a behaviour must hold every time and prompts cannot keep it there, consider <b>fine-tuning</b>. '
        'Most real systems end up combining them.'))
    body += one('Prompting changes the instruction, RAG changes the facts the model sees, fine-tuning changes the model itself — pick the lightest one that fixes the real problem.')
    body += why([
      'Three pages in a row gave you three tools. The mistake teams make is reaching for the heaviest one first: fine-tuning a model to teach it facts that RAG would supply, or building retrieval to fix what a clearer prompt would have solved.',
      'The decision comes down to <b>what is missing</b>: clarity (prompt), knowledge (RAG) or built-in behaviour (fine-tune). Name the gap first, then pick the tool.'])
    body += block('🧰 The three tools', pick_cards([
      dict(icon='💬', name='Prompting', tag='change the instruction', color='#22d3ee',
           use=['Wrong tone, format or steps', 'You can describe what you want in words', 'You want to try ideas in minutes'],
           skip=['The model simply does not have the facts', 'The behaviour must persist without being re-asked']),
      dict(icon='📚', name='RAG', tag='supply the facts at question time', color='#34d399',
           use=['Private, new or fast-changing information', 'Answers should point to source documents', 'The knowledge base is too big to paste in'],
           skip=['The knowledge base does not contain the answer — RAG cannot invent it', 'The problem is style, not facts']),
      dict(icon='🎯', name='Fine-tuning', tag='change the weights', color='#a78bfa',
           use=['A consistent tone or format that prompts cannot hold', 'A narrow skill shown best by many examples', 'You have good examples of the exact behaviour'],
           skip=['You mainly need current facts — use RAG', 'You have few or poor examples']),
    ]), label_cls='see')
    body += block('📏 Effort and permanence', figure(d_cost(),
        'the three sit on a line. <b>Prompting</b> is quick but lasts one request. <b>RAG</b> needs a knowledge base and keeps facts current without touching the model. <b>Fine-tuning</b> needs examples and a training run, and the result is built into the weights. Move right only when the left cannot do the job.'), label_cls='see')
    body += block('📊 Side by side', table(['','Fixes','Changes the model?','Facts stay current?','Typical first signal'], [
      ['💬 Prompting','Unclear instructions','No','Only what you paste in','Outputs are close but off in tone or format'],
      ['📚 RAG','Missing or private knowledge','No','Yes, update the knowledge base','Answers are confidently wrong about your data'],
      ['🎯 Fine-tuning','Behaviour that must be built in','Yes, the weights','No — facts are frozen at training','Prompts keep drifting on style or format'],
    ]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
      ('📝','Summaries come out too long','The model knows enough; the instruction is loose.','Prompting'),
      ('🏢','A bot must answer from this week\'s HR policy','The model never saw it, and it changes.','RAG'),
      ('🗣️','Every reply must follow a strict brand voice','Long prompts still drift.','Fine-tuning (after trying prompting)'),
      ('🧾','Support answers need policy facts and a fixed format','Two different gaps.','RAG for facts + prompt for format'),
      ('⚖️','Answers must cite the source document','You need traceability.','RAG'),
      ('🧪','Not sure which one you need','Cheap tests first.','Start with prompting and measure'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds) — how to decide with evidence', '''      <p><b>Measure first.</b> Build a small test set (see Evaluation, concept 17) before you change anything. Without it you cannot tell whether a prompt change, a retrieval change or a fine-tune actually helped.</p>
      <p><b>Look at the failures.</b> If the failing answers contain wrong facts, think RAG. If they contain the right facts in the wrong shape, think prompt or fine-tune. If retrieval returns the wrong documents, fix retrieval before blaming the model.</p>
      <p><b>Fine-tuning is not for facts.</b> It shapes behaviour from examples; it is a poor and costly way to keep knowledge current.</p>''')
    body += recall([
      'Prompting = change the instruction. RAG = supply facts at question time. Fine-tuning = change the weights.',
      'Name the gap first: clarity, knowledge or built-in behaviour.',
      'Start light (prompting), move right only when needed, and measure each step.',
      'RAG cannot invent facts the knowledge base lacks; fine-tuning is not a good way to teach changing facts.',
      'Real systems combine them.'])
    body += saythis('"I decide by what is missing. If the instruction is unclear I improve the prompt; if the model lacks private or current facts I add RAG; if a behaviour must hold every time and prompts cannot keep it there, I consider fine-tuning. '
      'I start with the lightest option, measure with a test set, and combine them when the problem has more than one gap."')
    body += trap([
      '<b>Fine-tuning to add facts.</b> It is slow to update and the facts go stale. If the problem is knowledge, retrieval fits better.',
      'Second trap: <b>skipping measurement.</b> Without a test set you will "fix" things that were fine and miss things that broke.'])
    body += confuse('📚 RAG', 'Adds knowledge at question time. The model stays the same.', '🎯 Fine-tuning', 'Changes behaviour permanently. Facts freeze at training time.')
    body += next_box('That is the choice between the three tools. Back to Fine-tuning for the full picture — and on to the next concept: Agents.', 'fine-tuning.html', 'Back to Fine-tuning')
    body += f'  <p class="fact-note">📌 {FOOT}</p>\n'
    return page('prompt-rag-or-fine-tune', 'Prompting, RAG or Fine-tuning?', 'Deep dive · Fine-tuning · ⚖️ Choosing',
        'Prompting changes the instruction, RAG changes the facts, fine-tuning changes the model — <span class="grad-text">pick the lightest one that fixes the real problem.</span>',
        'A decision tree, a side-by-side table and six real scenarios for the choice every AI builder faces.',
        'When would you use prompting, RAG or fine-tuning?',
        body, CR + ['<a href="fine-tuning.html">Fine-tuning</a>', '<span class="cur">Prompting, RAG or Fine-tuning?</span>'], '', search_title='Prompting, RAG or Fine-tuning?')
