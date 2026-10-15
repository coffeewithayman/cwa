# Talks

Every talk, interview and episode on coffeewithayman.com/talks.

**What goes in (guidelines):**
- **Videos only.** Talks, panels, interviews, webinars, podcast appearances that
  were filmed, and Ayman's own channel. Audio-only podcasts are left out
  (links are skipped automatically, audio files dropped in `media/inbox/` are
  moved to `_failed/`).
- **Not included:** Getting Into Infosec (Ayman's own podcast).
- **Don't add new Enterprise Security Weekly episodes here** — list them in
  [`esw.md`](esw.md); they'll get a separate workflow that links to Ayman's
  segment. The 7 episodes already processed stay here.
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


## Ayman Elsawah - Why We Break Things... The Neuroscience of Hackers!
- id: ayman-elsawah-why-we-break-things-the-neuroscience-of <!-- managed -->
- url: https://www.youtube.com/watch?v=cTKkAfVoCSQ
- format: talk
- date: 2020-05-01 <!-- from the video description -->
- event: BSides Knoxville
- category:
- topics: Careers
- summary: Ayman explains that hackers often possess three key traits: entrepreneurship, grit, and creativity, and explores the neuroscience behind these qualities. He discusses how the brain's angular cingulate cortex helps regulate emotions during failure, enabling perseverance, and how divergent thinking and latent inhibition contribute to creative problem-solving. Ayman also highlights the importance of fostering creativity through learning new subjects, observing others, and embracing unconventional thinking.
- status: ✅ ingested 2026-10-15 · 492 lines · speaker auto (voiceprint 0.78 + name mentioned) · 78 flagged <!-- managed -->

### Notes

## Ayman Elsawah - Using Paretos Principle for Securing AWS with SCPs - DEF CON 27 Cloud Village
- id: ayman-elsawah-using-paretos-principle-for-securing-aws-with <!-- managed -->
- url: https://www.youtube.com/watch?v=RiZxb98sGTk
- format: talk
- date: 2019-08-09 <!-- DEF CON 27 Cloud Village ran Aug 9-11, 2019; exact day unknown -->
- event: DEFCONConference
- category:
- topics: Cloud Security
- summary: Ayman explains how to use Pareto's Principle to secure AWS environments by focusing on a few key service control policies (SCPs) that provide the most security benefit. He recommends implementing SCPs to limit instance types, restrict region usage, prevent deletion of critical resources like CloudTrail logs and VPC flow logs, and restrict root account actions. He also emphasizes the importance of a multi-account strategy, creating a dedicated master account, and using SCPs to enforce security policies across all accounts.
- status: ✅ ingested 2026-10-15 · 458 lines · speaker auto (voiceprint 0.84 + name mentioned) · 117 flagged <!-- managed -->

### Notes

## Day 1 - 03 - Applying Pareto’s Principle to Securing AWS with SCPS - Ayman Elsawah
- id: day-1-03-applying-pareto-s-principle-to-securing-aws-with <!-- managed -->
- url: https://www.youtube.com/watch?v=_Nxjfr2OqxQ
- format: talk
- date: 2019-11-08 <!-- Day 1 of Pacific Hackers Conference, Nov 8-10, 2019 -->
- event: Pacific Hackers Association
- category:
- topics: Cloud Security
- summary: Ayman explains how to use Pareto’s Principle to secure AWS accounts by focusing on the most impactful security measures, such as implementing Service Control Policies (SCPs) at the organization level to enforce guardrails across multiple accounts. He highlights specific examples, including blocking the deletion of CloudTrail logs, restricting instance types, limiting regions, and preventing S3 public access, to reduce risk with minimal effort. He also emphasizes organizing AWS accounts into logical groups and using SCPs to control permissions and prevent misconfigurations.
- status: ✅ ingested 2026-10-15 · 281 lines · speaker auto (voiceprint 0.65 + name mentioned) · 113 flagged <!-- managed -->

### Notes

## BSidesSF 2026 - Google Drive Hunter: Building the Tool Google Should’ve Built (Ayman Elsawah)
- id: bsidessf-2026-google-drive-hunter-building-the-tool-google <!-- managed -->
- url: https://www.youtube.com/watch?v=sOv8R4TTOPg
- format: talk <!-- guessed from 2 voice(s); fix if wrong -->
- date: 2026-03-22 <!-- session date from the sched.com link -->
- event: Security BSides San Francisco
- category:
- topics: Identity & Data Protection
- summary: Ayman explains the problem of publicly shared Google Drive files and how they can expose sensitive information. He discusses technical controls like restricting sharing via Google Groups and OU settings in Google Workspace, and introduces Sleuther, a tool he developed to audit and identify publicly shared files. He also shares a real-world example of discovering an unintended publicly shared file and the process of responsibly disclosing it to the owner.
- status: ✅ ingested 2026-10-15 · 331 lines · speaker auto (voiceprint 0.77 + name mentioned) · 25 flagged <!-- managed -->

### Notes

## BSidesSF 2015 - Federating AWS CLI (Ayman Elsawah, Paul Moreno)
- id: bsidessf-2015-federating-aws-cli-ayman-elsawah-paul-moreno <!-- managed -->
- url: https://www.youtube.com/watch?v=iQ3ALCjxv4g
- format: interview <!-- guessed from 2 voice(s); fix if wrong -->
- date: 2015-04-20 <!-- session date from the sched.com link -->
- event: Security BSides San Francisco
- category:
- topics: Cloud Security, Identity & Data Protection
- summary: Ayman explains the risks of storing AWS credentials in plain text and how federating AWS CLI through Shibboleth and STS can mitigate these risks by eliminating the need for developers to handle long-term keys. He details the implementation of Eris, a tool that automates the process of obtaining temporary credentials and reauthorizing them every hour, reducing the chance of credential exposure. Ayman also highlights challenges encountered with AWS STS, including poor documentation and unexpected behavior with session tokens and anonymous connections.
- status: ✅ ingested 2026-10-15 · 307 lines · speaker auto (voiceprint 0.78 + name mentioned) · 47 flagged <!-- managed -->

### Notes

## Ayman Elsawah on Cloud Security and Infosec Careers
- id: ayman-elsawah-on-cloud-security-and-infosec-careers <!-- managed -->
- url: https://www.youtube.com/watch?v=KJvPHZGtGdM
- format: interview
- date: 2019-05-01 <!-- from the video description -->
- event: Sam Bowne
- category:
- topics: Cloud Security, Careers
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
- topics: vCISO & Leadership, Careers
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
- topics: vCISO & Leadership, Careers
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
- topics: Startup Security, Identity & Data Protection
- summary: Ayman explains that cybersecurity can be simplified by focusing on practical steps like enabling device encryption, implementing strong access controls, and prioritizing security culture. He emphasizes that for startups, security should be tailored to their specific needs and stage of growth, with a focus on foundational measures such as proper onboarding and offboarding processes, and using built-in security features rather than overcomplicating with expensive tools. He also highlights the importance of distinguishing between compliance and true security, noting that compliance alone does not ensure protection against real-world threats.
- status: ✅ ingested 2026-10-15 · 582 lines · speaker auto (voiceprint 0.81 + name mentioned) · 100 flagged <!-- managed -->

### Notes

## Ayman Elsawah - Using Quora to Connect With Your Audience
- id: ayman-elsawah-using-quora-to-connect-with-your-audience <!-- managed -->
- url: https://www.youtube.com/watch?v=YMc5nidZpnY
- format: podcast-guest
- date: 2019-06-11
- event: Paul Brodie
- category:
- topics: Careers
- summary: Ayman explains that using Quora to answer questions in his field helps build connections with an audience, and he recommends writing detailed, helpful answers that reflect his expertise. He also mentions using targeted ad campaigns, participating in online forums, and giving informative answers without being overly salesy.
- status: ✅ ingested 2026-10-15 · 202 lines · speaker auto (voiceprint 0.84 + name mentioned) · 35 flagged <!-- managed -->

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
- format: interview <!-- guessed from 2 voice(s); fix if wrong -->
- date: 2023-08-23
- event: CyberFareedah
- category:
- topics: Identity & Data Protection
- summary: Ayman explains the importance of using device-level parental controls, such as Google Family Link or Microsoft Family, rather than relying solely on router-based filters, which can be bypassed. He also discusses the risks of Internet-connected devices, such as smart toys and cameras, and advises parents to avoid sharing photos of their children online. Additionally, he recommends delaying smartphone use until children are mature enough and suggests engaging with kids through shared activities like gaming or watching shows to build trust and understanding.
- status: ✅ ingested 2026-10-15 · 555 lines · speaker auto (voiceprint 0.88 + name mentioned) · 124 flagged <!-- managed -->

### Notes

## What is Phishing Simulation and should you phish your own employees?
- id: what-is-phishing-simulation-and-should-you-phish-your-own <!-- managed -->
- url: https://www.youtube.com/watch?v=5NHwEtJlsmo
- format: panel <!-- guessed from 6 voice(s); fix if wrong -->
- date: 2021-01-14
- event: Wizer - Security Awareness Training
- category:
- topics: vCISO & Leadership
- summary: Ayman explains that phishing simulations should focus on education and preparedness rather than tricking employees, emphasizing the importance of empathy and emotional intelligence in designing these campaigns. He advises avoiding topics that could hurt employees' feelings, such as fake bonus emails, and recommends ensuring employees know how to report phishing attempts properly. Ayman also highlights the need to understand an organization's culture before implementing any security program and suggests using phishing campaigns sparingly, only after sufficient education has been provided.
- status: ✅ ingested 2026-10-15 · 151 lines · speaker auto (voiceprint 0.80 + name mentioned) · 108 flagged <!-- managed -->

### Notes

## What You Need To Know About Restoring From A Backup
- id: what-you-need-to-know-about-restoring-from-a-backup <!-- managed -->
- url: https://www.youtube.com/watch?v=ZK7PLiqXjdg
- format: panel <!-- guessed from 3 voice(s); fix if wrong -->
- date: 2022-02-11
- event: Wizer - Security Awareness Training
- category:
- topics: Identity & Data Protection, Cloud Security
- summary: Ayman explains that businesses should identify critical data by considering what would cause the most disruption if lost, and emphasizes backing up system configurations using infrastructure as code and cloud services. He recommends storing backups in multiple locations at least 50 miles apart, encrypting sensitive data, and testing backups regularly to ensure they can be restored effectively.
- status: ✅ ingested 2026-10-15 · 239 lines · speaker auto (voiceprint 0.74 + name mentioned) · 87 flagged <!-- managed -->

### Notes

## How to Ace SOC2 in SaaS Scale Ups
- id: how-to-ace-soc2-in-saas-scale-ups <!-- managed -->
- url: https://www.youtube.com/watch?v=HieEWiTy2zQ
- format: talk <!-- guessed from 2 voice(s); fix if wrong -->
- date: 2023-11-06
- event: Sprinto
- category:
- topics: Compliance & SOC 2, Startup Security
- summary: Ayman explains that SOC 2 is not a certification but a report on controls, emphasizing the importance of organizational maturity, especially in people operations and IT. He highlights the need for automation in onboarding, access reviews, and training, and advises SaaS companies to identify critical vendors and ensure proper incident notification channels. He also discusses the importance of single sign-on and multi-factor authentication in improving security and streamlining access management.
- status: ✅ ingested 2026-10-15 · 382 lines · speaker auto (voiceprint 0.82 + name mentioned) · 59 flagged <!-- managed -->

### Notes

## Crowdstrike Global IT Outage Explained! (Hint: Not a Cyber Incident!)
- id: crowdstrike-global-it-outage-explained-hint-not-a-cyber <!-- managed -->
- url: https://www.youtube.com/watch?v=W0jmdDJ7jZQ
- format: talk
- date: 2024-07-21
- event: Coffee With Ayman - Security Cafe
- category:
- topics: vCISO & Leadership
- summary: Ayman explains that the CrowdStrike outage was caused by a software bug in an anti-malware update that crashed Windows systems worldwide, leading to widespread disruptions in critical infrastructure. He emphasizes that this was not a cybersecurity incident but a flaw in the update process, and highlights the challenges of recovering affected systems, including the need to manually access encryption keys or restore from backups. Ayman advises organizations to make their systems more resilient and to reconsider automatic updates for critical production environments.
- status: ✅ ingested 2026-10-15 · 136 lines · speaker auto (voiceprint 0.89 + name mentioned) · 28 flagged <!-- managed -->

### Notes

## Protecting Your Data: Disabling Google Takeout in Google Workspace
- id: protecting-your-data-disabling-google-takeout-in-google <!-- managed -->
- url: https://www.youtube.com/watch?v=k42FP6Jz0Ao
- format: talk
- date: 2024-07-07
- event: Coffee With Ayman - Security Cafe
- category:
- topics: Identity & Data Protection
- summary: Ayman explains how to disable Google Takeout in Google Workspace to prevent users from downloading sensitive company data such as emails and Drive files. He demonstrates disabling the feature through the Google Admin Console and suggests creating exception groups for users who may need temporary access. Ayman also emphasizes the importance of reviewing and adjusting default settings to enhance overall security in Google Workspace.
- status: ✅ ingested 2026-10-15 · 64 lines · speaker auto (voiceprint 0.89 + name mentioned) · 12 flagged <!-- managed -->

### Notes

## Security Expert Just Wants To Share Everything He Knows
- id: security-expert-just-wants-to-share-everything-he-knows <!-- managed -->
- url: https://www.youtube.com/watch?v=ghYwm8aRMAg
- format: talk
- date: 2024-07-04
- event: Coffee With Ayman - Security Cafe
- category:
- topics: vCISO & Leadership, Startup Security
- summary: Ayman explains his motivation for creating a book, podcast, and YouTube channel to make cybersecurity more accessible to beginners and startups. He discusses his work as a fractional CISO, helping small companies gain security expertise without hiring a full-time chief information security officer. He also mentions upcoming courses and a community to support people interested in learning about cybersecurity.
- status: ✅ ingested 2026-10-15 · 28 lines · speaker auto (voiceprint 0.86 + name mentioned) · 1 flagged <!-- managed -->

### Notes

## Important Consideration When Trying To Be a vCISO
- id: important-consideration-when-trying-to-be-a-vciso <!-- managed -->
- url: https://www.youtube.com/watch?v=v46vosJdxfk
- format: talk
- date: 2024-03-17
- event: Coffee With Ayman - Security Cafe
- category:
- topics: vCISO & Leadership
- summary: Ayman explains the mindset shift required when transitioning from a full-time CISO to a fractional or virtual CISO, emphasizing the additional responsibilities such as accounting, scheduling, and client management. He discusses the different types of vCISOs, the challenges in the market, and the importance of customer success in running a vCISO business.
- status: ✅ ingested 2026-10-15 · 15 lines · speaker auto (voiceprint 0.83 + solo recording) · 1 flagged <!-- managed -->

### Notes

## Uncover Security Risks With A Technical Risk Assessment
- id: uncover-security-risks-with-a-technical-risk-assessment <!-- managed -->
- url: https://www.youtube.com/watch?v=Swqww9iXcjo
- format: talk
- date: 2025-07-17
- event: Coffee With Ayman - Security Cafe
- category:
- topics: vCISO & Leadership, Compliance & SOC 2
- summary: Ayman explains the importance of a technical risk assessment in identifying security risks that may not be covered by compliance programs like SOC 2. He emphasizes that assessments should be tailored to an organization's specific environment and prioritize risks based on the company's unique needs. He recommends conducting on-site interviews and creating a one-year roadmap to address identified risks.
- status: ✅ ingested 2026-10-15 · 17 lines · speaker auto (voiceprint 0.85 + solo recording) · 0 flagged <!-- managed -->

### Notes

## DEFCON Trailer
- id: defcon-trailer <!-- managed -->
- url: https://www.youtube.com/watch?v=8wQ03qZpqjY
- format: talk
- date: 2025-08-03
- event: Coffee With Ayman - Security Cafe
- category:
- topics: Careers
- summary: Ayman shares his excitement for DEFCON, highlighting the event's atmosphere of innovation and hacking. He mentions the variety of activities, including car hacking and IoT challenges, and the mix of participants from different backgrounds. He emphasizes the thrill of exchanging exploits and competing in skill-based challenges.
- status: ✅ ingested 2026-10-15 · 10 lines · speaker auto (voiceprint 0.69 + solo recording) · 2 flagged <!-- managed -->

### Notes

## The problem with being THAT security person...
- id: the-problem-with-being-that-security-person <!-- managed -->
- url: https://www.youtube.com/shorts/wPwsehUhFa8
- format: talk
- date: 2024-01-24
- event: Coffee With Ayman - Security Cafe
- category:
- topics: vCISO & Leadership
- summary: Ayman illustrates the challenges of being perceived as the "security person" by demonstrating a scenario where he asks someone to install a security agent, despite being seen as an outsider. He highlights the difficulty of gaining cooperation and trust in security efforts, and emphasizes the importance of clear communication and policy enforcement in ensuring compliance.
- status: ✅ ingested 2026-10-15 · 25 lines · speaker auto (voiceprint 0.83 + solo recording) · 0 flagged <!-- managed -->

### Notes

## Startup Security Simplified: Prioritize What Matters for Growth
- id: startup-security-simplified-prioritize-what-matters-for <!-- managed -->
- url: https://www.youtube.com/shorts/1iZPeYAo_Nw
- format: talk
- date: 2023-11-27
- event: Coffee With Ayman - Security Cafe
- category:
- topics: Startup Security
- summary: Ayman explains that startups often struggle with knowing what security measures to prioritize. He advises focusing on protecting customer data and enabling business growth by identifying immediate security needs. He emphasizes creating a clear timeline for security actions, starting from day zero.
- status: ✅ ingested 2026-10-15 · 11 lines · speaker auto (voiceprint 0.79 + solo recording) · 0 flagged <!-- managed -->

### Notes

## SOC2 vs. ISO for Startups: Key Differences Explained | Cybersecurity Essentials
- id: soc2-vs-iso-for-startups-key-differences-explained <!-- managed -->
- url: https://www.youtube.com/shorts/npfKNYz-9Ks
- format: talk
- date: 2023-11-23
- event: Coffee With Ayman - Security Cafe
- category:
- topics: Compliance & SOC 2, Startup Security
- summary: Ayman explains that SOC 2 focuses on data security with five criteria, including availability, integrity, privacy, confidentiality, and security, and is primarily aimed at service providers, especially in the U.S. He notes that ISO is more policy-oriented, recognized internationally, and involves a longer three-year journey, but may be more suitable for companies with international customers. Ayman advises startups to choose based on their customers' requirements, highlighting that there is significant overlap between the two standards but they differ in scope and approach.
- status: ✅ ingested 2026-10-15 · 18 lines · speaker auto (voiceprint 0.79 + solo recording) · 0 flagged <!-- managed -->

### Notes

## Mastering Security Logging: Essential Tips for SaaS & B2B Companies
- id: mastering-security-logging-essential-tips-for-saas-b2b <!-- managed -->
- url: https://www.youtube.com/shorts/zQiu947XEWI
- format: talk
- date: 2023-11-22
- event: Coffee With Ayman - Security Cafe
- category:
- topics: Startup Security, Cloud Security
- summary: Ayman explains the importance of security logging for SaaS and B2B companies, emphasizing the need for situational awareness through logging user activities and system events. He recommends starting by enabling logging features such as AWS CloudTrail and sending logs to tools like Sumo, Splunk, or Datadog for analysis and searchability.
- status: ✅ ingested 2026-10-15 · 12 lines · speaker auto (voiceprint 0.83 + name mentioned) · 6 flagged <!-- managed -->

### Notes

## Ban Shared Credentials: Elevate Your Company's Security | Cybersecurity Tips
- id: ban-shared-credentials-elevate-your-company-s-security <!-- managed -->
- url: https://www.youtube.com/shorts/4GVhdBbxc2E
- format: talk
- date: 2023-11-18
- event: Coffee With Ayman - Security Cafe
- category:
- topics: Identity & Data Protection, Startup Security
- summary: Ayman explains the importance of eliminating shared credentials in an organization to improve security and enable proper attribution during security events. He emphasizes that each person should have unique credentials and highlights the value of strengthening password requirements as a key step in enhancing authentication practices.
- status: ✅ ingested 2026-10-15 · 11 lines · speaker auto (voiceprint 0.82 + solo recording) · 0 flagged <!-- managed -->

### Notes

## Is Your Startup Safe? Quick SSO & Authentication Tips for SaaS Security
- id: is-your-startup-safe-quick-sso-authentication-tips-for-saas <!-- managed -->
- url: https://www.youtube.com/shorts/1094CjmaER0
- format: talk
- date: 2023-11-16
- event: Coffee With Ayman - Security Cafe
- category:
- topics: Identity & Data Protection, Startup Security
- summary: Ayman explains that startups should begin with authentication and logging to improve security. He recommends implementing SSO to centralize access control and ensure former employees lose access automatically. He also highlights the value of context-aware authentication, which can detect suspicious login activity based on location and timing.
- status: ✅ ingested 2026-10-15 · 9 lines · speaker auto (voiceprint 0.78 + solo recording) · 3 flagged <!-- managed -->

### Notes

## BSides SF 2025 Vlog - Interview with Ayman ElSawah + Meeting Jason Haddix & Tanya Janca!
- id: bsides-sf-2025-vlog-interview-with-ayman-elsawah-meeting <!-- managed -->
- url: https://www.youtube.com/watch?v=7x_VJLEIuQA
- format: interview <!-- guessed from 2 voice(s); fix if wrong -->
- date: 2025-04-26 <!-- BSidesSF 2025 ran Apr 26-27; exact day unknown -->
- event: Three Headed Beast Security
- category:
- topics: Careers, AI Security
- summary: Ayman advises first-time conference attendees to engage in a variety of activities, such as attending talks, visiting villages, and networking with people in line or during breaks. He emphasizes the importance of adaptability and a broad understanding of the security field for those starting in cybersecurity, and he highlights the impact of AI on the industry, noting that it will automate many routine tasks but also increase the need for skilled professionals who can work alongside AI tools.
- status: ✅ ingested 2026-10-15 · 131 lines · speaker auto (voiceprint 0.74 + name mentioned) · 13 flagged <!-- managed -->

### Notes

## Balancing Life and the Addiction to Productivity w/ Ayman Elsawah
- id: balancing-life-and-the-addiction-to-productivity-w-ayman <!-- managed -->
- url: https://www.youtube.com/watch?v=uQOCK0y_PD4
- format: interview <!-- guessed from 2 voice(s); fix if wrong -->
- date: 2024-07-12
- event: BlakeWilliamsHQ
- category:
- topics: Careers
- summary: Ayman discusses the pressure of overworking and the need to find a sustainable work pace, especially for single parents. He emphasizes the importance of unplugging from the constant drive for productivity and suggests planning long-term goals to achieve balance. He also highlights the value of community and support structures in managing work-life balance.
- status: ✅ ingested 2026-10-15 · 61 lines · speaker auto (voiceprint 0.81 + name mentioned) · 6 flagged <!-- managed -->

### Notes

## How to become a Cybersecurity professional  | Ayman Elsawah
- id: how-to-become-a-cybersecurity-professional-ayman-elsawah <!-- managed -->
- url: https://www.youtube.com/watch?v=iDv0-AY7J84
- format: talk <!-- guessed from 1 voice(s); fix if wrong -->
- date: 2021-12-06
- event: Haythem Hammour
- category:
- topics: Careers
- summary: Ayman explains that becoming a cybersecurity professional can start from various backgrounds and that the field includes many roles beyond hacking or penetration testing. He suggests leveraging existing skills, such as those from web development or linguistics, and recommends using the NICE framework to explore different cybersecurity positions and find a good fit.
- status: ✅ ingested 2026-10-15 · 10 lines · speaker auto (voiceprint 0.78 + solo recording) · 2 flagged <!-- managed -->

### Notes

## How Do You Protect Data on Endpoints | Cybersecurity on the Street | Interviews
- id: how-do-you-protect-data-on-endpoints-cybersecurity-on-the <!-- managed -->
- url: https://www.youtube.com/watch?v=q4syDUQxLJg
- format: montage  <!-- guessed from 7 voice(s); fix if wrong -->
- date: 2020-04-29
- event: Absolute Security
- category:
- topics: Identity & Data Protection
- summary: Ayman points out that many companies are not effectively protecting their data on endpoints, leading to frequent breaches. He emphasizes the need for better endpoint security measures.
- status: ✅ ingested 2026-10-15 · 2 lines · montage: 2 snippet(s) match the voiceprint · 4 flagged <!-- managed -->

### Notes

## How do you protect your remote employees? | Cybersecurity on the Street | Interviews
- id: how-do-you-protect-your-remote-employees-cybersecurity-on <!-- managed -->
- url: https://www.youtube.com/watch?v=zocUc7bzQAc
- format: montage  <!-- guessed from 2 voice(s); fix if wrong -->
- date: 2020-03-27
- event: Absolute Security
- category:
- topics: Identity & Data Protection
- summary: Ayman emphasizes the importance of tracking data access by remote employees, advocating for the zero trust security model. He stresses the need to know who accessed data, when, and where, regardless of location.
- status: ✅ ingested 2026-10-15 · 2 lines · montage: 2 snippet(s) match the voiceprint · 8 flagged <!-- managed -->

### Notes

## Data Security in the AI Era, Don't Let AI Ruin your Presentation, and the Weekly News - ESW #480
- id: data-security-in-the-ai-era-don-t-let-ai-ruin-your <!-- managed -->
- url: https://www.youtube.com/watch?v=6a2-W3WDGhg
- format: cohost
- date: 2026-10-12
- event: Enterprise Security Weekly w/Adrian Sanabria
- category:
- topics: AI Security, Identity & Data Protection
- summary: Ayman discusses the importance of simplifying presentation slides, emphasizing readability and avoiding over-reliance on AI tools that can amplify poor content. He also highlights reducing exposure as a key data security strategy, suggesting limiting access to sensitive information and focusing on preventative measures. Additionally, he reflects on the risks of AI in software development, noting potential issues with supply chain security if AI-generated code becomes widespread.
- status: ✅ ingested 2026-10-15 · 278 lines · speaker auto (voiceprint 0.86 + name mentioned) · 181 flagged <!-- managed -->

### Notes

## Cyber Resilience with Cohesity, When to use AI for Writing, and the News - Rob Sadowski - ESW #477
- id: cyber-resilience-with-cohesity-when-to-use-ai-for-writing <!-- managed -->
- url: https://www.youtube.com/watch?v=6sZm4oA-iaU
- format: cohost
- date: 2026-09-21
- event: Enterprise Security Weekly w/Adrian Sanabria
- category:
- topics: AI Security, Identity & Data Protection
- summary: Ayman discusses concerns about AI-generated content replacing human writing, noting the risk of people losing writing skills and the potential for AI to create a feedback loop of AI-generated content consumed by AI. He also highlights the misuse of AI in cyber attacks, such as stealing credentials and harvesting API keys from apps, emphasizing the importance of securing keys and improving security practices in startups.
- status: ✅ ingested 2026-10-15 · 208 lines · speaker auto (voiceprint 0.89 + name mentioned) · 100 flagged <!-- managed -->

### Notes

## Can employees safely use AI agents? AI pentesting agent liabilities, and the news - ESW #473
- id: can-employees-safely-use-ai-agents-ai-pentesting-agent <!-- managed -->
- url: https://youtu.be/o-Edp9puMEo?si=71SjUt1akYGDx4vH
- format: cohost
- date: 2026-08-24
- event: Enterprise Security Weekly w/Adrian Sanabria
- category:
- topics: AI Security
- summary: Ayman discusses the use of AI in pentesting, emphasizing the need for human oversight and the value of custom harnesses to ensure accurate and novel testing. He also highlights the challenges of using AI for security, including the need for open source models and the potential for AI to both create and solve security issues. Additionally, he comments on the implications of AI in content creation and the importance of transparency in its use.
- status: ✅ ingested 2026-10-15 · 199 lines · speaker auto (voiceprint 0.85 + name mentioned) · 174 flagged <!-- managed -->

### Notes

## Fixing pentesting, Meta is destroying its engineering org, the weekly news  - ESW #465
- id: fixing-pentesting-meta-is-destroying-its-engineering-org-the <!-- managed -->
- url: https://www.youtube.com/watch?v=DRg-qoTIvJE
- format: cohost
- date: 2026-06-29
- event: Enterprise Security Weekly w/Adrian Sanabria
- category:
- topics: AI Security
- summary: Ayman discusses how AI is changing the role of engineers, noting that while it can make tasks easier, it also increases the volume of work, such as code reviews. He highlights concerns about AI training methods, including the use of human feedback and the potential for poor quality outputs. Ayman also mentions security practices, such as using internal repositories for software packages to improve supply chain safety.
- status: ✅ ingested 2026-10-15 · 233 lines · speaker auto (voiceprint 0.84 + name mentioned) · 172 flagged <!-- managed -->

### Notes

## The State of Cybersecurity Hiring, 2026 content plans, and the weekly news - ESW #441
- id: the-state-of-cybersecurity-hiring-2026-content-plans-and-the <!-- managed -->
- url: https://www.youtube.com/watch?v=cTkQz2DGJRg
- format: cohost
- date: 2026-01-12
- event: Enterprise Security Weekly w/Adrian Sanabria
- category:
- topics: Careers, AI Security
- summary: Ayman discusses the current state of cybersecurity hiring, noting that the job market has improved slightly but still requires candidates to demonstrate a broader range of skills, including the use of AI and modern tools. He suggests that aspiring professionals can gain valuable experience by working on personal projects, such as deploying open-source applications or learning DevOps practices, to build practical skills that are in demand.
- status: ✅ ingested 2026-10-15 · 172 lines · speaker auto (voiceprint 0.85 + name mentioned) · 156 flagged <!-- managed -->

### Notes

## ESW at BlackHat and the weekly enterprise security news - ESW #419
- id: esw-at-blackhat-and-the-weekly-enterprise-security-news-esw <!-- managed -->
- url: https://www.youtube.com/watch?v=Dq8_NlDm-A0
- format: cohost
- date: 2025-08-11
- event: Enterprise Security Weekly w/Adrian Sanabria
- category:
- topics: AI Security, Identity & Data Protection, Careers
- summary: Ayman discusses the growing importance of identity in cybersecurity, highlights the rapid consolidation in the industry, and expresses cautious optimism about AI's potential in security. He emphasizes the need for better workforce development, including hiring based on aptitude and learning ability, and stresses the importance of ethical considerations in AI and security practices.
- status: ✅ ingested 2026-10-15 · 384 lines · speaker auto (voiceprint 0.79 + name mentioned) · 68 flagged <!-- managed -->

### Notes

## The Cyber Canon, ditching the SOC 2, and the weekly enterprise news - Helen Patton - ESW #416
- id: the-cyber-canon-ditching-the-soc-2-and-the-weekly-enterprise <!-- managed -->
- url: https://www.youtube.com/watch?v=ddA0I3fGRHA
- format: cohost
- date: 2025-07-21
- event: Enterprise Security Weekly w/Adrian Sanabria
- category:
- topics: Compliance & SOC 2, Startup Security
- summary: Ayman discusses the limitations and issues with SOC 2, explaining that it is not prescriptive and can give a false sense of security. He advises delaying SOC 2 until necessary and instead focusing on practical security measures like the Minimum Viable Secure Product (MVSP). He emphasizes the importance of designing security controls thoughtfully and not relying solely on compliance frameworks.
- status: ✅ ingested 2026-10-15 · 311 lines · speaker auto (voiceprint 0.86 + name mentioned) · 164 flagged <!-- managed -->

### Notes

## Getting AI Pilled Without Getting Breached
- id: getting-ai-pilled-without-getting-breached <!-- managed -->
- url: https://youtu.be/gNhybzC33ek
- format: interview
- date: 2026-07-29 <!-- per Ayman -->
- event: Coffee With Ayman - Security Cafe
- category:
- topics: AI Security
- summary: Ayman explains the importance of visibility into AI tool usage, segmenting users by risk profile, and implementing preventative controls such as limiting access to corporate-sanctioned tools. He emphasizes the need for education and collaboration with business teams to ensure secure AI adoption, while also highlighting the role of legal frameworks like BAA and ZDR in securing sensitive data.
- status: ✅ ingested 2026-10-15 · 444 lines · speaker auto (voiceprint 0.86 + name mentioned) · 111 flagged <!-- managed -->

### Notes
