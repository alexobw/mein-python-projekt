# Rolle
Du bist ein Senior Java Enterprise Architekt mit mehr als 10 Jahren Erfahrung in der automatisierten Migration von WildFly-basierten Anwendungen nach Quarkus. Du kennst alle spezifischen Transformationsregeln (EJBs -> CDI Beans, persistence.xml -> application.properties, WildFly Subsystems -> Quarkus Extensions) und erstellst vollstaendig funktionierenden Code mit detaillierten Migrationsanleitungen. Dein Ansatz ist systematisch: Analyse der WildFly-Abhaengigkeiten, praezise 1:1 Transformation zu Quarkus-Aequivalenten und Identifikation von Kompatibilitaetsproblemen.

# Build-Vorgaben
- Java-Version: 21.0.7 (Ubuntu OpenJDK)
- Maven-Version: 3.8.7
- Zielplattform: Quarkus 3.11.1 (neueste stabile Version)
- Build-Typ: JVM (kein native-image, kein GraalVM)
- Betriebssystem: Linux 6.11.0-26-generic (amd64)
- Alle Projekte müssen lokal ausführbar sein mit:
  - `mvn quarkus:dev` (Entwicklung)
- Es dürfen \textbf{keine Tests erzeugt oder migriert} werden
- Verwendete API-Extension: `quarkus-resteasy-reactive`
- Konfigurationsformat: `application.properties`
- Keine Docker-, Helm-, Kubernetes- oder OpenShift-Artefakte
- Keine automatischen Sicherheits- oder Datenbankkonfigurationen erzeugen, sofern nicht explizit gefordert

# Aufgabenbeschreibung
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
  
# Zu migrierende Aufgabe
Project Path: ejb-remote-client

Source Tree:

```txt
ejb-remote-client
├── pom.xml
└── src
    ├── main
    │   ├── java
    │   │   ├── main
    │   │   │   └── java
    │   │   │       └── org
    │   │   │           └── example
    │   │   └── org
    │   │       ├── example
    │   │       │   ├── CalculatorResource.java
    │   │       │   ├── CounterResource.java
    │   │       │   ├── EJBLookupHelper.java
    │   │       │   └── JaxRsActivator.java
    │   │       └── jboss
    │   │           └── as
    │   │               └── quickstarts
    │   │                   └── ejb
    │   │                       └── remote
    │   │                           ├── stateful
    │   │                           │   └── RemoteCounter.java
    │   │                           └── stateless
    │   │                               └── RemoteCalculator.java
    │   └── resources
    │       └── META-INF
    │           └── beans.xml
    └── webapp
        └── WEB-INF
            └── web.xml

```

`ejb-remote-client/pom.xml`:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.example</groupId>
    <artifactId>ejb-remote-client</artifactId>
    <version>1.0.0</version>
    <packaging>war</packaging>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- REST API -->
        <dependency>
            <groupId>jakarta.ws.rs</groupId>
            <artifactId>jakarta.ws.rs-api</artifactId>
            <version>3.1.0</version>
            <scope>provided</scope>
        </dependency>



        <!-- EJB Client (für Remote-Call) -->
        <dependency>
            <groupId>org.jboss</groupId>
            <artifactId>jboss-ejb-client</artifactId>
            <version>4.0.42.Final</version>
        </dependency>
    </dependencies>

    <build>
        <finalName>ejb-remote-client</finalName>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-war-plugin</artifactId>
                <version>3.4.0</version>
                <configuration>
                    <failOnMissingWebXml>false</failOnMissingWebXml>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>

```

`ejb-remote-client/src/main/java/org/example/CalculatorResource.java`:

```java
package main.java.org.example;

import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import org.jboss.as.quickstarts.ejb.remote.stateless.RemoteCalculator;
import java.util.Map;

@Path("/calculator")
@Produces(MediaType.APPLICATION_JSON)
public class CalculatorResource {

    @GET
    @Path("/add")
    public Response add(@QueryParam("a") int a, @QueryParam("b") int b) {
        try {
            RemoteCalculator calc = EJBLookupHelper.lookupCalculator();
            int result = calc.add(a, b);
            return Response.ok(Map.of("operation", "add", "a", a, "b", b, "result", result)).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }

    @GET
    @Path("/subtract")
    public Response subtract(@QueryParam("a") int a, @QueryParam("b") int b) {
        try {
            RemoteCalculator calc = EJBLookupHelper.lookupCalculator();
            int result = calc.subtract(a, b);
            return Response.ok(Map.of("operation", "subtract", "a", a, "b", b, "result", result)).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }
}

```

`ejb-remote-client/src/main/java/org/example/CounterResource.java`:

```java
package main.java.org.example;

import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import org.jboss.as.quickstarts.ejb.remote.stateful.RemoteCounter;
import java.util.Map;

@Path("/counter")
@Produces(MediaType.APPLICATION_JSON)
public class CounterResource {

    private static final RemoteCounter counter;

    static {
        try {
            counter = EJBLookupHelper.lookupCounter();
        } catch (Exception e) {
            throw new RuntimeException("Unable to initialize Counter EJB", e);
        }
    }

    @POST
    @Path("/increment")
    public Response increment() {
        try {
            counter.increment();
            return Response.ok(Map.of("action", "increment", "value", counter.getCount())).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }

    @POST
    @Path("/decrement")
    public Response decrement() {
        try {
            counter.decrement();
            return Response.ok(Map.of("action", "decrement", "value", counter.getCount())).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }

    @GET
    @Path("/value")
    public Response value() {
        try {
            int value = counter.getCount();
            return Response.ok(Map.of("counter", value)).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }
}


```

`ejb-remote-client/src/main/java/org/example/EJBLookupHelper.java`:

```java
package main.java.org.example;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import java.util.Properties;

import org.jboss.as.quickstarts.ejb.remote.stateless.RemoteCalculator;
import org.jboss.as.quickstarts.ejb.remote.stateful.RemoteCounter;

public class EJBLookupHelper {

    public static RemoteCalculator lookupCalculator() throws NamingException {
        Context context = createContext();
        return (RemoteCalculator) context.lookup("ejb:/ejb-remote/CalculatorBean!org.jboss.as.quickstarts.ejb.remote.stateless.RemoteCalculator");
    }

    public static RemoteCounter lookupCounter() throws NamingException {
        Context context = createContext();
        return (RemoteCounter) context.lookup("ejb:/ejb-remote/CounterBean!org.jboss.as.quickstarts.ejb.remote.stateful.RemoteCounter?stateful");
    }

    private static Context createContext() throws NamingException {
        Properties props = new Properties();
        props.put(Context.INITIAL_CONTEXT_FACTORY, "org.wildfly.naming.client.WildFlyInitialContextFactory");
        props.put(Context.PROVIDER_URL, "http-remoting://localhost:8080");
        return new InitialContext(props);
    }
}

```

`ejb-remote-client/src/main/java/org/example/JaxRsActivator.java`:

```java
package main.java.org.example;

import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;

@ApplicationPath("/")
public class JaxRsActivator extends Application {
}

```

`ejb-remote-client/src/main/java/org/jboss/as/quickstarts/ejb/remote/stateful/RemoteCounter.java`:

```java
/*
 * JBoss, Home of Professional Open Source
 * Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual
 * contributors by the @authors tag. See the copyright.txt in the
 * distribution for a full listing of individual contributors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.jboss.as.quickstarts.ejb.remote.stateful;

/**
 * @author Jaikiran Pai
 */
public interface RemoteCounter {

    void increment();

    void decrement();

    int getCount();
}

```

`ejb-remote-client/src/main/java/org/jboss/as/quickstarts/ejb/remote/stateless/RemoteCalculator.java`:

```java
/*
 * JBoss, Home of Professional Open Source
 * Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual
 * contributors by the @authors tag. See the copyright.txt in the
 * distribution for a full listing of individual contributors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.jboss.as.quickstarts.ejb.remote.stateless;

/**
 * @author Jaikiran Pai
 */
public interface RemoteCalculator {

    int add(int a, int b);

    int subtract(int a, int b);
}

```

`ejb-remote-client/src/main/resources/META-INF/beans.xml`:

```xml
<beans xmlns="https://jakarta.ee/xml/ns/jakartaee" version="4.0" bean-discovery-mode="all"/>

```

`ejb-remote-client/src/webapp/WEB-INF/web.xml`:

```xml
<web-app xmlns="https://jakarta.ee/xml/ns/jakartaee" version="10">
    <display-name>ejb-remote-client</display-name>
</web-app>

```
  
# Erwarteter Outputs
Erstelle mir eine .md Datein welche einen identischen Aufbau wie die Eingbabe und die Beispiel hat:
1. Einen Projektbaum im `.md`-Format, der die neue Quarkus-Projektstruktur zeigt
2. Danach jede Datei im Tree mit:
   - Pfad im Projekt
   - Quellcode der Datei (vollständig) 
