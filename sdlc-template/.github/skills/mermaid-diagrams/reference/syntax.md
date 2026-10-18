# Mermaid syntax cheat sheet

## flowchart

```mermaid
flowchart TD
  %% Create order: src/routes/orders.ts -> src/services/order.ts
  start([POST /orders]) --> auth[Auth middleware]
  auth --> valid{Token valid?}
  valid -- no --> e401[401 Unauthorized]
  valid -- yes --> svc[OrderService.create]
  svc --> db[(orders)]
  svc -. async .-> bus>order.created]
  bus -.-> mail[[Email provider]]
  svc --> done([201 Created])

  subgraph API
    auth
    valid
    svc
  end

  classDef err fill:#f8cecc,stroke:#b85450;
  class e401 err;
```

Shapes: `[rect]` `(rounded)` `([stadium])` `[[subroutine]]` `[(cylinder)]` `((circle))` `>flag]` `{diamond}` `{{hexagon}}` `[/parallelogram/]`.
Edges: `-->` solid arrow, `---` line, `-.->` dotted, `==>` thick, `--text-->` or `-- text -->` labeled, `-->|text|` labeled.
Direction: `TD`/`TB`, `LR`, `RL`, `BT`. Subgraphs can have their own `direction LR`.
Click: `click svc "https://github.com/org/repo/blob/main/src/services/order.ts"`.

## sequenceDiagram

```mermaid
sequenceDiagram
  autonumber
  actor U as User
  participant API
  participant S as OrderService
  participant DB as Postgres
  participant K as Kafka

  U->>API: POST /orders
  API->>API: validate JWT
  alt invalid token
    API-->>U: 401
  else valid
    API->>S: create(order)
    S->>DB: INSERT orders
    DB-->>S: id
    S-)K: order.created
    S-->>API: order
    API-->>U: 201 Created
  end
  Note over S,K: async, at-least-once
```

Arrows: `->>` sync call, `-->>` return, `-)` async (no wait), `-x` lost. Blocks: `alt/else/end`, `opt`, `loop`, `par/and`, `critical`, `break`, `rect rgb(240,240,240)`. `activate X` / `deactivate X` or `+`/`-` suffix on arrows.

## stateDiagram-v2

```mermaid
stateDiagram-v2
  [*] --> Pending
  Pending --> Paid: payment.succeeded
  Pending --> Cancelled: timeout 15m
  Paid --> Shipped: ship()
  Shipped --> Delivered
  Delivered --> [*]
  Cancelled --> [*]
  state Paid {
    [*] --> Packing
    Packing --> Ready
  }
```

## erDiagram

```mermaid
erDiagram
  USER ||--o{ ORDER : places
  ORDER ||--|{ ORDER_ITEM : contains
  PRODUCT ||--o{ ORDER_ITEM : "appears in"
  USER {
    uuid id PK
    string email UK
    timestamp created_at
  }
  ORDER {
    uuid id PK
    uuid user_id FK
    string status
  }
```

Cardinality: `|o` zero or one, `||` exactly one, `}o` zero or more, `}|` one or more. Left symbol = left entity's side. `--` identifying, `..` non-identifying.

## classDiagram

```mermaid
classDiagram
  class OrderService {
    -OrderRepo repo
    +create(dto) Order
    +cancel(id) void
  }
  class OrderRepo { <<interface>> }
  OrderService --> OrderRepo : uses
  PgOrderRepo ..|> OrderRepo : implements
  Order "1" *-- "many" OrderItem
```

Relations: `<|--` inheritance, `*--` composition, `o--` aggregation, `-->` association, `..>` dependency, `..|>` realization.

## C4

```mermaid
C4Context
  title System context: Shop
  Person(customer, "Customer")
  System(shop, "Shop", "Web shop")
  System_Ext(psp, "Payment provider")
  Rel(customer, shop, "buys via", "HTTPS")
  Rel(shop, psp, "charges", "REST")
```

Also `C4Container`, `C4Component`, `C4Deployment`; `Container(id, name, tech, desc)`, `ContainerDb`, `Container_Boundary(id, name) { ... }`.

## gantt

```mermaid
gantt
  title Release 2.0
  dateFormat YYYY-MM-DD
  section Backend
    API            :a1, 2026-11-01, 10d
    Migration      :after a1, 3d
  section Frontend
    UI             :2026-11-05, 12d
  milestone Launch :m1, 2026-11-20, 0d
```

## gitGraph

```mermaid
gitGraph
  commit
  branch feature/orders
  checkout feature/orders
  commit
  commit
  checkout main
  merge feature/orders tag: "v2.0"
```

## journey, mindmap, timeline

```mermaid
journey
  title Checkout
  section Cart
    Add item: 5: Customer
    Apply coupon: 3: Customer
  section Pay
    Enter card: 2: Customer
```

```mermaid
mindmap
  root((Platform))
    Backend
      API
      Workers
    Frontend
```

```mermaid
timeline
  title Incident 2026-10-18
  09:02 : Alert fired
  09:10 : Rollback started
  09:15 : Recovered
```

## Common parse errors

- Unquoted `(`, `)`, `|`, `:` in a label → wrap in `"..."`.
- A node named `end` → rename (`finish`).
- `sequenceDiagram` message text containing `;` → remove or quote.
- Missing `-v2` on `stateDiagram` when using composite states.
- `classDiagram` method with generics: write `List~Order~` for `List<Order>`.
- Blank line inside a `subgraph` block is fine; a blank line between the ```` ```mermaid ```` fence and the header is not.
- Theme/config: a front-matter block is allowed at the top:
  ```
  ---
  config:
    theme: neutral
    flowchart:
      curve: basis
  ---
  ```
