from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from os import environ as env
from urllib.parse import urlparse


load_dotenv()

# host=env.get('HOST')
# port=env.get('PORT')
# user=env.get('USER')
# password=env.get('PASSWORD')
# database=env.get('DATABASE')

CONNECTION_URL=env.get("CONNECTION_URL")
pgurl = urlparse(CONNECTION_URL)
print(pgurl)



class Database:
    """
    Initiate postgres database
    """
    def __init__(self):
        self.conn = None
        self.cursor = None


    @staticmethod
    def _compose_kv_and(separator=" AND ", kv_pairs=None):
        return sql.SQL(separator).join(
            sql.SQL("{} = {}").format(
                sql.Identifier(k), sql.Literal(v)
            ) for k, v in kv_pairs
        )



    def open(self, url=None):
        if not url:
            url = url = pgurl
        # print(url.hostname)
        # print(url.username)
        # print(url.password)
        # print(url.port)
        # print(url.path[1:])
        # print("==========================")
        self.conn = connect(host=url.hostname, port=url.port, user=url.username, password=url.password,database=url.path[1:])

        print("connection made")
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        print("connection cursor worked! ")

    def write(self, table: str, columns: list[str], data: list):
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING id").format(
            sql.Identifier(table),
            sql.SQL(",").join(map(sql.Identifier, columns)),        # columns are string
            sql.SQL(",").join(map(sql.Literal, data)),              # literal menas could be any data
        )
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchone().get('id')                     # returning usr id from query and through register function


    def get(self,  table: str, columns: list[str], where: dict = None, limit: int=None,
            or_where:dict = None):

        query = sql.SQL("SELECT {} FROM {}").format(
            # converting string columns in composed sql
            sql.SQL(',').join(map(sql.Identifier, columns)),
            sql.Identifier(table)
        )

        if where:
            query += sql.SQL(" WHERE {}").format(
                self._compose_kv_and(kv_pairs=where.items())
            )
        if where and or_where:
            query += sql.SQL(" OR ({})").format(
                self._compose_kv_and(kv_pairs=or_where.items())
                # sql.SQL(" AND ").join(
                #     sql.SQL("{} = {}").format(
                #         sql.Identifier(k),
                #         sql.Literal(v)
                #
                #     ) for k, v in or_where.items()
                # )
            )

        if limit:
            query += sql.SQL(" LIMIT {}").format(sql.Literal(limit))

        self.cursor.execute(query)
        return self.cursor.fetchall()





    def get_one(self, table: str, columns: list[str], where: dict = None):

        result = self.get(table, columns, where, 1)
        if len(result):
            return result[0]


    def update(self, table: str, columns: list[str], data: list, where: dict=None):
        where_clause = sql.SQL("")

        if where:
            where_clause = sql.SQL(" WHERE {}").format(
                self._compose_kv_and(kv_pairs=where.items())
                # sql.SQL(" AND ").join(
                #     sql.SQL("{} = {}").format(
                #         sql.Identifier(k), sql.Literal(v)) for k, v in where.items()
                #
                # )
            )

        query = sql.SQL(" UPDATE {} SET {} {}").format(
            sql.Identifier(table),
            self._compose_kv_and(separator=",", kv_pairs=zip(columns, data)),
            # sql.SQL(",").join(
            #     sql.SQL("{} = {}").format(
            #         sql.Identifier(x), sql.Literal(y)) for x, y in zip(columns, data)
            #
            # ),
            where_clause
        )
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.rowcount


    def delete(self, table: str, where: dict=None):
        where_clause = sql.SQL("")
        if where:
            where_clause = sql.SQL("WHERE {}").format(
                self._compose_kv_and(kv_pairs=where.items())
                # sql.SQL(" AND ").join(
                #     sql.SQL("{} = {}").format(
                #         sql.Identifier(k), sql.Literal(v)) for k, v in where.items()
                #     )
                )
        query= sql.SQL("DELETE FROM {} {}").format(
            sql.Identifier(table),
            where_clause
        )

        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.rowcount



    def get_containes(self, table:str, columns: list[str], search: str, limit: int= None):
        query = sql.SQL("SELECT {} FROM {} WHERE {}").format(
                sql.SQL(',').join(map(sql.Identifier, columns)),
            sql.Identifier(table),
            sql.SQL(" OR ").join(
                sql.SQL("{} LIKE {}").format(
                    sql.Identifier(k), sql.Literal(f"%{search}%")) for k in columns
                )
            )
        if limit:
            query += sql.SQL(" LIMIT {}").format(sql.Literal(limit))
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def close(self):
        self.cursor.close()
        self.conn.close()
        print("db closed!")



    """
    
        # def open(self):
        #     self.conn = connect(host=host, port=port, database=database, user=user, password=password)
        #     print("connected postgres db")
        #     # self.conn= connect(CONNECTION_URL)
        #     self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        #
        #     # by default a cursor return tuple, RealDictCursor will return dict
    """
