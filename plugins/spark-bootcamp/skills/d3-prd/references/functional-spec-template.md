# Functional Spec: <product name>

*The layer the build reads from. Concrete. Every field named, every action named, every state named. If it is not written here, the build will guess, and it will guess wrong.*

## Screens / steps

List each screen (software), each render or page (hardware), or each step of the sample deliverable and intake (services).

### Screen/Step 1: <name>
- **Purpose:** <one line: what the prospect does here>
- **Fields:** <name each input, its type, and whether it is required>
- **Actions:** <name each button or link, and what happens on click>
- **States:**
  - Empty: <what shows before any input>
  - Loading: <what shows while working>
  - Error: <the exact message on failure>
  - Done: <what confirms success to the prospect>

### Screen/Step 2: <name>
- **Purpose:** <...>
- **Fields:** <...>
- **Actions:** <...>
- **States:** empty / loading / error / done

## Data (software path)

The one table behind the slice.

| Field | Type | Notes |
| --- | --- | --- |
| id | uuid | primary key |
| created_at | timestamp | default now |
| <field> | <type> | <what it holds> |

## Intent capture (hardware path)

- What is captured: <deposit amount, or card hold>
- Where it lands: <waitlist table / payment provider>
- Confirmation shown: <exact message>

## Intake flow (services path)

- Package presented: <fixed scope, fixed price>
- Booking mechanism: <calendar link / form>
- What the prospect receives: <sample deliverable link, confirmation>

## Out of scope

Repeat the non-goals from the PRD here so the build never wanders into them.

- Not building: <thing>
- Not building: <thing>
