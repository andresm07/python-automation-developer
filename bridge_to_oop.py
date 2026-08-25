import sqlite3

#! Connects to database (creates app.db file if missing)
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

#! Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
""")

#! Insert Data using ? placeholders for safety
cursor.execute(
    "INSERT INTO users (name, email) VALUES (?, ?)",
    ("Alice", "alice@example.com"),
)

#! Read Data using ? placeholders for safety
cursor.execute("SELECT id, name, email FROM users WHERE name = ?", ("Alice",))

# ? Retrieve one row from the cursor's SELECT query
alice = cursor.fetchone()

print(f"Found User: {alice}")

#! Bulk Insertions
users_batch = [
    ("Bob", "bob@example.com"),
    ("Charlie", "charlie@example.com"),
    ("Dana", "dana@example.com"),
    ("Evan", "evan@example.com"),
    ("Fred", "fred@example.com"),
]

cursor.executemany(
    "INSERT INTO users (name, email) VALUES (?, ?)", users_batch
)

#! Save Changes
conn.commit()

#! Close resources
cursor.close()
conn.close()


# * --------------------------- SQLALCHEMY ORM ---------------------------

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    func,
    select,
    text,
)

#! Create Engine & Metadata Container
engine = create_engine("sqlite:///core.db")

# ? Within SQLAlchemy, Metadata refers to the structural description of your database tables, columns, constraints, relationships, rather than the actual data stored inside
# ? Refers to "data about data"

"""
Metadata: column names like id, name, email with their data types, rules, relationships, etc.
Data: (1, "Alice", "alice@example.com")
"""

# ? MetaData() in SQLAlchemy, this object acts as a central registry that holds all information about your database tables
metadata = MetaData()

#! Create Table
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("email", String(50), unique=True, nullable=False),
    Column("phone", String(50), unique=True, nullable=False),
)

#! Create Table
clients = Table(
    "clients",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("email", String(50), unique=True, nullable=False),
    Column("phone", String(50), unique=True, nullable=False),
)

#! Create Table
roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
)

# ? Because MetaData track every table registered, it can generate and execute the raw CREATE TABLE DDL statements for the entire database creation in one call
metadata.create_all(engine)

#! --- BASIC CRUD OPERATIONS ---

with engine.connect() as conn:
    #! CREATE
    insert_user = users.insert().values(
        name="Bob", email="bob@example.com", phone="+1 888 888 9999"
    )  #! Equivalent to INSERT INTO users ...
    result = conn.execute(insert_user)
    inserted_user_id = result.inserted_primary_key[0]

    insert_role = roles.insert().values(name="Admin", user_id=inserted_user_id)
    conn.execute(insert_role)
    conn.commit()

    #! READ
    query = (
        select(
            users.c.name, roles.c.name
        )  #! SELECT users.name, roles.name FROM users
        .select_from(
            users.join(roles)
        )  #! JOIN roles ON users.role_id = roles.role_id
        .where(users.c.name == "Alice")  #! WHERE users.name = 'Alice';
    )

    rows = conn.execute(query).fetchall()
    for row in rows:
        #! Row is a tuple containing the results from the SELECT statement
        #! If I selected users.name and roles.name, I would get a tuple back in the shape of (users.name, roles.name)
        print(f"User {row[0]} has role {row[1]}")

    #! UPDATE
    query = (
        users.update()  #! UPDATE users
        .where(users.c.id == 1)  #! SET email = 'alice.updated@example.com'
        .values(email="alice.updated@example.com")  #! WHERE users.id = 1;
    )

    conn.execute(query)
    conn.commit()

    #! DELETE
    query = roles.delete().where(
        roles.c.id == 1
    )  #! DELETE FROM roles WHERE roles.id = 1;
    conn.execute(query)
    conn.commit()

    #! RAW SQL DDL
    query = text("SELECT * FROM users WHERE users.id = :user_id")
    results = conn.execute(query, {"user_id": 1}).fetchall()

    print(results)

#! --- COMPLEX JOINS, AGGREGATIONS, GROUP BY, LIMITS

engine = create_engine("sqlite:///store.db")
metadata = MetaData()

customers = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey("customers.id")),
    Column("total", Float),
)

metadata.create_all(engine)

with engine.connect() as conn:
    conn.execute(customers.insert(), [{"name": "Alice"}, {"name": "Bob"}])

    conn.execute(
        orders.insert(),
        [
            {"customer_id": 1, "total": 150.00},
            {"customer_id": 2, "total": 249.00},
            {"customer_id": 2, "total": 49.99},
        ],
    )

    conn.commit()

    #! SELECT name, COUNT(orders.id), SUM(total) JOIN GROUP BY
    query = (
        select(
            customers.c.name,
            func.count(orders.c.id).label("order_count"),
            func.sum(orders.c.total).label("total_spent"),
        )
        .select_from(customers.join(orders))
        .group_by(customers.c.id)
        .having(func.sum(orders.c.total) > 100)
    )

    results = conn.execute(query).fetchall()
    for row in results:
        print(row)

#! --- TRANSACTION COMMITS & ROLLBACKS ---

engine = create_engine("sqlite:///bank.db")
metadata = MetaData()

accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("holder", String),
    Column("balance", Float),
)
metadata.create_all(engine)

#! If we need a transaction, instead of engine.connect(), we will use engine.begin()
with engine.connect() as conn:
    conn.execute(
        accounts.insert(),
        [
            {"holder": "Alice", "balance": 500.00},
            {"holder": "Bob", "balance": 600.00},
        ],
    )

    conn.commit()

#! Automatic Commit/Rollback using engine.begin()
try:
    with engine.begin() as conn:
        conn.execute(
            accounts.update()
            .where(accounts.c.holder == "Alice")
            .values(balance=accounts.c.balance - 100.00)
        )

        result = conn.execute(
            accounts.update()
            .where(accounts.c.holder == "Charlie")
            .values(balance=accounts.c.balance + 100.00)
        )

        # * If no error occurs, COMMIT happens automatically, if not ROLLBACK kicks in
        # ? For demo purposes, since an UPDATE with 0 rows affected is still a valid DB transaction, we force the exception, however
        # ? if a real DB error occurs, ROLLBACK does kick in automatically
        if result.rowcount == 0:
            raise ValueError(
                "Account 'Charlie' not found. Aborting transaction."
            )
except Exception as e:
    print(f"Transaction failed and rolled back automatically {e}")

with engine.connect() as conn:
    rows = conn.execute(select(accounts)).fetchall()
    for row in rows:
        print(row)

#! --- SUBQUERIES, CTEs (Common Table Expression), FILTERING

engine = create_engine("sqlite:///company.db")
metadata = MetaData()

employees = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("department", String),
    Column("salary", Integer),
)
metadata.create_all(engine)

with engine.begin() as conn:
    conn.execute(
        employees.insert(),
        [
            {"name": "Sarah", "department": "Engineering", "salary": 120000},
            {"name": "Alex", "department": "Engineering", "salary": 95000},
            {"name": "Maria", "department": "Marketing", "salary": 80000},
            {"name": "David", "department": "Marketing", "salary": 85000},
        ],
    )

"""
WITH TotalSales AS (
    SELECT customer_id, SUM(order_total) AS grand_total
    FROM orders
    GROUP BY customer_id
),

--- UPDATE STATEMENT HERE on orders

VIPCustomer AS (
    SELECT customer_id
    FROM TotalSales
    WHERE grand_total > 10000
)
SELECT c.customer_name, ts.grand_total
FROM VIPCustomer v
JOIN TotalSales ts on v.customer_id = ts.customer_id
JOIN customers c on V.customer_id = c.id;
"""

"""

Point in Time 1: CTE IS CREATED: The db parses the query structure and prepares execution plan, no rows retrieved yet or stored in CTE
Point in Time 2: TABLE USED FOR CTE CREATION IS UPDATED
Point in Time 3: READ FROM CTE: The CTE is executed as part of other outer SELECT query. It will read current information from the table at time of execution

"""

with engine.connect() as conn:
    avg_salary_cte = (
        select(
            employees.c.department.label("department"),
            func.avg(employees.c.salary).label("avg_dept_salary"),
        )
        .group_by(employees.c.department)
        .cte("dept_averages")  #! WITH dept_averages AS
    )

    #! SELECT employees with above average salary using CTEs

    query = (
        select(
            employees.c.name,
            employees.c.salary,
            avg_salary_cte.c.avg_dept_salary,
        )
        .select_from(
            employees.join(
                avg_salary_cte,
                employees.c.department == avg_salary_cte.c.department,
            )
        )
        .where(employees.c.salary > avg_salary_cte.c.avg_dept_salary)
    )

    results = conn.execute(query).fetchall()
    for row in results:
        print(row)
