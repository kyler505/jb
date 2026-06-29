---
type: application-essay
company: Palantir
role: Software Engineer, Internship - Production Infrastructure (Foundations)
date: 2026-06-29
source: Lever / Simplify
tags:
  - palantir
  - application-essay
  - production-infrastructure
---

# Palantir Application Essays

## If Palantir didn't exist, what kind of company or work would you be most excited and interested in working at/on? (Approx. 200 words)

If Palantir didn't exist, I'd find the same kind of work somewhere else. Defense tech, critical infrastructure, operations logistics. Places where the thing you build actually does something, and when it breaks someone notices.

My internship is at an ERP company. I build tools that people use every day to process orders and manage inventory. What surprised me is how much I care about whether that stuff actually works in the real world. An edge case isn't a footnote. It's someone's shipment not going out.

So I'd look at Anduril, Skydio, Shield AI. Or operational companies like Flexport, Tesla, maybe SpaceX. Even a trading firm, honestly. Anywhere where the data is messy, the stakes are real, and you don't have to squint to see whether your code mattered.

The common thread across all of them is that the work lives at the intersection of software and the actual thing: you can't build the system without understanding the domain first.

## What is the hardest technical challenge you've faced as part of work experience or a personal project? (Approx. 200 words)

The hardest technical challenge I've faced was building a shared compilation environment for an ERP company still running COBOL. The problem was simple to state and messy to solve: several developers needed to compile COBOL projects, but there was only one licensed VM with the compiler, and nobody could use it while someone else had a session open.

My first approach was a shared filesystem + SSH queue. That worked technically but was terrible in practice. People forgot to release the lock, sessions timed out, and we had no visibility into what was running.

I rebuilt it as a React dashboard with a .NET backend that talks directly to the VM. It manages a job queue, provisions the compiler when a slot opens, and streams compile output back to the browser in real time. The hard part wasn't any single piece of it. It was that every assumption I made about the COBOL toolchain was wrong. Error codes that meant different things in different contexts. A compiler that couldn't handle concurrent file access, even from different directories. A build pipeline that expected interactive input on stdin despite being batch-oriented.

I ended up having to wrap the whole thing in a custom launcher that stages files, patches the build scripts with environment-aware paths, and captures output character by character. It worked. The team stopped stepping on each other, and compile turnaround went from "ask if anyone's using it" to about 90 seconds.

## Tell us one thing that's not on your resume that you're proud of.

I started playing volleyball last year with basically no experience. I'd never played in any organized setting, didn't know rotations, and my first serve was genuinely embarrassing.

A few months in, a friend convinced me to enter Spikefest with his team. I figured we'd get eliminated early and it'd be a fun day. Instead we made it to the semifinals and placed 5th out of 32 teams. The whole thing caught me off guard. I wasn't the weakest link by then, and there were moments in the later matches where I actually made plays that mattered.

That's not on my resume because it doesn't belong there. But it's one of the things I'm proudest of from last year. Learning a new sport from zero and ending up competitive in it faster than I expected made me realize that the hardest part of getting good at something is just deciding to start being bad at it first.

I've kept playing since. Still not great, but a lot better than I was.

## At Palantir we have two main Software Engineering roles: FDSE and SWE. Which resonates most and why?

At Global Shop, the work I've been most absorbed in isn't the frontend features. It's the infrastructure underneath: standing up a shared compilation environment so the team can build COBOL projects without stepping on each other, wiring up TestArchitect VMs into an automated pipeline, getting a .NET 7.0 compiler accessible through a web interface so nobody has to remote into a licensed machine to run a build.

Those weren't glamorous problems. They were about reliability, concurrency, and making the environment invisible so people could just do their work. That's what draws me to infrastructure.

Outside of work, the same pattern holds. I bought a Grace Blackwell machine before PyTorch officially supported the architecture and spent weeks getting it running, not because I needed it for anything specific, but because I wanted to understand the stack from CUDA up. I learned more about memory bandwidth and model quantization debugging CUDA compatibility tables than from any class.

The Production Infrastructure role at Palantir is that same kind of work at a much bigger scale. Building the systems that Palantir's platforms depend on, making them reliable and fast so the people building on top don't have to think about it. That's what I actually want to do.

## Preferred Palantir Product(s)

Apollo is the obvious choice for me.

Palantir deploys into some of the hardest environments I know of. Classified networks, disconnected sites, critical infrastructure where downtime means something real. Apollo sits underneath all of it. Continuous deployment, release management, day 2 operations.

What I like about it is simple. Building the platform is one problem. Getting it running somewhere the network drops twice a day, keeping it reliable when you can't SSH in, making sure the people depending on it trust what's deployed. That's a harder problem, and it's the one I'd rather work on.

Foundry too. Not for the data pipelines. The ontology. Treating business objects as real things with lineage and actions built in makes more sense than most data platforms I've seen. I'd want to build infrastructure underneath that.
