from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO():

    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from genre g  """

        cursor.execute(query)

        for row in cursor:
            results.append(Genre(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(idGenre):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a2.ArtistId , a2.Name 
                    from genre g , track t , album a , artist a2 
                    where g.GenreId = t.GenreId and t.AlbumId = a.AlbumId and a.ArtistId = a2.ArtistId 
                    and g.GenreId = %s  """

        cursor.execute(query, (idGenre,))

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(genreId, idMap):
        conn = DBConnect.get_connection()

        results = {}

        cursor = conn.cursor(dictionary=True)
        query = """select i.CustomerId as client , a.ArtistId as idArtist
                    from invoice i, invoiceline i2 , track t , album a 
                    where i.InvoiceId = i2.InvoiceId and i2.TrackId = t.TrackId and t.AlbumId = a.AlbumId 
                    and t.GenreId = %s
                    group by i.CustomerId , a.ArtistId """

        cursor.execute(query, (genreId,))

        for row in cursor:
            if row["idArtist"] in idMap.keys():
                if row["client"] not in results.keys():
                    results[row["client"]] = []
                results[row["client"]].append(row["idArtist"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllPopo(idGenre, idMap):
        conn = DBConnect.get_connection()

        results = {}

        cursor = conn.cursor(dictionary=True)
        query = """select a.ArtistId as idArtist, count(*) as pop
                    from invoice i, invoiceline i2 , track t , album a 
                    where i.InvoiceId = i2.InvoiceId and i2.TrackId = t.TrackId and t.AlbumId = a.AlbumId 
                    and t.GenreId = %s
                    group by a.ArtistId """

        cursor.execute(query, (idGenre,))

        for row in cursor:
            if row["idArtist"] in idMap.keys():
                results[row["idArtist"]] = row["pop"]

        cursor.close()
        conn.close()
        return results

