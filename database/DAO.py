from Arco import Arco
from Retailer import Retailer
from database.DB_connect import DBConnect


class DAO():
    @staticmethod
    def getNazioni():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary = True)
        result = []
        query = """SELECT DISTINCT Country as nazione
FROM go_retailers """
        cursor.execute(query)
        # rows = cursor.fetchall()
        # for row in rows:
        #     print(row)
        for row in cursor:
            result.append(row["nazione"])
            #result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """Select distinct YEAR(Date) as year
    from go_daily_sales gds """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(country, idRetailers):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """SELECT DISTINCT Retailer_code as rt_code, Retailer_name as rt_name, Type as rt_type, Country as rt_country
FROM go_retailers gr 
WHERE gr.Country = %s"""

        cursor.execute(query,(country,))

        for row in cursor:
            result.append(idRetailers[row["rt_code"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRetailers():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """SELECT *
        FROM go_retailers gr"""
        cursor.execute(query)
        for row in cursor:
            result.append(Retailer(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(country, idRetailers, year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """SELECT t.rt_cod as cod1, t1.rt_cod as cod2, count(DISTINCT t.prod_Cod) as peso
FROM(SELECT gds.Retailer_code as rt_cod, gds.Product_number as prod_Cod, gds.`Date`as date, gr.Country as nazione
FROM go_daily_sales gds , go_retailers gr 
WHERE YEAR(gds.`Date`) = %s and gr.Country = %s and gds.Retailer_code = gr.Retailer_code
) AS t, (SELECT gds.Retailer_code as rt_cod, gds.Product_number as prod_Cod, gds.`Date`as date, gr.Country as nazione
FROM go_daily_sales gds , go_retailers gr 
WHERE YEAR(gds.`Date`) = %s and gr.Country = %s and gds.Retailer_code = gr.Retailer_code) as t1
WHERE t.rt_cod < t1.rt_cod and t.prod_Cod = t1.prod_Cod 
group by t.rt_cod, t1.rt_cod
order by peso desc"""

        cursor.execute(query, (year,country,year, country))

        for row in cursor:
            result.append(Arco(idRetailers[row["cod1"]],
                              idRetailers[row["cod2"]],
                              row['peso']))
        # for row in cursor:
        #     result.append(Arco(idproducts[row['p1']],
        #                   idproducts[row['p2']],
        #                   row['peso']))

        cursor.close()
        conn.close()
        print(result)
        return result



