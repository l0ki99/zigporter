---
name: brainstorming
description: Turn ideas into fully formed designs through collaborative dialogue before implementation. You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. This ensures ideas are validated and well-designed before coding begins.
argument-hint: "[topic or feature description]"
---

# Brainstorming Skill

The process of turning an idea into an implemented feature involves two critical phases:

1. **Design Phase** (this skill): Turn vague ideas into concrete, validated designs
2. **Implementation Phase**: Execute the validated design with appropriate agents

This skill focuses exclusively on the design phase - ensuring ideas are fully formed and validated before any code is written.

## When to Use This Skill

**You MUST use this skill when:**

- Creating new features or functionality
- Building new components or modules
- Adding significant new behavior
- Making architectural decisions
- Planning complex changes that affect multiple areas
- User says "I want to add..." or "I need to build..."

**Skip this skill when:**

- Fixing obvious bugs with clear solutions
- Making trivial updates (typo fixes, small tweaks)
- Implementing a design that's already been validated
- User provides extremely detailed specifications with no ambiguity

## The Brainstorming Process

### Phase 1: Understanding the Idea

Start by understanding what the user wants to build:

1. **Ask clarifying questions** - One question at a time
2. **Explore the problem space** - Why is this needed?
3. **Understand constraints** - Technical, time, resource limitations
4. **Identify success criteria** - What does "done" look like?

**Principles:**

- Ask one question at a time, wait for the answer
- Don't assume - validate your understanding
- Focus on the "why" before the "how"
- Keep questions specific and actionable

### Phase 2: Designing the Solution

Once you understand the need, design a solution:

1. **Propose an approach** - Present one coherent design idea
2. **Get feedback** - Does this solve the problem?
3. **Iterate** - Refine based on user input
4. **Validate trade-offs** - Discuss pros/cons of key decisions

**Design principles:**

- **YAGNI** (You Aren't Gonna Need It) - Don't over-engineer
- **Start simple** - Minimal viable solution first
- **Incremental** - Can we build this in stages?
- **Concrete** - Specific files, functions, and data structures

### Phase 3: Presenting the Final Design

Present the design in digestible sections:

1. **Overview** - High-level summary (2-3 sentences)
2. **Architecture** - Components, modules, and how they interact
3. **Data Model** - Key data structures, schemas, or entities
4. **API/Interface** - Public interfaces, endpoints, or function signatures
5. **Implementation Steps** - Ordered list of what to build
6. **Trade-offs** - What we're optimizing for and what we're sacrificing

**Present each section separately:**

- Show one section at a time
- Wait for user approval before showing the next section
- Be ready to revise based on feedback
- Don't proceed to implementation until ALL sections are approved

### Phase 4: Validation Checkpoint

Before moving to implementation, confirm:

- [ ] User understands the entire design
- [ ] All sections have been reviewed and approved
- [ ] Trade-offs are acknowledged and accepted
- [ ] Implementation steps are clear and actionable
- [ ] Success criteria are defined

**Ask explicitly:** "Are you ready to proceed with implementation, or should we revise any part of the design?"

## After the Design is Validated

Once the design is approved:

1. **Document the design**:

   - Use the `documentation-writer` agent to create a design document
   - Save to `docs/plans/YYYY-MM-DD-<topic>-design.md`
   - Include all design sections plus validation notes

2. **Transition to implementation**:

   - Hand off to appropriate implementation agents:
     - `fastapi-backend-developer` for backend features
     - `frontend-developer` for UI components
     - `api-designer` for API design
     - `database-specialist` for schema changes

3. **Track progress** (optional):
   - Create Jira issues for tracking (use `jira` skill)
   - Break implementation into tasks if complex

## Integration with Core Agents

This skill feeds into specialized implementation agents:

- **documentation-writer** (`agents/docs/`) - Document validated designs
- **api-designer** (`agents/architecture/`) - Refine API designs
- **fastapi-backend-developer** (`agents/backend/`) - Implement backend features
- **frontend-developer** (`agents/frontend/`) - Build UI components
- **database-specialist** (`agents/backend/`) - Design schemas and queries
- **devops-engineer** (`agents/devops/`) - Plan infrastructure changes

## Example Workflow

\`\`\`text
User: "I want to add user authentication to the app"

Assistant (using brainstorming skill):
1. "What type of authentication do you want - email/password, OAuth, or SSO?"
2. [User answers]
3. "Do you need to support multiple authentication methods, or just one?"
4. [User answers]
5. "Should sessions be stateless (JWT) or stateful (server-side sessions)?"
6. [Iterative discussion continues...]

7. Present Design - Section 1 (Overview):
   "We'll implement JWT-based authentication with email/password login..."
   [Wait for approval]

8. Present Design - Section 2 (Architecture):
   "The system will have three main components: AuthService, TokenManager, UserRepository..."
   [Wait for approval]

[Continue for all sections...]

9. Validation: "Are you ready to proceed with implementation?"
10. [User approves]
11. Create design document using documentation-writer agent
12. Hand off to fastapi-backend-developer for implementation
\`\`\`

## Principles for Good Brainstorming

1. **One question at a time** - Don't overwhelm with multiple questions
2. **Listen first** - Understand before proposing solutions
3. **Start simple** - Don't over-engineer on first iteration
4. **Concrete over abstract** - Specific examples > generic descriptions
5. **Validate incrementally** - Get feedback on each design section
6. **Document the outcome** - Design docs create a record for future reference

## Anti-Patterns to Avoid

❌ **Don't jump to implementation** - Validate the design first
❌ **Don't assume requirements** - Ask clarifying questions
❌ **Don't present full design at once** - Break into sections
❌ **Don't skip trade-off discussion** - Make implications clear
❌ **Don't over-engineer** - YAGNI principle applies here too

## Success Criteria

A successful brainstorming session results in:

- ✅ User has clear mental model of the solution
- ✅ All sections of design are approved
- ✅ Trade-offs are understood and accepted
- ✅ Implementation steps are actionable and ordered
- ✅ Design is documented for future reference
- ✅ Appropriate implementation agent is ready to execute

## Notes

- This skill is about **collaboration**, not dictation
- The user is the domain expert - you're the technical facilitator
- Good design catches problems early, before they become bugs
- Time spent in design saves time in implementation and debugging
- Design documentation serves as requirements and audit trail
