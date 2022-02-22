# Fachbegriffe
- MQTT:
  - Nachrichtenprotokoll

- Broker
  - Zentrale
  - Software: Mosquitto

- publish:
  - senden der Information

- subscribe:
  - Änderungen der Topics als nachricht bekommen

- payload:
  - inhalt der Nachricht


- Topic
  - Hierachische Benennung der Variablen und Ordner
  - z.B. building/room/temp

- QoS (Quality of Service):
  - Qos1:
    - At most once
    - nachricht wird genau ein mal gesendet, es wird keine kontrolle des empfangs durchgeführt
  - QOS2:
    - At least once
    - nachricht wird gesendet bis eine Rückmeldung kommt (doppelungen können auftreten)
  - QoS3:
    - exactly once
    - nachricht wird gesendet mit empfangsbestätigung (Nachricht wird so gesendet, dass sic genau ein mal beim client ankommt)

- client connection status:
  - birth
    - 
  - death
    - 
  - last will and testament
    - 


