# Beyond World Models: A Multi-Scale Control Architecture for Physical AI

*July 3, 2026*

---

## Abstract

Current research in world models has focused primarily on perception and prediction. Tremendous effort has been devoted to enabling AI systems to reconstruct physical environments, understand object dynamics, and forecast future states from visual observations. These capabilities represent essential foundations of Physical AI, yet they do not answer a more fundamental question: once multiple intelligent agents coexist inside the same physical environment, who is responsible for maintaining order?

This paper argues that perception alone is insufficient for Physical AI. A robot may perfectly understand the geometry of its surroundings, accurately estimate physical interactions, and successfully predict the consequences of its own actions. However, the physical world is rarely composed of a single agent. Warehouses, factories, roads, hospitals, and cities are environments in which hundreds or even millions of autonomous systems continuously influence one another. Intelligence therefore becomes a coordination problem rather than merely a perception problem.

We propose a hierarchical control architecture consisting of four conceptual layers: **Gritray**, **Fricial**, **Artifriction**, and **Resonial**, together forming the local intelligence stack of Physical AI. Above these layers, we further introduce **Starray**, a planetary-scale supervisory system responsible for maintaining global stability through rare but authoritative intervention. This architecture separates local autonomy from global supervision, allowing physical intelligence to scale without requiring centralized control over every decision.

---

## World Models Do Not Fail Because They Cannot See

Much of today's AI research assumes that better perception naturally produces better intelligence. Cameras become higher in resolution, sensors become more accurate, and neural networks become increasingly capable of reconstructing three-dimensional environments. Yet many failures observed in multi-agent systems are not caused by poor perception.

Imagine four autonomous delivery robots arriving at the same narrow intersection. Every robot correctly recognizes the surrounding environment. Every robot predicts the movements of the others. Every robot behaves rationally according to its own objective. Nevertheless, the entire system reaches a deadlock because no individual robot possesses the authority or mechanism to resolve the collective conflict.

The failure is not visual.

The failure is organizational.

Physical intelligence therefore requires mechanisms capable of coordinating multiple independent decision-makers rather than simply improving individual perception.

---

## From Perception to Physical Understanding

Galileo's lower layers describe how an intelligent system constructs an understanding of physical reality.

**Gritray** transforms reflected light into geometric structure, reducing visual complexity into relational representations suitable for reasoning.

**Fricial** describes the physical interactions that emerge between entities once these relationships have been reconstructed. Contact forces, resistance, material constraints, and environmental interactions become explicit components of the world model.

**Artifriction** represents the learned interpretation of these interactions. Instead of explicitly calculating every physical variable, the AI develops internal estimates of traversability, stability, collision probability, and task feasibility through experience.

Together, these three layers answer a single question:

> *What is happening in the physical world?*

However, understanding reality is fundamentally different from coordinating reality.

---

## Resonial: Local Coordination Without Central Authority

Physical environments require continuous coordination among independent agents. Waiting for a centralized controller before every decision would introduce unacceptable latency, communication overhead, and single points of failure.

Resonial is proposed as a decentralized coordination layer operating locally among neighboring agents.

Its objective is not to maximize efficiency.

Its objective is to prevent instability.

When autonomous vehicles approach the same intersection, Resonial negotiates priority.

When warehouse robots share narrow corridors, Resonial resolves movement conflicts.

When multiple service robots operate within hospitals, Resonial maintains safe spatial behavior.

Most importantly, Resonial intervenes before local disagreements become global failures.

Unlike traditional planning algorithms, Resonial does not attempt to optimize the entire world.

It protects the stability of the local world.

This distinction allows thousands of independent local coordination processes to operate simultaneously without overwhelming a centralized controller.

---

## Starray: Global Supervision Above Local Intelligence

Local coordination alone cannot guarantee system-wide stability.

Factories experience emergencies.

Entire transportation networks become congested.

Natural disasters disrupt regional infrastructure.

Communication failures isolate groups of robots.

Under these circumstances, local negotiation is no longer sufficient.

A higher supervisory layer becomes necessary.

This paper introduces **Starray** as that supervisory layer.

Unlike Resonial, Starray does not participate in ordinary decision-making.

Instead, it continuously observes large-scale system behavior through distributed sensing infrastructure, including satellite networks, environmental monitoring systems, and global communication channels. Under normal operating conditions, Starray remains silent.

Its authority exists precisely because it is rarely exercised.

Only when local coordination can no longer preserve global stability does Starray intervene, issuing system-level corrections that restore overall order.

The relationship between Resonial and Starray resembles biological nervous systems. Reflexes are handled locally through the spinal cord because immediate responses cannot wait for the brain. Only complex or system-wide decisions require central supervision. Likewise, Resonial maintains local stability, while Starray preserves planetary stability.

---

## A Multi-Scale Control Theory for Physical AI

This layered architecture separates Physical AI into distinct levels of responsibility.

```text
Reality
    ↓
Gritray
(Structure)

    ↓
Fricial
(Physical Interaction)

    ↓
Artifriction
(Physical Understanding)

    ↓
Resonial
(Local Coordination)

    ↓
Starray
(Global Supervision)
```

Each layer solves a fundamentally different problem.

Perception does not become coordination.

Coordination does not become supervision.

Instead, intelligence emerges through cooperation across multiple scales.

This separation reduces computational complexity, improves scalability, and mirrors organizational principles repeatedly observed in biological systems, distributed computing, and human societies.

---

## Conclusion

The next generation of Physical AI may not be defined by larger foundation models or increasingly realistic world simulations. Its defining challenge will be maintaining stability among millions of intelligent agents operating simultaneously within the same physical world.

Galileo proposes that intelligence should therefore be viewed not merely as perception or prediction, but as a hierarchy of control.

Gritray enables machines to perceive structure.

Fricial enables machines to understand interaction.

Artifriction enables machines to internalize physical intuition.

Resonial enables neighboring agents to cooperate autonomously.

Starray preserves order across the entire system when local coordination reaches its limits.

Future world models will not simply observe reality.

They will continuously organize it.
