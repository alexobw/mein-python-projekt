# Projektbaum

```txt
ejb-remote-client-quarkus
├── pom.xml
└── src
    └── main
        ├── java
        │   └── org
        │       └── example
        │           ├── CalculatorResource.java
        │           ├── CounterResource.java
        │           ├── EJBLookupHelper.java
        └── resources
            └── META-INF
                └── resources
                    └── index.html
```

# Dateien

## `ejb-remote-client-quarkus/pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>
    <groupId>org.example</groupId>
    <artifactId>ejb-remote-client-quarkus</artifactId>
    <version>1.0.0</version>
    <name>EJB Remote Client Quarkus</name>
    <description>EJB Remote Client migrated to Quarkus</description>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id>
        <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id>
        <quarkus.platform.version>3.11.1</quarkus.platform.version>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
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
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive</artifactId>
        </dependency>
        <dependency>
            <groupId>org.jboss</groupId>
            <artifactId>jboss-ejb-client</artifactId>
            <version>4.0.42.Final</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>io.quarkus</groupId>
                <artifactId>quarkus-maven-plugin</artifactId>
                <version>${quarkus.platform.version}</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>build</goal>
                            <goal>generate-code</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

</project>
```

## `ejb-remote-client-quarkus/src/main/java/org/example/CalculatorResource.java`

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

## `ejb-remote-client-quarkus/src/main/java/org/example/CounterResource.java`

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

## `ejb-remote-client-quarkus/src/main/java/org/example/EJBLookupHelper.java`

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

## `ejb-remote-client-quarkus/src/main/resources/META-INF/resources/index.html`

```html
<html>
    <head>
        <meta http-equiv="Refresh" content="0; URL=calculator">
    </head>
</html>
```

In dieser Migration wurden die EJB-Remote-Client-Funktionalitäten beibehalten, wobei die REST-Endpunkte in Quarkus integriert wurden. Die Struktur und die Konfigurationen wurden entsprechend angepasst, um die Quarkus-Umgebung zu unterstützen.