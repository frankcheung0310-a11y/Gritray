# Beyond Patrol Cleaning: A Camera-Centric Architecture for Event-Driven Autonomous Cleaning Systems

**Galileo Lab · Technical Report v1.0**

---

## Abstract

Most autonomous cleaning robots operate under a patrol-based paradigm. The robot continuously traverses a predefined environment, using onboard sensors to detect dirt, debris, or spills encountered during navigation. While effective in small and predictable environments, this architecture scales poorly in large facilities where contamination events are sparse, spatially localized, and temporally unpredictable.

This paper proposes a **Camera-Centric Cleaning Architecture (CCCA)**, in which environmental perception is decoupled from robotic mobility. Instead of relying on the robot to discover cleaning opportunities, a network of fixed cameras continuously monitors the environment, identifies cleaning events, and dispatches tasks to available cleaning robots.

The proposed architecture transforms cleaning from a patrol-driven process into an event-driven system, reducing unnecessary robot movement while improving response time, operational efficiency, and scalability.

---

# 1. Introduction

Autonomous cleaning systems have become increasingly common in warehouses, airports, shopping centers, hospitals, and industrial facilities. Most commercial solutions follow a simple operational principle:

1. Navigate through an environment.
2. Detect contamination during navigation.
3. Execute cleaning actions.
4. Continue patrolling.

This approach implicitly assumes that the robot must act as both:

- A sensing platform
- A cleaning platform

However, this dual-role architecture introduces inefficiencies.

In large facilities, contamination typically occupies less than 1% of the total floor area at any given moment. Consequently, robots spend the majority of their operational time searching rather than cleaning.

This observation motivates a different question:

> Should robots be responsible for discovering cleaning tasks, or should the environment itself perform that function?

---

# 2. Patrol-Based Systems and Their Limitations

Current cleaning robots rely primarily on onboard sensing systems, including:

- RGB cameras
- LiDAR
- Depth sensors
- Ultrasonic sensors

These sensors enable autonomous navigation and obstacle avoidance but create a fundamental operational constraint:

The robot can only perceive locations it physically visits.

As a result:

| Metric | Patrol-Based Architecture |
|----------|----------|
| Discovery latency | Depends on patrol cycle |
| Coverage efficiency | Low |
| Energy consumption | High |
| Scalability | Limited |
| Response time | Variable |

Consider a warehouse aisle where a spill occurs immediately after a robot has passed.

The spill may remain undetected for:

- 30 minutes
- 1 hour
- Several hours

depending on patrol frequency.

This delay is a direct consequence of coupling perception to mobility.

---

# 3. Camera-Centric Cleaning Architecture

We propose a system in which environmental perception is externalized.

Instead of the robot discovering contamination, a fixed sensing network continuously observes the facility.

The architecture consists of four layers:

```text
Camera Layer
      ↓
Perception Layer
      ↓
Spatial Task Layer
      ↓
Robot Execution Layer
```

---

# 4. Observation Layer

The observation layer consists of fixed cameras positioned throughout the facility.

Typical deployment locations include:

- Warehouse aisles
- Production corridors
- Loading docks
- Shopping mall walkways
- Airport terminals

Each camera continuously streams visual data.

Unlike mobile sensors, fixed cameras offer:

- Persistent observation
- Stable viewpoints
- Continuous coverage
- Low maintenance

The environment effectively becomes a distributed sensing platform.

---

# 5. Perception Layer

Visual streams are processed using computer vision models.

Potential tasks include:

### Contamination Detection

Examples:

- Paper debris
- Packaging material
- Dust accumulation
- Liquid spills

### Obstacle Detection

Examples:

- Fallen objects
- Blocked pathways
- Unexpected inventory placement

### Environmental Monitoring

Examples:

- Floor condition assessment
- Traffic density estimation
- Area utilization statistics

Modern object detection frameworks such as:

- YOLO
- RT-DETR
- Grounding DINO

provide sufficient performance for real-time deployment.

---

# 6. Spatial Task Representation

Detected events are transformed into spatial tasks.

The facility is discretized into grid cells:

```text
1m × 1m
```

or

```text
0.5m × 0.5m
```

depending on operational requirements.

Each cell maintains a state vector:

```json
{
  "occupancy": 0,
  "dirty_score": 0.93,
  "last_update": "2026-05-24T10:35:00Z"
}
```

This creates a continuously updated digital representation of facility cleanliness.

Instead of storing geometry, the system stores operational state.

---

# 7. Event-Driven Dispatch

When contamination exceeds a predefined threshold:

```text
dirty_score > threshold
```

a cleaning task is generated.

Example:

```json
{
  "task_id": 1542,
  "location": "Aisle-7",
  "cell": "B4",
  "priority": "High"
}
```

The task is then dispatched to:

- Autonomous cleaning robots
- Human operators
- Hybrid fleets

The robot no longer searches for work.

The environment assigns work.

---

# 8. Multi-Robot Scalability

One major advantage of camera-centric perception is scalability.

In conventional architectures:

```text
N Robots
=
N Perception Systems
```

Every robot requires:

- Cameras
- Sensors
- Detection algorithms

In the proposed architecture:

```text
1 Environment Model
+
N Robots
```

The perception infrastructure becomes shared.

This reduces:

- Computational redundancy
- Hardware costs
- Fleet management complexity

while increasing system-wide awareness.

---

# 9. Predictive Cleaning

Beyond reactive cleaning, the system enables predictive behavior.

Historical contamination events can be accumulated:

```text
Location
Time
Frequency
Severity
```

Machine learning models can estimate:

```text
P(Contamination | Location, Time)
```

For example:

| Location | Predicted Probability |
|-----------|-----------|
| Aisle 3 | 82% |
| Dock 5 | 74% |
| Corridor 8 | 69% |

Robots can then pre-position themselves before contamination events occur.

Cleaning transitions from:

```text
Reactive
```

to

```text
Predictive
```

operations.

---

# 10. Integration with Existing Robot Fleets

An important characteristic of the architecture is vendor independence.

The perception system operates separately from robot hardware.

Any robot capable of receiving location commands can participate.

Examples include:

- Cleaning robots
- Mobile manipulators
- AMRs
- Human-operated equipment

The system therefore functions as an environmental intelligence layer rather than a robot product.

---

# 11. Economic Implications

The proposed architecture changes the economics of autonomous cleaning.

Traditional model:

```text
Robot = Perception + Navigation + Cleaning
```

Proposed model:

```text
Environment Intelligence
+
Robot Execution
```

This separation allows facility operators to:

- Upgrade perception independently
- Reuse existing robot fleets
- Add robots without redesigning sensing infrastructure

The result is a more modular and scalable deployment strategy.

---

# 12. Future Directions

Future research may extend the architecture toward:

### Facility World Models

Persistent digital representations of operational environments.

### Multi-Agent Coordination

Shared task allocation across heterogeneous robots.

### Predictive Facility Management

Forecasting maintenance, cleanliness, and operational risks.

### Physical AI Systems

Integrating perception, planning, and execution into a continuously updated environmental model.

---

# 13. Conclusion

Current autonomous cleaning systems remain largely constrained by patrol-based operational paradigms.

This paper proposes a camera-centric alternative in which perception is moved from the robot into the environment itself.

By separating observation from execution, facilities gain:

- Faster contamination detection
- Reduced robot travel
- Improved scalability
- Shared environmental awareness
- Predictive cleaning capabilities

The central idea is simple:

> Robots should clean.  
> The environment should decide when cleaning is needed.

As sensing infrastructure becomes increasingly affordable and AI perception continues to improve, camera-centric architectures may become a foundational design pattern for large-scale autonomous facility management.

---

**Galileo Lab**

*Researching Physical AI Systems, Facility Intelligence, and Environmental World Models.*
