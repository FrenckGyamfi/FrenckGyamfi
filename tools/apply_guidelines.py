"""Applies the 8-dimension positioning to index.html: when to call, a named first engagement,
a repeatable method with clear expectations and handover, and the four client outcomes."""
import re, sys
p = sys.argv[1]; h = open(p).read()
def rep(a, b, count=1):
    global h
    n = h.count(a); assert n == count, (a[:90], n); h = h.replace(a, b)
DOT = '<span class="dot"><svg viewBox="0 0 12 12" fill="none" stroke-width="1.6"><path d="M2 10 10 2M4 2h6v6"/></svg></span>'

# Step 3: make it clear when a client should call
rep('<h2>Recognise this<span class="hl">?</span></h2>', '<h2>When to call us<span class="hl">.</span></h2>')
rep('<p>The questions we hear from infrastructure managers, architects and CISOs. If one of them is on your agenda, we should talk.</p>',
    '<p>If one of these questions is on your desk, that is the moment to call. They are the questions we hear most from infrastructure managers, architects and CISOs.</p>')

# Steps 4 + 5: a clear, named, fixed-price first engagement
offer = f'''  <section class="section gutter offer-sec" id="first-engagement">
    <div class="rail">
      <div class="offer">
        <div class="offer-main">
          <p class="label"><span class="index">[00]</span> Your first engagement</p>
          <h2>The Data Resilience Assessment<span class="hl">.</span></h2>
          <p class="offer-lede">One clear answer to the question boards and auditors now ask: <strong>can we recover, and what do we fix first?</strong></p>
          <a class="pill solid" href="#contact">Request the assessment
            {DOT}
          </a>
        </div>
        <dl class="offer-facts">
          <div><dt>Scope</dt><dd>Storage, backup and recovery of your business-critical systems, and where your sensitive data lives.</dd></div>
          <div><dt>You get</dt><dd>A recoverability verdict, a risk register and a prioritised plan, presented to your team and management.</dd></div>
          <div><dt>Success</dt><dd>Agreed with you in writing before we start.</dd></div>
          <div><dt>Price</dt><dd>Fixed scope, fixed price, agreed upfront. No hourly surprises.</dd></div>
        </dl>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <section class="section gutter" id="services">'''
rep('  <section class="section gutter" id="services">', offer)
rep('/* Challenges */', '''/* First engagement */
.offer { display: grid; grid-template-columns: 1.1fr 1fr; gap: clamp(28px, 5vw, 64px); align-items: start; padding: clamp(24px, 4vw, 48px); border: 1px solid var(--line); background: var(--panel); }
.offer > * { min-width: 0; }
.offer h2 { font-size: clamp(2rem, 4.4vw, 3.4rem); margin-top: 18px; }
.offer-lede { color: var(--muted); font-size: 1.15rem; margin: 18px 0 28px; max-width: 32rem; }
.offer-lede strong { color: var(--fg); font-weight: 500; }
.offer-facts { margin: 0; display: grid; }
.offer-facts > div { padding: 16px 0; border-top: 1px solid var(--line); }
.offer-facts > div:last-child { border-bottom: 1px solid var(--line); }
.offer-facts dt { font: 500 0.75rem var(--font-mono); letter-spacing: 0.1em; text-transform: uppercase; color: var(--signal); }
.offer-facts dd { margin: 4px 0 0; }
@media (max-width: 860px) { .offer { grid-template-columns: 1fr; } }

/* Challenges */''')

# Step 7 + expectations/handover: a named, repeatable method
rep('<span class="index">[05]</span> How we work</p>', '<span class="index">[05]</span> Our method</p>')
rep('<p>Every engagement answers three questions in order. You only commit to the next step once you have seen the result of the previous one.</p>',
    '<p>The same proven method on every engagement, so we never start from scratch. You only commit to the next step once you have seen the result of the previous one.</p>')
rep("<ul><li>Your storage, backup and virtualisation estate</li><li>Risks: recovery gaps, end-of-support, sensitive data</li><li>Capabilities you already own but don't use</li></ul>",
    "<ul><li>Success agreed upfront, in writing</li><li>The exact scope defined</li><li>Risks: recovery gaps, end-of-support, sensitive data</li><li>Capabilities you already own but don't use</li></ul>")
rep('<ul><li>Storage, backup and cyber recovery design</li><li>Virtualisation, cloud and migration</li><li>Data clean-up and classification</li></ul>',
    '<ul><li>Storage, backup, cyber recovery, virtualisation and cloud</li><li>Honest progress updates, including the difficult conversations</li><li>Decisions prepared for you, so you can choose quickly</li></ul>')
rep('<h3>Ongoing support</h3>', '<h3>Handover &amp; support</h3>')
rep('<p>We stay on as your infrastructure partner after go-live.</p>', '<p>A clear handover, and support for as long as you need it.</p>')
rep('<ul><li>Regular recovery testing</li><li>Health checks and capacity planning</li><li>Training as your platforms change</li></ul>',
    '<ul><li>Documentation (HLD/LLD) and knowledge transfer</li><li>Tested recovery, with the evidence</li><li>Optional health checks and recovery testing</li></ul>')
rep('<p class="out"><b>You get:</b> confidence that it keeps working.</p>', '<p class="out"><b>You get:</b> a team that can run it, and proof that it works.</p>')

# The goal of an elite advisor -> four client outcomes
rep('<h3 class="commit-head">What you can count on</h3>', '<h3 class="commit-head">What every client can count on</h3>')
h, n = re.subn(r'(<div class="reasons">).*?(\n      </div>\n    </div>\n  </section>)', lambda m: m.group(1) + '''
        <div><span class="index">→ Outcome</span><h3>The problem, solved well</h3><p>We fix what you hired us for, and take the time-consuming work off your team's plate.</p></div>
        <div><span class="index">→ Capability</span><h3>A stronger team</h3><p>Documentation and knowledge transfer, so your team can run what we build without us.</p></div>
        <div><span class="index">→ Clarity</span><h3>A result you can describe</h3><p>Every engagement ends with an outcome you can explain in one sentence to your board or auditor.</p></div>
        <div><span class="index">→ Evidence</span><h3>Proof of our contribution</h3><p>Tested failover and recovery, with evidence you can show.</p></div>''' + m.group(2), h, count=1, flags=re.S)
assert n == 1

# Step 8: choose the projects that build the business
rep('<p>We work where data is critical, sensitive and regulated: from central banking and national government to defence, universities and the infrastructure the Netherlands runs on.</p>',
    '<p>We work where data is critical, sensitive and regulated. Our best fit: organisations where downtime, data loss or a failed audit is not an option.</p>')

# The importance of every client: confidentiality and helpful answers
rep('<span class="index">[06]</span> Questions</p>', '<span class="index">[06]</span> Helpful answers</p>')
rep('<p>Tell us about your environment, the challenge and your timeline. We will come back with a clear first step.</p>',
    '<p>Tell us about your environment, the challenge and your timeline. We will come back with a clear first step. Every conversation is confidential, and we are happy to sign your NDA first.</p>')

# navigation
rep('<a href="#challenges">Challenges</a>', '<a href="#first-engagement">Assessment</a>', 2)
rep('<a href="#how-we-work">How we work</a>', '<a href="#how-we-work">Method</a>', 2)

c = iter(range(100))
h = re.sub(r'(<p class="label"[^>]*><span class="index">)\[\d\d\](</span>)', lambda m: '%s[%02d]%s' % (m.group(1), next(c), m.group(2)), h)
open(p, 'w').write(h); print('guidelines applied')
