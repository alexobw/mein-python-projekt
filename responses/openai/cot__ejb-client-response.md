# Quarkus Migration Guide

## Projektbaum

```txt
ejb-remote-client
├── pom.xml
└── src
    ├── main
    │   ├── java
    │   │   └── org
    │   │       └── example
    │   │           ├── CalculatorResource.java
    │   │           ├── CounterResource.java
    │   │           └── EJBLookupHelper.java
    │   └── resources
    │       └── application.properties
```

## Dateien

### `ejb-remote-client/pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.example</groupId>
    <artifactId>ejb-remote-client</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <quarkus.version>3.11.1</quarkus.version>
    </properties>

    <dependencies>
        <!-- Quarkus BOM -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-bom</artifactId>
            <version>${quarkus.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>

        <!-- Quarkus RESTEasy Reactive -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive</artifactId>
        </dependency>

        <!-- Quarkus EJB Client -->
        <dependency>
            <groupId>org.jboss</groupId>
            <artifactId>jboss-ejb-client</artifactId>
            <version>4.0.42.Final</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>21</source>
                    <target>21</target>
                </configuration>
            </plugin>
            <plugin>
                <groupId>io.quarkus</groupId>
                <artifactId>quarkus-maven-plugin</artifactId>
                <version>${quarkus.version}</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>build</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

### `ejb-remote-client/src/main/java/org/example/CalculatorResource.java`

```java
package org.example;

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

### `ejb-remote-client/src/main/java/org/example/CounterResource.java`

```java
package org.example;

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

### `ejb-remote-client/src/main/java/org/example/EJBLookupHelper.java`

```java
package org.example;

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

### `ejb-remote-client/src/main/resources/application.properties`

```properties
# Quarkus application properties
quarkus.http.port=8080
quarkus.http.host=0.0.0.0
```

## Hinweise zur Migration

1. **Projektstruktur**: Die Struktur wurde vereinfacht, indem unnötige Verzeichnisse entfernt wurden. Quarkus benötigt keine `web.xml` oder `beans.xml`.

2. **POM-Konfiguration**: Die POM-Datei wurde aktualisiert, um Quarkus-spezifische Abhängigkeiten und Plugins zu verwenden. Die Java-Version wurde auf 21 aktualisiert, um den Anforderungen zu entsprechen.

3. **RESTEasy Reactive**: Die REST-API wurde auf Quarkus RESTEasy Reactive umgestellt, was eine bessere Integration und Performance in Quarkus bietet.

4. **EJB-Client**: Die EJB-Client-Abhängigkeit bleibt bestehen, da die Remote-EJB-Aufrufe weiterhin verwendet werden. Eine Umstellung auf RESTful Services könnte in Betracht gezogen werden, um die Architektur zu modernisieren.

5. **Konfiguration**: Die Konfiguration wurde von `standalone.xml` zu `application.properties` migriert, um die Quarkus-Konventionen zu erfüllen.