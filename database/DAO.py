from database.DB_connect import DBConnect
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_chromosoma():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct Chromosome 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Chromosome"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(cMin,cMax):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *
                        FROM genes
                        where Chromosome >= %s
                        and Chromosome <= %s"""
            cursor.execute(query, (cMin,cMax,))

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllArchi(min, max, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct g1.GeneID as g1, g1.Function as f1, g2.GeneID as g2, g2.Function as f2, i.Expression_Corr as peso
                        FROM classification c1, classification c2, interactions i, genes g1, genes g2
                        where c1.GeneID =g1.GeneID
                        and c2.GeneID = g2.GeneID 
                        and c1.GeneID != c2.GeneID 
                        and c1.Localization = c2.Localization
                        and g1.Chromosome <= g2.Chromosome
                        and ((c1.GeneID = i.GeneID1 and c2.GeneID = i.GeneID2) or (c1.GeneID = i.GeneID2 and c2.GeneID = i.GeneID1))
                        and g1.Chromosome >= %s
                        and g1.Chromosome <= %s 
                        and g2.Chromosome >= %s
                        and g2.Chromosome <= %s """

            cursor.execute(query, (min, max, min, max))

            for row in cursor:
                result.append((idMap[(row["g1"], row["f1"])], idMap[(row["g2"], row["f2"])], row["peso"]))

            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_all_localizations():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT c.Localization  
                        FROM classification c 
                        ORDER BY c.Localization  ASC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Localization"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_localization_gene(g: Gene, localization_map: dict):
        cnx = DBConnect.get_connection()
        result = None
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT c.Localization  
                            FROM classification c 
                            WHERE c.GeneID = %s """
            cursor.execute(query, (g.GeneID,))

            rows = cursor.fetchall()
            localization_map[g.GeneID] = rows[0]["Localization"]
            result = rows[0]["Localization"]

            cursor.close()
            cnx.close()
        return result