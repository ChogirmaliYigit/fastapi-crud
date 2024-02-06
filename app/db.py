import sqlite3


class Database:
    """
    The database class with sqlite3 engine
    """
    def __init__(self, path="main.db"):
        self.path = path
        self.connection = sqlite3.connect(self.path)

    def execute(
            self,
            sql: str,
            parameters: tuple = (),
            fetchone: bool = False,
            fetchall: bool = False,
            commit: bool = False,
    ) -> list | None:
        cursor = self.connection.cursor()
        cursor.execute(sql, parameters)

        if commit:
            self.connection.commit()

        data = None
        if fetchone and fetchall:
            raise ValueError("The `fetchone` or the `fetchall` should be either True.")
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def create_categories_table(self) -> None:
        self.execute("""
            CREATE TABLE IF NOT EXISTS Categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(400) NOT NULL
            );
        """)

    def create_tasks_table(self) -> None:
        self.execute("""
            CREATE TABLE IF NOT EXISTS Tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(400) NOT NULL,
                description TEXT NOT NULL,
                status VARCHAR(50) DEFAULT 'todo',
                priority VARCHAR(50) DEFAULT 'medium',
                category_id INTEGER,

                FOREIGN KEY (category_id) REFERENCES Categories(id)
            );
        """)

    def add_a_category(self, title: str) -> None:
        self.execute(
            """
            INSERT INTO Categories(title) VALUES(?)
            """,
            (title, ),
            commit=True
        )

    def get_all_categories(self) -> list | None:
        return self.execute("SELECT * FROM Categories", fetchall=True)

    def get_a_category(self, category_id: int) -> list | None:
        return self.execute(
            "SELECT * FROM Categories WHERE id = ?",
            (category_id, ),
            fetchone=True
        )

    def update_a_category(self, category_id: int, title: str) -> None:
        self.execute(
            "UPDATE Categories SET title = ? WHERE id = ?",
            (title, category_id,),
            commit=True
        )

    def delete_a_category(self, category_id: int) -> None:
        self.execute(
            "DELETE FROM Categories WHERE id = ?",
            (category_id, ),
            commit=True
        )

    def add_a_task(
            self,
            title: str,
            description: str,
            category_id: int,
            status: str = "todo",
            priority: str = "medium",
    ) -> None:
        self.execute(
            """
            INSERT INTO Tasks(title, description, category_id, status, priority) VALUES(?, ?, ?, ?, ?)
            """,
            (title, description, category_id, status, priority, ),
            commit=True
        )

    def get_all_tasks(self, category_id: int = None) -> list | None:
        sql = "SELECT * FROM Tasks"
        parameters = ()
        if category_id:
            sql += " WHERE category_id = ?"
            parameters = (category_id, )
        return self.execute(sql, parameters, fetchall=True)

    def get_a_task(self, task_id: int):
        return self.execute(
            "SELECT * FROM Tasks WHERE id = ?",
            (task_id, ),
            fetchone=True
        )

    def update_a_task(
            self,
            task_id: int,
            title: str = None,
            description: str = None,
            category_id: int = None,
            status: str = None,
            priority: str = None,
    ):
        sql = "UPDATE Tasks SET "
        parameters = []
        if title:
            sql += "title = ? AND "
            parameters.append(title)
        if description:
            sql += "description = ? AND "
            parameters.append(description)
        if status:
            sql += "status = ? AND "
            parameters.append(status)
        if priority:
            sql += "priority = ? AND "
            parameters.append(priority)
        if category_id:
            sql += "category_id = ? AND "
            parameters.append(category_id)
        sql = sql.strip()
        sql = sql[:(len(sql) - 3)]
        sql += "WHERE id = ?"
        parameters.append(task_id)
        self.execute(sql, tuple(parameters), commit=True)

    def delete_a_task(self, task_id: int):
        self.execute(
            "DELETE FROM Tasks WHERE id = ?",
            (task_id, ),
            commit=True
        )
