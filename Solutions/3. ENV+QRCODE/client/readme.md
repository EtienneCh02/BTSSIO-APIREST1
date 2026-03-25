SELECT     dbo.Livre.Id_Livre, dbo.Livre.Titre, dbo.Livre.Résumé, dbo.Livre.Prix, dbo.Livre.ISBN, dbo.Livre.Stock, dbo.Editeur.Nom AS Editeur, STRING_AGG(dbo.Auteur.Nom + ' ' + dbo.Auteur.Prénom, ',') AS AUTEURS2
FROM        dbo.v_GetGenreLivre INNER JOIN
                  dbo.Livre ON dbo.v_GetGenreLivre.Id_Livre = dbo.Livre.Id_Livre INNER JOIN
                  dbo.Editeur ON dbo.Livre.Id_Editeur = dbo.Editeur.Id_Editeur INNER JOIN
                  dbo.Est_écrit_par ON dbo.Livre.Id_Livre = dbo.Est_écrit_par.Id_Livre INNER JOIN
                  dbo.Auteur ON dbo.Est_écrit_par.Id_Auteur = dbo.Auteur.Id_Auteur
GROUP BY dbo.Livre.Id_Livre, dbo.Livre.Titre, dbo.Livre.Résumé, dbo.Livre.Prix, dbo.Livre.ISBN, dbo.Livre.Stock, dbo.Editeur.Nom