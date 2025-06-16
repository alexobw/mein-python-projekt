# Migrationsergebnis: WildFly zu Quarkus

## Projektstruktur

```txt
ejb-remote-client-quarkus
├── pom.xml
└── src
    └── main
        ├── java
        │   └── org
        │       ├── example
        │       │   ├── CalculatorResource.java
        │       │   ├── CounterResource.java
        │       │   ├── EJBService.java
        │       │   └── JaxRsActivator.java
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
            │   └── resources
            └── application.properties
```

## Dateien

### `ejb-remote-client-quarkus/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>org.example</groupId>
    <artifactId>ejb-remote-client-quarkus</artifactId>
    <version>1.0.0</version>
    
    <properties>
        <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id>
        <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id>
        <quarkus.platform.version>3.11.1</quarkus.platform.version>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
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
        <finalName>ejb-remote-client-quarkus</finalName>
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
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>21</source>
                    <target>21</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### `ejb-remote-client-quarkus/src/main/java/org/example/CalculatorResource.java`

```java
package org.example;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import org.jboss.as.quickstarts.ejb.remote.stateless.RemoteCalculator;
import java.util.Map;

@Path("/calculator")
@Produces(MediaType.APPLICATION_JSON)
public class CalculatorResource {

    @Inject
    EJBService ejbService;

    @GET
    @Path("/add")
    public Response add(@QueryParam("a") int a, @QueryParam("b") int b) {
        try {
            RemoteCalculator calc = ejbService.getCalculator();
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
            RemoteCalculator calc = ejbService.getCalculator();
            int result = calc.subtract(a, b);
            return Response.ok(Map.of("operation", "subtract", "a", a, "b", b, "result", result)).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }
}
```

### `ejb-remote-client-quarkus/src/main/java/org/example/CounterResource.java`

```java
package org.example;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import org.jboss.as.quickstarts.ejb.remote.stateful.RemoteCounter;
import java.util.Map;

@Path("/counter")
@Produces(MediaType.APPLICATION_JSON)
public class CounterResource {

    @Inject
    EJBService ejbService;

    @POST
    @Path("/increment")
    public Response increment() {
        try {
            RemoteCounter counter = ejbService.getCounter();
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
            RemoteCounter counter = ejbService.getCounter();
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
            RemoteCounter counter = ejbService.getCounter();
            int value = counter.getCount();
            return Response.ok(Map.of("counter", value)).build();
        } catch (Exception e) {
            return Response.serverError().entity(Map.of("error", e.getMessage())).build();
        }
    }
}
```

### `ejb-remote-client-quarkus/src/main/java/org/example/EJBService.java`

```java
package org.example;

import jakarta.enterprise.context.ApplicationScoped;
import org.jboss.as.quickstarts.ejb.remote.stateful.RemoteCounter;
import org.jboss.as.quickstarts.ejb.remote.stateless.RemoteCalculator;

/**
 * Service that implements the remote EJB interfaces locally for Quarkus.
 * In a real-world scenario, this would either:
 * 1. Connect to a remote service using REST/gRPC
 * 2. Implement the business logic directly (if migrating the entire application)
 */
@ApplicationScoped
public class EJBService {

    // Simple implementation of the calculator
    private final RemoteCalculator calculator = new RemoteCalculator() {
        @Override
        public int add(int a, int b) {
            return a + b;
        }

        @Override
        public int subtract(int a, int b) {
            return a - b;
        }
    };

    // Simple implementation of the counter with state
    private final RemoteCounter counter = new RemoteCounter() {
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
    };

    public RemoteCalculator getCalculator() {
        return calculator;
    }

    public RemoteCounter getCounter() {
        return counter;
    }
}
```

### `ejb-remote-client-quarkus/src/main/java/org/example/JaxRsActivator.java`

```java
package org.example;

import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;

@ApplicationPath("/")
public class JaxRsActivator extends Application {
    // This class is needed to activate JAX-RS
}
```

### `ejb-remote-client-quarkus/src/main/java/org/jboss/as/quickstarts/ejb/remote/stateful/RemoteCounter.java`

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

### `ejb-remote-client-quarkus/src/main/java/org/jboss/as/quickstarts/ejb/remote/stateless/RemoteCalculator.java`

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

### `ejb-remote-client-quarkus/src/main/resources/application.properties`

```properties
# Quarkus configuration
quarkus.http.port=8080
quarkus.http.root-path=/
quarkus.application.name=ejb-remote-client-quarkus
```