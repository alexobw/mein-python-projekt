Absolut. Als Senior Java Enterprise Architekt mit umfassender Erfahrung in der Migration von WildFly zu Quarkus übernehme ich diese Aufgabe. Die Migration von EJB-Remote-Clients ist ein klassisches Szenario, bei dem Quarkus durch seine Konfigurations- und Injektionsmechanismen erhebliche Vereinfachungen bietet.

Hier ist die vollständige Migration des `ejb-remote-client`-Projekts nach Quarkus 3.11.1.

### Migrations-Analyse

1.  **Build-System (`pom.xml`):**
    *   Das `packaging` wird von `war` auf `jar` umgestellt, da Quarkus-Anwendungen standardmäßig als ausführbare Jars gepackt werden.
    *   Die `quarkus-bom` wird importiert, um die Versionen der Quarkus-Abhängigkeiten zentral zu verwalten.
    *   Die explizite Abhängigkeit `jakarta.ws.rs-api` wird durch die Quarkus-Extension `quarkus-resteasy-reactive-jackson` ersetzt. Diese Extension stellt nicht nur die JAX-RS-API bereit, sondern auch die Jackson-Bibliothek für die JSON-Serialisierung, die in den REST-Endpunkten verwendet wird.
    *   Die `jboss-ejb-client`-Abhängigkeit wird durch die Quarkus-Extension `quarkus-ejb-client` ersetzt. Diese ermöglicht die nahtlose Integration von Remote-EJB-Aufrufen mittels CDI.
    *   Der `maven-war-plugin` wird entfernt und durch den `quarkus-maven-plugin` ersetzt, der den Build-Lebenszyklus und die Entwicklungsmodi (`quarkus:dev`) steuert.
    *   Die Java-Version wird gemäß den Vorgaben auf 21 aktualisiert.

2.  **EJB-Client-Konfiguration:**
    *   Die manuelle JNDI-Konfiguration und der Lookup-Code in `EJBLookupHelper.java` werden vollständig entfernt. Diese Klasse wird obsolet.
    *   Die Verbindungsinformationen (Initial Context Factory, Provider URL) werden deklarativ in die `application.properties` verschoben. Quarkus nutzt diese Konfiguration, um den JNDI-Kontext für die gesamte Anwendung bereitzustellen.

3.  **Source-Code-Transformation:**
    *   **`EJBLookupHelper.java`:** Wird gelöscht. Die Funktionalität wird durch Quarkus' CDI-Integration ersetzt.
    *   **`JaxRsActivator.java`:** Wird gelöscht. Quarkus RESTEasy Reactive scannt den Classpath automatisch nach JAX-RS-Ressourcen. Die `@ApplicationPath("/")` ist das Standardverhalten und muss nicht explizit konfiguriert werden.
    *   **`CalculatorResource.java` & `CounterResource.java`:**
        *   Der programmatische Aufruf von `EJBLookupHelper.lookup...()` wird durch die CDI-Annotation `@EJB` ersetzt.
        *   Die JNDI-Lookup-Strings werden direkt in der `@EJB(lookup = "...")`-Annotation angegeben.
        *   Beide Ressourcen werden zu `@ApplicationScoped` CDI-Beans, um die Injektion zu ermöglichen. Für die `CounterResource` stellt dies sicher, dass der stateful EJB-Proxy über alle Anfragen hinweg erhalten bleibt, was das Verhalten der ursprünglichen `static`-Initialisierung nachbildet.
    *   **Package-Struktur:** Die fehlerhafte Package-Deklaration `package main.java.org.example;` wird zu `package org.example;` korrigiert und die Verzeichnisstruktur entsprechend auf den Maven-Standard `src/main/java/org/example` angepasst.
    *   **`RemoteCalculator.java` & `RemoteCounter.java`:** Diese Interfaces definieren den Remote-Vertrag und bleiben unverändert.

4.  **Konfigurations- und Metadaten-Dateien:**
    *   `src/main/resources/META-INF/beans.xml`: Wird entfernt. Quarkus aktiviert CDI standardmäßig und benötigt diese Datei nicht.
    *   `src/main/webapp/WEB-INF/web.xml`: Wird entfernt, da es sich nicht mehr um eine WAR-Anwendung handelt.

Das Ergebnis ist eine schlankere, modernere Anwendung, die idiomatische Quarkus-Patterns verwendet und gleichzeitig die exakt gleiche Funktionalität wie das ursprüngliche WildFly-Projekt beibehält.

---

### Neue Projektstruktur

```txt
ejb-remote-client-quarkus
├── pom.xml
└── src
    └── main
        ├── java
        │   ├── org
        │   │   ├── example
        │   │   │   ├── CalculatorResource.java
        │   │   │   └── CounterResource.java
        │   │   └── jboss
        │   │       └── as
        │   │           └── quickstarts
        │   │               └── ejb
        │   │                   └── remote
        │   │                       ├── stateful
        │   │                       │   └── RemoteCounter.java
        │   │                       └── stateless
        │   │                           └── RemoteCalculator.java
        └── resources
            └── application.properties
```

---

### Migrierte Dateien

#### `ejb-remote-client-quarkus/pom.xml`

```xml
<?xml version="1.0"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd"
         xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.example</groupId>
    <artifactId>ejb-remote-client-quarkus</artifactId>
    <version>1.0.0</version>

    <properties>
        <compiler-plugin.version>3.11.0</compiler-plugin.version>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id>
        <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id>
        <quarkus.platform.version>3.11.1</quarkus.platform.version>
        <surefire-plugin.version>3.2.5</surefire-plugin.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>${quarkus.platform.group-id}</groupId>
                <artifactId>${quarkus.platform.artifact-id}</artifactId>
                <version>${quarkus.platform.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <!-- JAX-RS, JSON-B, and other web functionalities -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive-jackson</artifactId>
        </dependency>
        <!-- EJB Client for remote EJB calls -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-ejb-client</artifactId>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>${quarkus.platform.group-id}</groupId>
                <artifactId>quarkus-maven-plugin</artifactId>
                <version>${quarkus.platform.version}</version>
                <extensions>true</extensions>
                <executions>
                    <execution>
                        <goals>
                            <goal>build</goal>
                            <goal>generate-code</goal>
                            <goal>generate-code-tests</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>${compiler-plugin.version}</version>
                <configuration>
                    <compilerArgs>
                        <arg>-parameters</arg>
                    </compilerArgs>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

#### `ejb-remote-client-quarkus/src/main/resources/application.properties`

```properties
# Quarkus EJB Client Configuration
# These properties replace the manual InitialContext setup from EJBLookupHelper.java

# 1. Define the remote connection to the WildFly server
quarkus.ejb.remote.connections.default.host=localhost
quarkus.ejb.remote.connections.default.port=8080
quarkus.ejb.remote.connections.default.protocol=http-remoting

# 2. Configure the JNDI context properties
# This tells the EJB client which factory to use for lookups.
quarkus.naming.context.initial.factory=org.wildfly.naming.client.WildFlyInitialContextFactory
quarkus.naming.provider.url=http-remoting://localhost:8080

# Optional: Set the application root path if needed. Default is "/"
# quarkus.resteasy-reactive.path=/
```

#### `ejb-remote-client-quarkus/src/main/java/org/example/CalculatorResource.java`

```java
package org.example;

import jakarta.ejb.EJB;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.jboss.as.quickstarts.ejb.remote.stateless.RemoteCalculator;

import java.util.Map;

@Path("/calculator")
@ApplicationScoped
@Produces(MediaType.APPLICATION_JSON)
public class CalculatorResource {

    @EJB(lookup = "ejb:/ejb-remote/CalculatorBean!org.jboss.as.quickstarts.ejb.remote.stateless.RemoteCalculator")
    RemoteCalculator calculator;

    @GET
    @Path("/add")
    public Response add(@QueryParam("a") int a, @QueryParam("b") int b) {
        try {
            int result = calculator.add(a, b);
            return Response.ok(Map.of("operation", "add", "a", a, "b", b, "result", result)).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }

    @GET
    @Path("/subtract")
    public Response subtract(@QueryParam("a") int a, @Query_Param("b") int b) {
        try {
            int result = calculator.subtract(a, b);
            return Response.ok(Map.of("operation", "subtract", "a", a, "b", b, "result", result)).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }
}
```

#### `ejb-remote-client-quarkus/src/main/java/org/example/CounterResource.java`

```java
package org.example;

import jakarta.ejb.EJB;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.jboss.as.quickstarts.ejb.remote.stateful.RemoteCounter;

import java.util.Map;

@Path("/counter")
@ApplicationScoped
@Produces(MediaType.APPLICATION_JSON)
public class CounterResource {

    // By injecting the stateful EJB into an @ApplicationScoped bean,
    // we ensure that a single stateful session is used for all requests,
    // mimicking the behavior of the original static field.
    @EJB(lookup = "ejb:/ejb-remote/CounterBean!org.jboss.as.quickstarts.ejb.remote.stateful.RemoteCounter?stateful")
    RemoteCounter counter;

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

#### `ejb-remote-client-quarkus/src/main/java/org/jboss/as/quickstarts/ejb/remote/stateful/RemoteCounter.java`

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

#### `ejb-remote-client-quarkus/src/main/java/org/jboss/as/quickstarts/ejb/remote/stateless/RemoteCalculator.java`

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

---

### Ausführungsanleitung

1.  **Voraussetzung:** Stellen Sie sicher, dass eine WildFly-Instanz läuft und die Remote-EJB-Anwendung (`ejb-remote.jar`) darauf deployed ist. Die EJB-Anwendung ist typischerweise in den WildFly Quickstarts zu finden.

2.  **Kompilieren und Starten:**
    Navigieren Sie in das Stammverzeichnis des neuen Projekts `ejb-remote-client-quarkus` und starten Sie die Anwendung im Entwicklungsmodus:
    ```bash
    mvn quarkus:dev
    ```
    Die Anwendung startet und verbindet sich mit dem WildFly-Server, wie in `application.properties` konfiguriert.

3.  **Endpunkte testen:**
    Öffnen Sie ein neues Terminal und verwenden Sie `curl`, um die Endpunkte zu testen.

    *   **Calculator (Stateless):** Jeder Aufruf ist unabhängig.
        ```bash
        # Add
        curl "http://localhost:8080/calculator/add?a=100&b=200"
        # Expected Output: {"operation":"add","a":100,"b":200,"result":300}

        # Subtract
        curl "http://localhost:8080/calculator/subtract?a=50&b=25"
        # Expected Output: {"operation":"subtract","a":50,"b":25,"result":25}
        ```

    *   **Counter (Stateful):** Die Aufrufe bauen aufeinander auf, da der Zustand auf dem Server gehalten wird.
        ```bash
        # Get initial value
        curl http://localhost:8080/counter/value
        # Expected Output: {"counter":0}

        # Increment
        curl -X POST http://localhost:8080/counter/increment
        # Expected Output: {"action":"increment","value":1}

        # Increment again
        curl -X POST http://localhost:8080/counter/increment
        # Expected Output: {"action":"increment","value":2}

        # Get current value
        curl http://localhost:8080/counter/value
        # Expected Output: {"counter":2}

        # Decrement
        curl -X POST http://localhost:8080/counter/decrement
        # Expected Output: {"action":"decrement","value":1}
        ```

Die Migration ist damit abgeschlossen. Das Projekt ist nun eine native Quarkus-Anwendung, die ihre Geschäftslogik über Remote-EJBs bezieht und dabei moderne, deklarative Konfigurations- und Injektionsmechanismen nutzt.