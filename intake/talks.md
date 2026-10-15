# Talks

Every talk, interview and episode on coffeewithayman.com/talks.

**What goes in (guidelines):**
- **Videos only.** Talks, panels, interviews, webinars, podcast appearances that
  were filmed, and Ayman's own channel. Audio-only podcasts are left out
  (links are skipped automatically, audio files dropped in `media/inbox/` are
  moved to `_failed/`).
- **Not included:** Getting Into Infosec (Ayman's own podcast).
- Recordings where Ayman doesn't actually speak are skipped automatically by
  the voiceprint check.

Three ways in:

1. **Paste a link** into the Inbox below and save; the watcher turns it into an entry.
2. **Drop a video** into `media/inbox/` (`.mp4 .mov .mkv .webm .m4v .avi`, optionally with a same-named `.md` holding its details).
3. **Edit an entry** — change `format`, `clip`, `category` or `topics` and only the affected steps re-run.

Fields: `format` is one of talk · webinar · interview · podcast-guest · panel · cohost.
It decides what gets indexed: talks/webinars and one-on-one interviews keep the whole
conversation; panels and co-hosted shows keep only Ayman's parts. `clip: 39:00–1:02:00`
limits processing to part of a long episode. `status` lines are written by the pipeline.

Notes: add bullets under any entry's `### Notes`. Open notes get handled with
`/process-notes` in Claude Code and are struck through when done.

## Inbox
<!-- Paste URLs here, one per line. -->


## Can employees safely use AI agents? AI pentesting agent liabilities, and the news - ESW #473
- id: can-employees-safely-use-ai-agents-ai-pentesting-agent <!-- managed -->
- url: https://youtu.be/o-Edp9puMEo?si=71SjUt1akYGDx4vH
- format: panel <!-- guessed from 5 voice(s); fix if wrong -->
- date: 2026-08-24
- event: Security Weekly - A CRA Resource
- category:
- topics:
- summary: Ayman discusses the use of AI in pentesting, emphasizing the importance of human oversight and the value of custom harnesses to ensure accurate and novel testing. He also highlights the potential of AI in both offensive and defensive security operations, while noting the challenges of keeping up with the volume of threats and the need for open-source models and tools.
- status: ✅ ingested 2026-10-15 · 199 lines · speaker auto (voiceprint 0.85 + name mentioned) · 174 flagged <!-- managed -->

### Notes

## Ayman Elsawah - Why We Break Things... The Neuroscience of Hackers!
- id: ayman-elsawah-why-we-break-things-the-neuroscience-of <!-- managed -->
- url: https://www.youtube.com/watch?v=cTKkAfVoCSQ
- format: talk
- date: 2020-05-02
- event: BSides Knoxville
- category:
- topics:
- summary: Ayman explains that hackers often possess three key traits: entrepreneurship, grit, and creativity, and explores the neuroscience behind these qualities. He discusses how the brain's angular cingulate cortex helps regulate emotions during failure, enabling perseverance, and how divergent thinking and latent inhibition contribute to creative problem-solving. Ayman also highlights the importance of fostering creativity through learning new subjects, observing others, and embracing unconventional thinking.
- status: ✅ ingested 2026-10-15 · 492 lines · speaker auto (voiceprint 0.78 + name mentioned) · 78 flagged <!-- managed -->

### Notes

## Ayman Elsawah - Using Paretos Principle for Securing AWS with SCPs - DEF CON 27 Cloud Village
- id: ayman-elsawah-using-paretos-principle-for-securing-aws-with <!-- managed -->
- url: https://www.youtube.com/watch?v=RiZxb98sGTk
- format: talk
- date: 2019-12-20
- event: DEFCONConference
- category:
- topics:
- summary: Ayman explains how to use Pareto's Principle to secure AWS environments by focusing on a few key service control policies (SCPs) that provide the most security benefit. He recommends implementing SCPs to limit instance types, restrict region usage, prevent deletion of critical resources like CloudTrail logs and VPC flow logs, and restrict root account actions. He also emphasizes the importance of a multi-account strategy, creating a dedicated master account, and using SCPs to enforce security policies across all accounts.
- status: ✅ ingested 2026-10-15 · 458 lines · speaker auto (voiceprint 0.84 + name mentioned) · 117 flagged <!-- managed -->

### Notes

## Day 1 - 03 - Applying Pareto’s Principle to Securing AWS with SCPS - Ayman Elsawah
- id: day-1-03-applying-pareto-s-principle-to-securing-aws-with <!-- managed -->
- url: https://www.youtube.com/watch?v=_Nxjfr2OqxQ
- format: talk
- date: 2019-12-14
- event: Pacific Hackers Association
- category:
- topics:
- summary: Ayman explains how to use Pareto’s Principle to secure AWS accounts by focusing on the most impactful security measures, such as implementing Service Control Policies (SCPs) at the organization level to enforce guardrails across multiple accounts. He highlights specific examples, including blocking the deletion of CloudTrail logs, restricting instance types, limiting regions, and preventing S3 public access, to reduce risk with minimal effort. He also emphasizes organizing AWS accounts into logical groups and using SCPs to control permissions and prevent misconfigurations.
- status: ✅ ingested 2026-10-15 · 281 lines · speaker auto (voiceprint 0.65 + name mentioned) · 113 flagged <!-- managed -->

### Notes

## BSidesSF 2026 - Google Drive Hunter: Building the Tool Google Should’ve Built (Ayman Elsawah)
- id: bsidessf-2026-google-drive-hunter-building-the-tool-google <!-- managed -->
- url: https://www.youtube.com/watch?v=sOv8R4TTOPg
- format: talk <!-- guessed from 2 voice(s); fix if wrong -->
- date: 2026-05-12
- event: Security BSides San Francisco
- category:
- topics:
- summary: Ayman explains the problem of publicly shared Google Drive files and how they can expose sensitive information. He discusses technical controls like restricting sharing via Google Groups and OU settings in Google Workspace, and introduces Sleuther, a tool he developed to audit and identify publicly shared files. He also shares a real-world example of discovering an unintended publicly shared file and the process of responsibly disclosing it to the owner.
- status: ✅ ingested 2026-10-15 · 331 lines · speaker auto (voiceprint 0.77 + name mentioned) · 25 flagged <!-- managed -->

### Notes

## BSidesSF 2015 - Federating AWS CLI (Ayman Elsawah, Paul Moreno)
- id: bsidessf-2015-federating-aws-cli-ayman-elsawah-paul-moreno <!-- managed -->
- url: https://www.youtube.com/watch?v=iQ3ALCjxv4g
- format: interview <!-- guessed from 2 voice(s); fix if wrong -->
- date: 2023-12-02
- event: Security BSides San Francisco
- category:
- topics:
- summary: Ayman explains the risks of storing AWS credentials in plain text and how federating AWS CLI through Shibboleth and STS can mitigate these risks by eliminating the need for developers to handle long-term keys. He details the implementation of Eris, a tool that automates the process of obtaining temporary credentials and reauthorizing them every hour, reducing the chance of credential exposure. Ayman also highlights challenges encountered with AWS STS, including poor documentation and unexpected behavior with session tokens and anonymous connections.
- status: ✅ ingested 2026-10-15 · 307 lines · speaker auto (voiceprint 0.78 + name mentioned) · 47 flagged <!-- managed -->

### Notes

## Ayman Elsawah on Cloud Security and Infosec Careers
- id: ayman-elsawah-on-cloud-security-and-infosec-careers <!-- managed -->
- url: https://www.youtube.com/watch?v=KJvPHZGtGdM
- format: interview
- date: 2019-05-02
- event: Sam Bowne
- category:
- topics:
- summary: Ayman discusses cloud security challenges, emphasizing the importance of least privilege access and proper configuration management to prevent data leaks and unauthorized access. He highlights the risks of misconfigured S3 buckets and insecure IAM credentials, using real-world examples like the Code Spaces breach. Ayman also talks about diversity in infosec, advocating for more inclusive programs and awareness of ongoing challenges faced by underrepresented groups. For aspiring infosec professionals, he encourages creativity, persistence, and hands-on learning, suggesting practical steps like using open-source tools and contributing to GitHub projects.
- status: ✅ ingested 2026-10-15 · 643 lines · speaker auto (voiceprint 0.68 + name mentioned) · 199 flagged <!-- managed -->

### Notes

## Fractional CISO - When, Why, & How to Become One w/ Ayman Elsawah  - Hyperdrive Minds Podcast 10
- id: fractional-ciso-when-why-how-to-become-one-w-ayman-elsawah <!-- managed -->
- url: https://www.youtube.com/watch?v=4r964FmeJ-4
- format: podcast-guest
- date: 2024-07-05
- event: BlakeWilliamsHQ
- category:
- topics:
- summary: Ayman explains the benefits and challenges of becoming a fractional CISO, emphasizing the importance of having experience managing a security program, understanding the mindset of a security professional, and identifying whether fractional work is a temporary or long-term career path. He also discusses the value of being present and approachable in security roles, the importance of building strong relationships for business development, and the need for security professionals to focus on creating a positive security culture within organizations.
- status: ✅ ingested 2026-10-15 · 828 lines · speaker auto (voiceprint 0.84 + name mentioned) · 94 flagged <!-- managed -->

### Notes

## How to Hack your Career  Building a vCISO Business with Ayman Elsawah
- id: how-to-hack-your-career-building-a-vciso-business-with-ayman <!-- managed -->
- url: https://www.youtube.com/watch?v=JKTdDMTtvqs
- format: podcast-guest
- date: 2024-04-23
- event: Hacker Valley Media
- category:
- topics:
- summary: Ayman explains how to build a vCISO business by emphasizing the importance of niche specialization, personal branding, and consistent marketing efforts on platforms like LinkedIn. He advises aspiring vCISOs to assess their motivation, build expertise in specific areas such as SOC 2 or incident response, and structure their services to align with their lifestyle and long-term goals. He also highlights the need to balance client work with ongoing sales and marketing to ensure business sustainability.
- status: ✅ ingested 2026-10-15 · 369 lines · speaker auto (voiceprint 0.87 + name mentioned) · 41 flagged <!-- managed -->

### Notes

## Let’s Simplify Cybersecurity Language with Ayman Elsawah, Founder at Cloud Security Labs
- id: let-s-simplify-cybersecurity-language-with-ayman-elsawah <!-- managed -->
- url: https://www.youtube.com/watch?v=K8tMGW4dH68
- format: podcast-guest
- date: 2023-11-28
- event: Cyft
- category:
- topics:
- status: 🎧 transcribing on GPU <!-- managed -->

### Notes

## Ayman Elsawah - Using Quora to Connect With Your Audience
- id: ayman-elsawah-using-quora-to-connect-with-your-audience <!-- managed -->
- url: https://www.youtube.com/watch?v=YMc5nidZpnY
- format: podcast-guest
- date: 2019-06-11
- event: Paul Brodie
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Episode 41 Ayman Elsawah from Cloud Security Labs
- id: episode-41-ayman-elsawah-from-cloud-security-labs <!-- managed -->
- url: https://podcasts.apple.com/us/podcast/episode-41-ayman-elsawah-from-cloud-security-labs/id1676823766?i=1000638123708
- format: podcast-guest
- date: 2023-12-11
- event:
- category:
- topics:
- status: ⏭ skipped: audio only — the archive is videos only <!-- managed -->

### Notes

## How Internet Safety Experts Protect Their Kids Online | Ep2
- id: how-internet-safety-experts-protect-their-kids-online-ep2 <!-- managed -->
- url: https://www.youtube.com/watch?v=QLAE3mUEnmY
- format:
- date: 2023-08-23
- event: CyberFareedah
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## What is Phishing Simulation and should you phish your own employees?
- id: what-is-phishing-simulation-and-should-you-phish-your-own <!-- managed -->
- url: https://www.youtube.com/watch?v=5NHwEtJlsmo
- format:
- date: 2021-01-14
- event: Wizer - Security Awareness Training
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## What You Need To Know About Restoring From A Backup
- id: what-you-need-to-know-about-restoring-from-a-backup <!-- managed -->
- url: https://www.youtube.com/watch?v=ZK7PLiqXjdg
- format:
- date: 2022-02-11
- event: Wizer - Security Awareness Training
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## How to Ace SOC2 in SaaS Scale Ups
- id: how-to-ace-soc2-in-saas-scale-ups <!-- managed -->
- url: https://www.youtube.com/watch?v=HieEWiTy2zQ
- format:
- date: 2023-11-06
- event: Sprinto
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Crowdstrike Global IT Outage Explained! (Hint: Not a Cyber Incident!)
- id: crowdstrike-global-it-outage-explained-hint-not-a-cyber <!-- managed -->
- url: https://www.youtube.com/watch?v=W0jmdDJ7jZQ
- format: talk
- date: 2024-07-21
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Protecting Your Data: Disabling Google Takeout in Google Workspace
- id: protecting-your-data-disabling-google-takeout-in-google <!-- managed -->
- url: https://www.youtube.com/watch?v=k42FP6Jz0Ao
- format: talk
- date: 2024-07-07
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Security Expert Just Wants To Share Everything He Knows
- id: security-expert-just-wants-to-share-everything-he-knows <!-- managed -->
- url: https://www.youtube.com/watch?v=ghYwm8aRMAg
- format: talk
- date: 2024-07-04
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Important Consideration When Trying To Be a vCISO
- id: important-consideration-when-trying-to-be-a-vciso <!-- managed -->
- url: https://www.youtube.com/watch?v=v46vosJdxfk
- format: talk
- date: 2024-03-17
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Uncover Security Risks With A Technical Risk Assessment
- id: uncover-security-risks-with-a-technical-risk-assessment <!-- managed -->
- url: https://www.youtube.com/watch?v=Swqww9iXcjo
- format: talk
- date: 2025-07-17
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## DEFCON Trailer
- id: defcon-trailer <!-- managed -->
- url: https://www.youtube.com/watch?v=8wQ03qZpqjY
- format: talk
- date: 2025-08-03
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## The problem with being THAT security person...
- id: the-problem-with-being-that-security-person <!-- managed -->
- url: https://www.youtube.com/shorts/wPwsehUhFa8
- format: talk
- date: 2024-01-24
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Startup Security Simplified: Prioritize What Matters for Growth
- id: startup-security-simplified-prioritize-what-matters-for <!-- managed -->
- url: https://www.youtube.com/shorts/1iZPeYAo_Nw
- format: talk
- date: 2023-11-27
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## SOC2 vs. ISO for Startups: Key Differences Explained | Cybersecurity Essentials
- id: soc2-vs-iso-for-startups-key-differences-explained <!-- managed -->
- url: https://www.youtube.com/shorts/npfKNYz-9Ks
- format: talk
- date: 2023-11-23
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Mastering Security Logging: Essential Tips for SaaS & B2B Companies
- id: mastering-security-logging-essential-tips-for-saas-b2b <!-- managed -->
- url: https://www.youtube.com/shorts/zQiu947XEWI
- format: talk
- date: 2023-11-22
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Ban Shared Credentials: Elevate Your Company's Security | Cybersecurity Tips
- id: ban-shared-credentials-elevate-your-company-s-security <!-- managed -->
- url: https://www.youtube.com/shorts/4GVhdBbxc2E
- format: talk
- date: 2023-11-18
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Is Your Startup Safe? Quick SSO & Authentication Tips for SaaS Security
- id: is-your-startup-safe-quick-sso-authentication-tips-for-saas <!-- managed -->
- url: https://www.youtube.com/shorts/1094CjmaER0
- format: talk
- date: 2023-11-16
- event: Coffee With Ayman - Security Cafe
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## BSides SF 2025 Vlog - Interview with Ayman ElSawah + Meeting Jason Haddix & Tanya Janca!
- id: bsides-sf-2025-vlog-interview-with-ayman-elsawah-meeting <!-- managed -->
- url: https://www.youtube.com/watch?v=7x_VJLEIuQA
- format:
- date: 2025-05-07
- event: Three Headed Beast Security
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Balancing Life and the Addiction to Productivity w/ Ayman Elsawah
- id: balancing-life-and-the-addiction-to-productivity-w-ayman <!-- managed -->
- url: https://www.youtube.com/watch?v=uQOCK0y_PD4
- format:
- date: 2024-07-12
- event: BlakeWilliamsHQ
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## How to become a Cybersecurity professional  | Ayman Elsawah
- id: how-to-become-a-cybersecurity-professional-ayman-elsawah <!-- managed -->
- url: https://www.youtube.com/watch?v=iDv0-AY7J84
- format:
- date: 2021-12-06
- event: Haythem Hammour
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## How Do You Protect Data on Endpoints | Cybersecurity on the Street | Interviews
- id: how-do-you-protect-data-on-endpoints-cybersecurity-on-the <!-- managed -->
- url: https://www.youtube.com/watch?v=q4syDUQxLJg
- format:
- date: 2020-04-29
- event: Absolute Security
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## How do you protect your remote employees? | Cybersecurity on the Street | Interviews
- id: how-do-you-protect-your-remote-employees-cybersecurity-on <!-- managed -->
- url: https://www.youtube.com/watch?v=zocUc7bzQAc
- format:
- date: 2020-03-27
- event: Absolute Security
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Cyber Resilience with Cohesity, When to use AI for Writing, and the News - Rob Sadowski - ESW #477
- id: cyber-resilience-with-cohesity-when-to-use-ai-for-writing <!-- managed -->
- url: https://www.youtube.com/watch?v=6sZm4oA-iaU
- format: cohost
- date: 2026-09-21
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## The State of Cybersecurity Hiring, 2026 content plans, and the weekly news - ESW #441
- id: the-state-of-cybersecurity-hiring-2026-content-plans-and-the <!-- managed -->
- url: https://www.youtube.com/watch?v=cTkQz2DGJRg
- format: cohost
- date: 2026-01-12
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## ESW at BlackHat and the weekly enterprise security news - ESW #419
- id: esw-at-blackhat-and-the-weekly-enterprise-security-news-esw <!-- managed -->
- url: https://www.youtube.com/watch?v=Dq8_NlDm-A0
- format: cohost
- date: 2025-08-11
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## The Cyber Canon, ditching the SOC 2, and the weekly enterprise news - Helen Patton - ESW #416
- id: the-cyber-canon-ditching-the-soc-2-and-the-weekly-enterprise <!-- managed -->
- url: https://www.youtube.com/watch?v=ddA0I3fGRHA
- format: cohost
- date: 2025-07-21
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Data Security in the AI Era, Don't Let AI Ruin your Presentation, and the Weekly News - ESW #480
- id: data-security-in-the-ai-era-don-t-let-ai-ruin-your <!-- managed -->
- url: https://www.youtube.com/watch?v=6a2-W3WDGhg
- format: cohost
- date: 2026-10-12
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Shadow AI Epidemic: Uncovering Agents on the Endpoint, British Library Breach, & News ... - ESW #475
- id: shadow-ai-epidemic-uncovering-agents-on-the-endpoint-british <!-- managed -->
- url: https://www.youtube.com/watch?v=FnO0T_1Fj-M
- format: cohost
- date: 2026-09-07
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Exploring AI Network Protocols; Vulnerability Truths and Guarantees; and the News - ESW #469
- id: exploring-ai-network-protocols-vulnerability-truths-and <!-- managed -->
- url: https://www.youtube.com/watch?v=Em3FoAU4AE8
- format: cohost
- date: 2026-07-27
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## AI Security at Scale, CMMC phase II paused, and the Weekly Enterprise News - ESW #468
- id: ai-security-at-scale-cmmc-phase-ii-paused-and-the-weekly <!-- managed -->
- url: https://www.youtube.com/watch?v=b4jFqynkXgo
- format: cohost
- date: 2026-07-28
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Fixing pentesting, Meta is destroying its engineering org, the weekly news  - ESW #465
- id: fixing-pentesting-meta-is-destroying-its-engineering-org-the <!-- managed -->
- url: https://www.youtube.com/watch?v=DRg-qoTIvJE
- format: cohost
- date: 2026-06-29
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Safe AI at scale, what happens after initial access, and the weekly enterprise news  - ESW #463
- id: safe-ai-at-scale-what-happens-after-initial-access-and-the <!-- managed -->
- url: https://www.youtube.com/watch?v=FDWowt7UOhU
- format: cohost
- date: 2026-06-15
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Helping defense's use of AI catch up with offense, cost of the vulnpocalypse, news - ESW #461
- id: helping-defense-s-use-of-ai-catch-up-with-offense-cost-of <!-- managed -->
- url: https://www.youtube.com/watch?v=pUEYXOX8hOY
- format: cohost
- date: 2026-06-01
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## We catch up on the news, including AI vuln hunting; also more RSAC interviews! - ESW #454
- id: we-catch-up-on-the-news-including-ai-vuln-hunting-also-more <!-- managed -->
- url: https://www.youtube.com/watch?v=ul7Cj6BuA48
- format: cohost
- date: 2026-04-13
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Can AI help critical infrastructure, the state of the cyber market, and weekly news - ESW #451
- id: can-ai-help-critical-infrastructure-the-state-of-the-cyber <!-- managed -->
- url: https://www.youtube.com/watch?v=S74rml3jr2A
- format: cohost
- date: 2026-03-23
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## AI Governance, new book (Code War) from Allie Mellen, and the weekly news! - ESW #450
- id: ai-governance-new-book-code-war-from-allie-mellen-and-the <!-- managed -->
- url: https://www.youtube.com/watch?v=J8_MeasiN0Q
- format: cohost
- date: 2026-03-16
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Bringing intelligence to assets, new White House cybersecurity strategy, and the news - ESW #447
- id: bringing-intelligence-to-assets-new-white-house <!-- managed -->
- url: https://www.youtube.com/watch?v=xKjbiRY7RSw
- format: cohost
- date: 2026-02-23
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Hardware-level zero trust, don't trust AI with your employees, and the news - ESW #446
- id: hardware-level-zero-trust-don-t-trust-ai-with-your-employees <!-- managed -->
- url: https://www.youtube.com/watch?v=tKa7EsJA8Xg
- format: cohost
- date: 2026-02-16
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Making vulnerability management and incident response actually work. Also, the News! - ESW #442
- id: making-vulnerability-management-and-incident-response <!-- managed -->
- url: https://www.youtube.com/watch?v=nsfAZtwp1Yc
- format: cohost
- date: 2026-01-19
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Illuminating Data Blind Spots, Topic, Enterprise News - Tony Kelly - ESW #437
- id: illuminating-data-blind-spots-topic-enterprise-news-tony <!-- managed -->
- url: https://www.youtube.com/watch?v=UxOnCMw_yPc
- format: cohost
- date: 2025-12-15
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Internal threats are the hole in Cybersecurity’s donut - Frank Vukovits - ESW #438
- id: internal-threats-are-the-hole-in-cybersecurity-s-donut-frank <!-- managed -->
- url: https://www.youtube.com/watch?v=CJbqpcN_lz0
- format: cohost
- date: 2025-12-22
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Transforming Frontline Workflows with Passwordless Access, AI costs, and the News - ESW #431
- id: transforming-frontline-workflows-with-passwordless-access-ai <!-- managed -->
- url: https://www.youtube.com/watch?v=KkM82krp3UU
- format: cohost
- date: 2025-11-03
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Mitigating attacks against AI-enabled Apps, Replacing the CIA triad, Enterprise News - ESW #429
- id: mitigating-attacks-against-ai-enabled-apps-replacing-the-cia <!-- managed -->
- url: https://www.youtube.com/watch?v=Q0FJzZPgwwU
- format: cohost
- date: 2025-10-20
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Disruption is Coming for the Vulnerability Management Market - Tod Beardsley - ESW #425
- id: disruption-is-coming-for-the-vulnerability-management-market <!-- managed -->
- url: https://www.youtube.com/watch?v=CBoEIl2CcY0
- format: cohost
- date: 2025-09-22
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Dave Lewis talks M&A due diligence, TBD topic, the weekly news - Dave Lewis - ESW #422
- id: dave-lewis-talks-m-a-due-diligence-tbd-topic-the-weekly-news <!-- managed -->
- url: https://www.youtube.com/watch?v=SsDGk99LT9c
- format: cohost
- date: 2025-09-01
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Oktane Preview with Harish Peri, Invisible Prompt Attacks, and the weekly news! - Hari... - ESW #421
- id: oktane-preview-with-harish-peri-invisible-prompt-attacks-and <!-- managed -->
- url: https://www.youtube.com/watch?v=WHSw4wn3iIo
- format: cohost
- date: 2025-08-25
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Rethinking risk based vulnerability management, Black Hat expo insights, and the news  - ESW #420
- id: rethinking-risk-based-vulnerability-management-black-hat <!-- managed -->
- url: https://www.youtube.com/watch?v=GILIKiSsIGo
- format: cohost
- date: 2025-08-18
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Weekly Enterprise Security News and Tips on Building Security From Day 1 - Guillaume Ross - ESW #418
- id: weekly-enterprise-security-news-and-tips-on-building <!-- managed -->
- url: https://www.youtube.com/watch?v=JKmz11ew9-s
- format: cohost
- date: 2025-08-04
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## The enterprise security news, more secure by removing credentials, & RSAC interviews -... - ESW #410
- id: the-enterprise-security-news-more-secure-by-removing <!-- managed -->
- url: https://www.youtube.com/watch?v=Xg6ylqF0-qc
- format: cohost
- date: 2025-06-09
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Tailscale rakes it in, CVE dead to us, cool Chrome extensions, dog saves toddler - ESW #403
- id: tailscale-rakes-it-in-cve-dead-to-us-cool-chrome-extensions <!-- managed -->
- url: https://www.youtube.com/watch?v=-egy0Z62VOA
- format: cohost
- date: 2025-04-21
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Best of Cyber April Fools, Tons of Free Tools, runZero positioned to disrupt? - ESW #401
- id: best-of-cyber-april-fools-tons-of-free-tools-runzero <!-- managed -->
- url: https://www.youtube.com/watch?v=-JJw212ph8Q
- format: cohost
- date: 2025-04-07
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## The toughest decisions CISOs have to make, MCP servers, Napster's comeback - ESW #400
- id: the-toughest-decisions-cisos-have-to-make-mcp-servers <!-- managed -->
- url: https://www.youtube.com/watch?v=3LRiRy-6-cU
- format: cohost
- date: 2025-03-31
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Security doesn't trust AI, but startups are using it to write 95% of their code - ESW #398
- id: security-doesn-t-trust-ai-but-startups-are-using-it-to-write <!-- managed -->
- url: https://www.youtube.com/watch?v=dkKqBjMRgIA
- format: cohost
- date: 2025-03-17
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Ransomware is down, Mac malware is up, AI disappoints - ESW #396
- id: ransomware-is-down-mac-malware-is-up-ai-disappoints-esw-396 <!-- managed -->
- url: https://www.youtube.com/watch?v=wmlCgBpNCNo
- format: cohost
- date: 2025-03-03
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## The dark side of security leadership, will agentic be a thing, OWASP AI resources - ESW #394
- id: the-dark-side-of-security-leadership-will-agentic-be-a-thing <!-- managed -->
- url: https://www.youtube.com/watch?v=iezO2Muq7VU
- format: cohost
- date: 2025-02-17
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Semgrep non-drama, Facebook hates Linux - Vulns in Cars, Cell Towers, M365, and more - ESW #392
- id: semgrep-non-drama-facebook-hates-linux-vulns-in-cars-cell <!-- managed -->
- url: https://www.youtube.com/watch?v=YS7CpWENEiA
- format: cohost
- date: 2025-02-03
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Celebrity investors, creator metrics, and Chrome extension compromise - ESW #389
- id: celebrity-investors-creator-metrics-and-chrome-extension <!-- managed -->
- url: https://www.youtube.com/watch?v=WynViAuMtFQ
- format: cohost
- date: 2025-01-13
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## AI messes with scammers, autonomous endpoint security, malware targets Excel - ESW #385
- id: ai-messes-with-scammers-autonomous-endpoint-security-malware <!-- managed -->
- url: https://www.youtube.com/watch?v=EMnkgH2re-Y
- format: cohost
- date: 2024-11-22
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes

## Funding, AI controls your PC, Cyberstarts stops Sunrise, public cyber goes private - ESW #382
- id: funding-ai-controls-your-pc-cyberstarts-stops-sunrise-public <!-- managed -->
- url: https://www.youtube.com/watch?v=hmrrhMrJPYM
- format: cohost
- date: 2024-11-04
- event: Security Weekly - A CRA Resource
- category:
- topics:
- status: ⏳ queued <!-- managed -->

### Notes
