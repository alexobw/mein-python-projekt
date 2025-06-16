# Migration von WildFly zu Quarkus: ejb-remote-client

## Projektstruktur nach der Migration

```
ejb-remote-client
├── pom.xml
└── src
    └── main
        ├── java
        │   └── org
        │       ├── example
        │       │   ├── CalculatorResource.java
        │       │   ├── CounterResource.java
        │       │   ├── EJBLookupHelper.java
        │       │   ├── JaxRsActivator.java
        │       │   ├── service
        │       │   │   ├── CalculatorService.java
        │       │   │   └── CounterService.java
        │       │   └── startup
        │       │       └── AppLifecycleBean.java
        │       └── jboss
        │           └── as
        │               └── quickstarts
        │                   └── ejb
        │                       └── remote
        │                           ├── stateful
        │                           │   └── RemoteCounter.java
        │                           └── stateless
        │                               └── RemoteCalculator.java
        └── resources
            ├── META-INF
            │   └── beans.xml
            └── application.properties
```

## Dateiinhalte

### `pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.example</groupId>
    <artifactId>ejb-remote-client</artifactId>
    <version>1.0.0</version>

    <properties>
        <compiler-plugin.version>3.11.0</compiler-plugin.version>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <quarkus.platform.version>3.11.1</quarkus.platform.version>
        <skipITs>true</skipITs>
        <surefire-plugin.version>3.2.5</surefire-plugin.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>io.quarkus.platform</groupId>
                <artifactId>quarkus-bom</artifactId>
                <version>${quarkus.platform.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <!-- REST API -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive-jackson</artifactId>
        </dependency>
        
        <!-- CDI -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-arc</artifactId>
        </dependency>
    </dependencies>

    <build>
        <finalName>ejb-remote-client</finalName>
        <plugins>
            <plugin>
                <groupId>io.quarkus.platform</groupId>
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
            <plugin>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>${surefire-plugin.version}</version>
                <configuration>
                    <systemPropertyVariables>
                        <java.util.logging.manager>org.jboss.logmanager.LogManager</java.util.logging.manager>
                        <maven.home>${maven.home}</maven.home>
                    </systemPropertyVariables>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### `src/main/java/org/example/CalculatorResource.java`

```java
package org.example;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import org.example.service.CalculatorService;
import java.util.Map;

@Path("/calculator")
@Produces(MediaType.APPLICATION_JSON)
public class CalculatorResource {

    @Inject
    CalculatorService calculatorService;

    @GET
    @Path("/add")
    public Response add(@QueryParam("a") int a, @QueryParam("b") int b) {
        try {
            int result = calculatorService.add(a, b);
            return Response.ok(Map.of("operation", "add", "a", a, "b", b, "result", result)).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }

    @GET
    @Path("/subtract")
    public Response subtract(@QueryParam("a") int a, @QueryParam("b") int b) {
        try {
            int result = calculatorService.subtract(a, b);
            return Response.ok(Map.of("operation", "subtract", "a", a, "b", b, "result", result)).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }
}
```

### `src/main/java/org/example/CounterResource.java`

```java
package org.example;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import org.example.service.CounterService;
import java.util.Map;

@Path("/counter")
@Produces(MediaType.APPLICATION_JSON)
public class CounterResource {

    @Inject
    CounterService counterService;

    @POST
    @Path("/increment")
    public Response increment() {
        try {
            counterService.increment();
            return Response.ok(Map.of("action", "increment", "value", counterService.getCount())).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }

    @POST
    @Path("/decrement")
    public Response decrement() {
        try {
            counterService.decrement();
            return Response.ok(Map.of("action", "decrement", "value", counterService.getCount())).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }

    @GET
    @Path("/value")
    public Response value() {
        try {
            int value = counterService.getCount();
            return Response.ok(Map.of("counter", value)).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }
}
```

### `src/main/java/org/example/EJBLookupHelper.java`

```java
package org.example;

// Diese Klasse wird in Quarkus nicht mehr benötigt, da wir keine EJB-Lookups mehr durchführen.
// Sie wird nur aus Kompatibilitätsgründen beibehalten, aber nicht verwendet.
@Deprecated
public class EJBLookupHelper {
    // Leere Implementierung, da wir in Quarkus CDI-Beans verwenden
}
```

### `src/main/java/org/example/JaxRsActivator.java`

```java
package org.example;

import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;

@ApplicationPath("/")
public class JaxRsActivator extends Application {
    // In Quarkus wird diese Klasse weiterhin verwendet, um den Basis-Pfad für REST-Endpunkte zu definieren
}
```

### `src/main/java/org/example/service/CalculatorService.java`

```java
package org.example.service;

import jakarta.enterprise.context.ApplicationScoped;
import org.jboss.as.quickstarts.ejb.remote.stateless.RemoteCalculator;

@ApplicationScoped
public class CalculatorService implements RemoteCalculator {

    @Override
    public int add(int a, int b) {
        return a + b;
    }

    @Override
    public int subtract(int a, int b) {
        return a - b;
    }
}
```

### `src/main/java/org/example/service/CounterService.java`

```java
package org.example.service;

import jakarta.enterprise.context.ApplicationScoped;
import org.jboss.as.quickstarts.ejb.remote.stateful.RemoteCounter;

@ApplicationScoped
public class CounterService implements RemoteCounter {
    
    private int count = 0;

    @Override
    public void increment() {
        count++;
    }

    @Override
    public void decrement() {
        count--;
    }

    @Override
    public int getCount() {
        return count;
    }
}
```

### `src/main/java/org/example/startup/AppLifecycleBean.java`

```java
package org.example.startup;

import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import org.jboss.logging.Logger;

@ApplicationScoped
public class AppLifecycleBean {

    private static final Logger LOGGER = Logger.getLogger(AppLifecycleBean.class);

    void onStart(@Observes StartupEvent ev) {
        LOGGER.info("Die Anwendung wurde erfolgreich gestartet");
        LOGGER.info("Die EJB-Remote-Funktionalität wurde durch lokale CDI-Beans ersetzt");
    }
}
```

### `src/main/java/org/jboss/as/quickstarts/ejb/remote/stateful/RemoteCounter.java`

```java
package org.jboss.as.quickstarts.ejb.remote.stateful;

/**
 * Interface für den Counter-Service
 */
public interface RemoteCounter {

    void increment();

    void decrement();

    int getCount();
}
```

### `src/main/java/org/jboss/as/quickstarts/ejb/remote/stateless/RemoteCalculator.java`

```java
package org.jboss.as.quickstarts.ejb.remote.stateless;

/**
 * Interface für den Calculator-Service
 */
public interface RemoteCalculator {

    int add(int a, int b);

    int subtract(int a, int b);
}
```

### `src/main/resources/META-INF/beans.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="https://jakarta.ee/xml/ns/jakartaee"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee https://jakarta.ee/xml/ns/jakartaee/beans_4_0.xsd"
       version="4.0" bean-discovery-mode="all">
</beans>
```

### `src/main/resources/application.properties`

```properties
# Konfiguration für Quarkus
quarkus.http.port=8080
quarkus.http.root-path=/
quarkus.application.name=ejb-remote-client
quarkus.banner.enabled=true

# Logging-Konfiguration
quarkus.log.console.enable=true
quarkus.log.console.format=%d{HH:mm:ss} %-5p [%c{2.}] (%t) %s%e%n
quarkus.log.console.level=INFO
```