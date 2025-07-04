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
Migriere das folgende WildFly-Projekt vollständig zu Quarkus. Das bedeutet, dass alle Aspekte der aktuellen WildFly-Implementierung, einschließlich Konfigurationen, Abhängigkeiten und Jakarta EE (ehemals Java EE) APIs, so umgewandelt werden müssen, dass sie nativ in einer Quarkus-Umgebung funktionieren. Die Migration soll sich an Best Practices orientieren, insbesondere im Hinblick auf Erweiterungen, Konfigurationsstruktur, REST-Endpunkte und CDI-Nutzung.
  
Dieses Beispiel zeigt exemplarisch, wie eine vollständige Migration von einem einfachen WildFly-Projekt zu einer funktional äquivalenten Quarkus-Anwendung aussehen soll.
  
## Beispiel:
Project Path: helloworld-prompt-wildfly

Source Tree:

```txt
helloworld-prompt-wildfly
├── charts
│   └── helm.yaml
├── pom.xml
└── src
    └── main
        ├── java
        │   └── org
        │       └── jboss
        │           └── as
        │               └── quickstarts
        │                   └── helloworld
        │                       └── HelloWorldServlet.java
        └── webapp
            └── index.html

```

`helloworld-prompt-wildfly/charts/helm.yaml`:

```yaml
build:
  uri: https://github.com/wildfly/quickstart.git
  ref: main
  contextDir: helloworld
deploy:
  replicas: 1
```

`helloworld-prompt-wildfly/pom.xml`:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!--
    JBoss, Home of Professional Open Source
    Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual
    contributors by the @authors tag. See the copyright.txt in the
    distribution for a full listing of individual contributors.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
-->
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.wildfly.quickstarts</groupId>
        <artifactId>wildfly-quickstart-parent</artifactId>
        <!--
        Maintain separation between the artifact id and the version to help prevent
        merge conflicts between commits changing the GA and those changing the V.
        -->
        <version>10</version>
        <relativePath/>
    </parent>
    <artifactId>helloworld</artifactId>
    <version>37.0.0.Beta1-SNAPSHOT</version>
    <packaging>war</packaging>
    <name>Quickstart: helloworld</name>
    <description>Helloworld</description>

    <licenses>
        <license>
            <name>Apache License, Version 2.0</name>
            <distribution>repo</distribution>
            <url>http://www.apache.org/licenses/LICENSE-2.0.html</url>
        </license>
    </licenses>

    <properties>
        <!-- the Maven project should use the minimum Java SE version supported -->
        <maven.compiler.release>17</maven.compiler.release>
        <!-- the version for the Server -->
        <version.server>36.0.0.Final</version.server>
        <!-- the versions for BOMs, Packs and Plugins -->
        <version.bom.ee>${version.server}</version.bom.ee>
        <version.plugin.wildfly>5.1.2.Final</version.plugin.wildfly>
    </properties>

    <dependencyManagement>
        <dependencies>
            <!-- importing the ee-with-tools BOM adds specs and other useful artifacts as managed dependencies -->
            <dependency>
                <groupId>org.wildfly.bom</groupId>
                <artifactId>wildfly-ee-with-tools</artifactId>
                <version>${version.bom.ee}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <!-- Import the Servlet API, we use provided scope as the API is included in the server -->
        <dependency>
            <groupId>jakarta.servlet</groupId>
            <artifactId>jakarta.servlet-api</artifactId>
            <scope>provided</scope>
        </dependency>

        <!-- Tests -->
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <!-- Set the name of the WAR, used as the context root when the app is deployed. -->
        <finalName>${project.artifactId}</finalName>
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>org.wildfly.plugins</groupId>
                    <artifactId>wildfly-maven-plugin</artifactId>
                    <version>${version.plugin.wildfly}</version>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>

    <profiles>
        <profile>
            <id>provisioned-server</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <build>
                <plugins>
                    <plugin>
                        <groupId>org.wildfly.plugins</groupId>
                        <artifactId>wildfly-maven-plugin</artifactId>
                        <configuration>
                            <discover-provisioning-info>
                                <version>${version.server}</version>
                            </discover-provisioning-info>
                        </configuration>
                        <executions>
                            <execution>
                                <goals>
                                    <goal>package</goal>
                                </goals>
                            </execution>
                        </executions>
                    </plugin>
                </plugins>
            </build>
        </profile>
        <profile>
            <id>bootable-jar</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <build>
                <plugins>
                    <plugin>
                        <groupId>org.wildfly.plugins</groupId>
                        <artifactId>wildfly-maven-plugin</artifactId>
                        <configuration>
                            <discover-provisioning-info>
                                <version>${version.server}</version>
                            </discover-provisioning-info>
                            <bootable-jar>true</bootable-jar>
                        </configuration>
                        <executions>
                            <execution>
                                <goals>
                                    <goal>package</goal>
                                </goals>
                            </execution>
                        </executions>
                    </plugin>
                </plugins>
            </build>
        </profile>
        <profile>
            <id>openshift</id>
            <build>
                <plugins>
                    <plugin>
                        <groupId>org.wildfly.plugins</groupId>
                        <artifactId>wildfly-maven-plugin</artifactId>
                        <configuration>
                            <discover-provisioning-info>
                                <version>${version.server}</version>
                                <context>cloud</context>
                            </discover-provisioning-info>
                        </configuration>
                        <executions>
                            <execution>
                                <goals>
                                    <goal>package</goal>
                                </goals>
                            </execution>
                        </executions>
                    </plugin>
                    <!-- do not attach sources to openshift deployments -->
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-source-plugin</artifactId>
                        <executions>
                            <execution>
                                <id>attach-sources</id>
                                <phase>none</phase>
                            </execution>
                        </executions>
                    </plugin>
                </plugins>
            </build>
        </profile>
        <profile>
            <id>integration-testing</id>
            <build>
                <plugins>
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-failsafe-plugin</artifactId>
                        <configuration>
                            <includes>
                                <include>**/BasicRuntimeIT</include>
                            </includes>
                        </configuration>
                        <executions>
                            <execution>
                                <goals>
                                    <goal>integration-test</goal>
                                    <goal>verify</goal>
                                </goals>
                            </execution>
                        </executions>
                    </plugin>
                </plugins>
            </build>
        </profile>
    </profiles>

    <repositories>
        <repository>
            <id>jboss-public-maven-repository</id>
            <name>JBoss Public Maven Repository</name>
            <url>https://repository.jboss.org/nexus/content/groups/public/</url>
            <releases>
                <enabled>true</enabled>
                <updatePolicy>never</updatePolicy>
            </releases>
            <snapshots>
                <enabled>true</enabled>
                <updatePolicy>never</updatePolicy>
            </snapshots>
            <layout>default</layout>
        </repository>
    </repositories>
    <pluginRepositories>
        <pluginRepository>
            <id>jboss-public-maven-repository</id>
            <name>JBoss Public Maven Repository</name>
            <url>https://repository.jboss.org/nexus/content/groups/public/</url>
            <releases>
                <enabled>true</enabled>
            </releases>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </pluginRepository>
    </pluginRepositories>
</project>

```

`helloworld-prompt-wildfly/src/main/java/org/jboss/as/quickstarts/helloworld/HelloWorldServlet.java`:

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
package org.jboss.as.quickstarts.helloworld;

import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.io.PrintWriter;

/**
 *
 * <p>
 * The servlet is registered and mapped to /HelloServlet using the {@linkplain WebServlet
 * @HttpServlet}.
 * </p>
 *
 * @author Pete Muir
 *
 */
@WebServlet("/HelloWorld")
public class HelloWorldServlet extends HttpServlet {

    static String PAGE_HEADER = "<html><head><title>helloworld</title></head><body>";

    static String PAGE_FOOTER = "</body></html>";

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.setContentType("text/html");
        PrintWriter writer = resp.getWriter();
        writer.println(PAGE_HEADER);
        writer.println("<h1>Hello World!</h1>");
        writer.println(PAGE_FOOTER);
        writer.close();
    }

}

```

`helloworld-prompt-wildfly/src/main/webapp/index.html`:

```html
<!--
    JBoss, Home of Professional Open Source
    Copyright 2015, Red Hat, Inc. and/or its affiliates, and individual
    contributors by the @authors tag. See the copyright.txt in the
    distribution for a full listing of individual contributors.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
-->
<!-- Plain HTML page that kicks us into the app -->

<html>
    <head>
        <meta http-equiv="Refresh" content="0; URL=HelloWorld">
    </head>
</html>

```


  
## Erwarteter Output:
Project Path: helloworld-quarkus

Source Tree:

```txt
helloworld-quarkus
├── pom.xml
└── src
    └── main
        ├── java
        │   └── org
        │       └── jboss
        │           └── quickstarts
        │               └── helloworld
        │                   └── HelloWorldResource.java
        └── resources
            └── META-INF
                └── resources
                    └── index.html

```

`helloworld-quarkus/pom.xml`:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>
    <groupId>org.jboss.as.quickstarts</groupId>
    <artifactId>helloworld</artifactId>
    <version>1.0.0</version>
    <name> Helloworld</name>
    <description>Helloworld</description>

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

`helloworld-quarkus/src/main/java/org/jboss/quickstarts/helloworld/HelloWorldResource.java`:

```java
package org.jboss.as.quickstarts.helloworld;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

@Path("/HelloWorld")
public class HelloWorldResource {

    private static final String PAGE_HEADER = "<html><head><title>helloworld</title></head><body>";
    private static final String PAGE_FOOTER = "</body></html>";

    @GET
    @Produces(MediaType.TEXT_HTML)
    public String hello() {
        return PAGE_HEADER +
               "<h1>Hello World!</h1>" +
               PAGE_FOOTER;
    }
}

```

`helloworld-quarkus/src/main/resources/META-INF/resources/index.html`:

```html
<html>
    <head>
        <meta http-equiv="Refresh" content="0; URL=HelloWorld">
    </head>
</html>

```
  
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
