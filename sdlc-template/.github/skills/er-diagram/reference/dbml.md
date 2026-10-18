# DBML quick reference

DBML opens in https://dbdiagram.io (paste) and dbdocs; `npm i -g @dbml/cli` gives `sql2dbml` / `dbml2sql`.

```dbml
Project shop {
  database_type: 'PostgreSQL'
  Note: 'Derived from prisma/schema.prisma on 2026-10-18'
}

Enum order_status {
  pending
  paid
  shipped
  cancelled
}

Table users {
  id uuid [pk, default: `gen_random_uuid()`]
  email citext [unique, not null]
  created_at timestamptz [not null, default: `now()`]
}

Table orders {
  id uuid [pk]
  user_id uuid [not null, ref: > users.id]      // many orders -> one user
  status order_status [not null, default: 'pending']
  total numeric(12,2) [not null]
  created_at timestamptz [not null]

  Indexes {
    (user_id, created_at)
  }
}

Table order_items {
  order_id uuid [ref: > orders.id]
  product_id uuid [ref: > products.id]
  qty int [not null]

  Indexes {
    (order_id, product_id) [pk]
  }
}

Table products {
  id uuid [pk]
  sku text [unique]
  name text
}

TableGroup commerce {
  orders
  order_items
  products
}
```

Relations: `>` many-to-one, `<` one-to-many, `-` one-to-one, `<>` many-to-many (DBML ≥ 3). Standalone form: `Ref: orders.user_id > users.id [delete: restrict]`.

Convert an existing database: `pg_dump --schema-only db > schema.sql && sql2dbml schema.sql --postgres -o schema.dbml`.
