# BarcodeDataTranfer_Windows_Edition
Dieses Repository soll als Beispiel gelten, für einen möglichen Ansatz einen Barcode in ein Windows-Anwendungsfenster zu integrieren

Die Anwendung wurde mithilfe der PyCharm - IDE unter Python 3.10 entwickelt.
Weitere Informationen und Verlinkungen befinden sich im Modul in den Kommentaren zu den jeweiligen Abschnitten

##Installation und Verwendung
Um die Anwendung zu installieren reicht es, wenn man das betreffende Projekt in einer IDE öffnet (Diese Anwendung hier wurde unter PyCharm implementiert und getestet - für die Funktion auf anderen IDE's kann keine Garantie übernommen werden)

Die Anwendung wird  gestartet, indem man sie in der bevorzugten IDE lädt oder Ausführt und auf das Fenster, welches man "overlayed" haben möchte, draufklickt. Es ist noch ein existenter Bug, dass es nicht sofort angezeigt wird.Im Zweifelsfall ist es besser ein paar mal auf das ausgewählte Fenster zu klicken

##Aktuelle Features der Anwendung:
- Marker, welcher im oberen rechten Bereich der Titlebar angezeigt wird 
- Dieser ändert sich vom Inhalt dynamisch, abhängig von dem aktuell ausgewählten Fenster
- Marker bewegt sich dynamisch mit und reagiert auf verschiedene Fenstergrößen
- Im Systemtray wird ein Icon eingeblendet, mit welchem das Konfigurationsmenü aufgerufen werden kann
- Der Marker kann mit einem Kontextmenü - oder den entsprechend angezeigten Tastenkombinationen manipuliert werden, das Kontextmenü kann per rechtsklick auf den Marker aufgerufen werden
- Im Konfigurationsmenü lassen sich die Standardgröße des Markers, die Hotkeykombinationen und auch die Passwörter einstellen
- Die Passwörter finden sich in der Datei "hhtpd.password"
- Die aktuell verwendeten Tastenkombinationen finden sich in der "ConfigFile.ini"

## Versionen
master-Branch: Die aktuellste Variante des Prototypen
Effizienteres Backend - Branch:

