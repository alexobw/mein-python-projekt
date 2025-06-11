Migriere das folgende WildFly-Projekt vollständig zu Quarkus. Das bedeutet, dass alle Aspekte der aktuellen WildFly-Implementierung, einschließlich Konfigurationen, Abhängigkeiten und Jakarta EE (ehemals Java EE) APIs, so umgewandelt werden müssen, dass sie nativ in einer Quarkus-Umgebung funktionieren. Der Migrationsprozess soll durchdacht und schrittweise erfolgen. Dabei ist es wichtig, die funktionalen Anforderungen zu erhalten und gleichzeitig typische Quarkus-Muster und -Vorgaben zu berücksichtigen.
  
Bitte denke dabei strukturiert über die folgenden Aspekte nach und nutze sie als Orientierungspunkte für deine Umsetzung.
  
Denkansatzt: 
- Analysiere, welche Jakarta EE-Komponenten in der Anwendung verwendet werden und ob diese in Quarkus direkt unterstützt werden.
- Achte darauf, dass alle `javax.*`-Importe durch `jakarta.*` ersetzt werden müssen, da Quarkus auf Jakarta EE 10 basiert.
- Prüfe, ob RESTEasy Classic verwendet wird und ob eine Migration zu Quarkus REST notwendig ist.
- Stelle sicher, dass benutzerdefinierte Provider und Exception Mapper mit Quarkus REST kompatibel sind.
- Untersuche die aktuelle Sicherheitsarchitektur und entscheide, ob sie mit Quarkus Security nachgebildet werden kann.
- Überführe sicherheitsrelevante Einstellungen aus XML in das Quarkus-Konfigurationsformat (`application.properties`).
- Ermittle, ob EJB-Remote-Aufrufe bestehen, und bewerte deren Weiterverwendung oder Ersatz.
- Erwäge, ob EJB-Remote-Kommunikation durch RESTful Services ersetzt werden kann.
- Überdenke die bisherige Transaktionslogik und prüfe, ob eine Umstellung auf CDI-gestützte Transaktionen erforderlich ist.
- Vergewissere dich, dass die bestehende Benutzer- und Rollenlogik mit Quarkus-Sicherheitsmechanismen kompatibel ist.
- Plane die Überführung der Konfiguration von `standalone.xml` zu `application.properties`. 
