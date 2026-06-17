from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct g.GeneID , g.Essential, g.Chromosome
                        FROM genes g"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        dict = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                dict[(row["GeneID1"], row["GeneID2"])] = Interaction(**row)

            cursor.close()
            cnx.close()
        return dict

    @staticmethod
    def get_all_nodes(localization):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct g.GeneID , g.Essential, g.Chromosome
                    FROM classification c, genes g
                    where g.GeneID = c.GeneID 
                    and c.Localization = %s """
            cursor.execute(query, (localization,))

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllLocalizations():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct Localization 
                    from classification c 
                    order by Localization desc """
            cursor.execute(query)

            for row in cursor:
                result.append(row["Localization"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(localization):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select i.GeneID1 , i.GeneID2 
            from interactions i , classification c1, classification c2
            where i.GeneID1 = c1.GeneID 
            and i.GeneID2 = c2.GeneID 
            and c1.Localization = c2.Localization
            and c1.Localization = %s
            and i.GeneID1 != c2.GeneID"""

            cursor.execute(query, (localization, ))

            for row in cursor:
                result.append((row["GeneID1"], row["GeneID2"]))

            cursor.close()
            cnx.close()
        return result
