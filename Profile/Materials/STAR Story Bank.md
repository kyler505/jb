---
type: reference
title: STAR Story Bank
---

# STAR Story Bank

> Pre-written behavioral stories in **S**ituation · **T**ask · **A**ction · **R**esult form. Reuse across interviews. Tighten wording in your own voice and fill the {{gaps}}.

## Competency coverage
| Story | Covers |
|-------|--------|
| Sprint conflict (CSCE 331 / Panda Express POS) | conflict, leadership, accountability, data-driven decisions |
| ADSC project step-away | failure, self-awareness, prioritization, integrity |
| DMS production deploy | resilience, debugging, ownership, learning |
| Earning the TechHub devs' trust | reliability, growth, initiative |
| Project SHADE LSTM | technical challenge, ML, perseverance |
| Personal website in Rust | fast learning, initiative |

---

### Sprint conflict — CSCE 331 Panda Express POS modernization
*Best for: conflict on a team · leadership/influence · holding people accountable*
- **Situation:** Fall 2025 software-engineering class (CSCE 331); 5-person team modernizing a Panda Express point-of-sale system. I was **scrum master**.
- **Task:** Early on, 2 of 5 members were contributing little to nothing, putting our sprint goals at risk.
- **Action:** Rather than call them out publicly, I analyzed **sprint metrics and git commit activity** to understand the gap objectively, then held **one-on-one check-ins**. One teammate was dealing with personal issues, the other was struggling to balance coursework. I **rebuilt the sprint board and re-delegated responsibilities** to fit realistic capacity and enforced clearer accountability in sprint meetings.
- **Result:** Contributions evened out and the team delivered. {{Add the outcome — e.g. shipped the POS modernization / grade / what the team said.}}

### Stepping away from the ADSC project
*Best for: a time you failed · overcommitting · prioritization · integrity*
- **Situation:** Sophomore year, I was selected for an ADSC project while carrying a heavy course load.
- **Task:** I'd committed to contributing at a high level but realized I had underestimated the time required.
- **Action:** Rather than stretch myself thin and underperform, I took responsibility for overcommitting and **made the decision to step away**.
- **Result:** It taught me to evaluate commitments realistically before saying yes. Since then I assess workload carefully, build buffers into my schedule, and only commit when I know I can deliver consistently.

### Getting the DMS to production
*Best for: resilience · debugging · ownership · "didn't work as expected"*
- **Situation:** I built a full-stack **delivery management system** (Flask, React, MySQL) for TechHub to handle order processing.
- **Task:** Take it from working-locally to running reliably in production for real staff use.
- **Action:** The deploy surfaced many unexpected errors — things that worked in dev broke in prod. I worked through them systematically, found workarounds and fixes, and hardened the system.
- **Result:** It now processes **150+ orders/month at 99.8% uptime** with automated order-history audit tracking. {{Add a specific bug you squashed for color.}}

### Earning the TechHub developers' trust
*Best for: reliability · proving yourself · initiative*
- **Situation:** When I joined TechHub as a student technician, the senior software developers were doubtful of my abilities and experience.
- **Task:** Become someone the team could depend on for real engineering work, not just hardware tasks.
- **Action:** I took on full-stack development and debugging tasks, delivered them consistently, and contributed to **8+ internal tools**.
- **Result:** They now rely on me to build full-stack systems and debug workflow problems on my own.

### Project SHADE — building the LSTM component
*Best for: hardest technical problem · ML · perseverance*
- **Situation:** A team heat-wave prediction system (Sept-Dec 2025); I was on the **LSTM subteam**.
- **Task:** Build the LSTM component and integrate it with SEIR-based epidemiological modeling.
- **Action:** Built a pipeline over **500K+ data points** (cleaning, feature engineering — temporal lags, rolling stats), then designed and tuned the LSTM (hyperparameter optimization, sequence-length tuning).
- **Result:** **87% validation accuracy**; improved model-level accuracy by **23%**. {{What was the hardest part / what you'd do differently.}}

---

## Prompts still to prepare (notes only)
- **Tell me about a time you led a team** — reuse the sprint-conflict story (scrum master angle).
- **A time you made a mistake** — {{draft one — possibly an early DMS bug pushed to prod, and how you caught/fixed it.}}
- **Believed in something no one else did** — {{draft — possibly pushing for the DMS tool or a tech choice at TechHub.}}
- **Manage your time / prioritize** — {{draft — balancing TechHub work + heavy CS coursework; the ADSC lesson applied.}}