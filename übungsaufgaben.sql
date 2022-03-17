-- Aufgabe 1:

-- Arbeiten Sie die Beispiele für den Select-Befehl (Select-Basic) durch.

-- Aufgabe 2:

-- Arbeiten Sie die Beispiele für den Insert-Befehl (Insert-Values) durch. Ergänzen Sie die Tabelle mit den folgenden Daten:

-- - 2016 Rio de Janeiro
-- - 2021 Tokio
-- - 2024 Paris
-- - 2028 Los Angeles
-- - 2032 Brisbane


-- SELECT Befehle

Select * from Tabelle   --Alle datensätze aller Spalten
Select Temperatur, Zeitstempel from Tabelle     --Nur die Daten der Temperatur und des Zeitstempels aller Datensätze
Select * from Tabelle where Temperatur > 23     -- Nur Datensätze, bei denen die Temperatur > 23 ist

-- Insert Befehle:
-- in die Tabelle | ID | Jahr | Ort |
-- kurzform:
Insert into Tabelle
(2016, "Rio de Janeiro"),
(2021, "Tokio"),
(2024, "Paris"),
(2028, "Los Angeles"),
(2032, "Brisbane")

-- Langform:
Insert into Tabelle
("Jahr", "Ort")
Values
(2016, "Rio de Janeiro"),
(2021, "Tokio"),
(2024, "Paris"),
(2028, "Los Angeles"),
(2032, "Brisbane")


-- Beispiel für den Raumsensor:

insert into messwerte_raumluft
("TEMPERATUR", "LUFTFEUCHTE", "HELLIGKEIT")
Values
($temperature, $humidity, $luminance)