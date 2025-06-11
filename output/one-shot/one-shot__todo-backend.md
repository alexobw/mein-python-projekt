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
Project Path: todo-backend

Source Tree:

```txt
todo-backend
├── pom.xml
├── src
│   ├── main
│   │   ├── java
│   │   │   └── org
│   │   │       └── wildfly
│   │   │           └── quickstarts
│   │   │               └── todos
│   │   │                   ├── Resources.java
│   │   │                   ├── ToDo.java
│   │   │                   ├── ToDoBackendApplication.java
│   │   │                   └── ToDoController.java
│   │   └── resources
│   │       └── META-INF
│   └── test
└── summary.md

```

`todo-backend/pom.xml`:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.wildfly.quickstarts</groupId>
    <artifactId>todo-backend</artifactId>
    <version>1.0.0</version>
    <packaging>war</packaging>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>jakarta.ws.rs</groupId>
            <artifactId>jakarta.ws.rs-api</artifactId>
            <version>3.1.0</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>jakarta.validation</groupId>
            <artifactId>jakarta.validation-api</artifactId>
            <version>3.0.2</version>
        </dependency>
        <dependency>
            <groupId>org.hibernate.validator</groupId>
            <artifactId>hibernate-validator</artifactId>
            <version>7.0.5.Final</version>
        </dependency>
        <dependency>
        <groupId>org.glassfish</groupId>
            <artifactId>jakarta.el</artifactId>
            <version>4.0.2</version>
        </dependency>
    </dependencies>

<build>
  <finalName>todo-backend</finalName>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <version>3.8.1</version>
      <configuration>
        <source>17</source>
        <target>17</target>
        <encoding>UTF-8</encoding>
      </configuration>
    </plugin>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-war-plugin</artifactId>
      <version>3.3.2</version>
      <configuration>
        <failOnMissingWebXml>false</failOnMissingWebXml>
      </configuration>
    </plugin>
  </plugins>
</build>
</project>

```

`todo-backend/src/main/java/org/wildfly/quickstarts/todos/Resources.java`:

```java
package org.wildfly.quickstarts.todos;

import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;

@ApplicationPath("/")
public class Resources extends Application {
}
```

`todo-backend/src/main/java/org/wildfly/quickstarts/todos/ToDo.java`:

```java
package org.wildfly.quickstarts.todos;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import jakarta.validation.constraints.Min;
import jakarta.validation.Valid;



public class ToDo {

    private Long id;
    @NotNull
    @Size(min = 1, max = 20)
    private String title;
    @NotNull
    private boolean completed;
    private String url;
    @Min(0)
    private int order;


    public ToDo(Long id, String title, boolean completed, String url, int order) {
        this.id = id;
        this.title = title;
        this.completed = completed;
        this.url = url;
        this.order = order;
    }
    
    public ToDo() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public boolean isCompleted() { return completed; }
    public void setCompleted(boolean completed) { this.completed = completed; }
    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }
    public int getOrder() { return order; }
    public void setOrder(int order) { this.order = order; }
}
```

`todo-backend/src/main/java/org/wildfly/quickstarts/todos/ToDoBackendApplication.java`:

```java
package org.wildfly.quickstarts.todos;

import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.core.Application;

@ApplicationPath("/")
public class ToDoBackendApplication extends Application {
}

```

`todo-backend/src/main/java/org/wildfly/quickstarts/todos/ToDoController.java`:

```java
package org.wildfly.quickstarts.todos;


import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import java.net.URI;
import java.util.*;
import java.util.concurrent.atomic.AtomicLong;
import jakarta.validation.Valid;


@Path("/todos")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ToDoController {

    private static final List<ToDo> todos = new ArrayList<>();
    private static final AtomicLong idGenerator = new AtomicLong(1);

    static {
        todos.add(new ToDo(idGenerator.getAndIncrement(), "Willkommen bei ToDo!", false, "/todos/1", 1));
        todos.add(new ToDo(idGenerator.getAndIncrement(), "Erstelle dein erstes ToDo", false, "/todos/2", 2));
        todos.add(new ToDo(idGenerator.getAndIncrement(), "Lösche ein ToDo", false, "/todos/3", 3));
    }

    @GET
    public List<ToDo> getAll() {
        return todos;
    }

    @POST
    public Response create(@Valid ToDo todo, @Context UriInfo uriInfo) {
        todo.setId(idGenerator.getAndIncrement());
        todo.setUrl("/todos/" + todo.getId());
        todos.add(todo);
        return Response.created(URI.create(todo.getUrl())).entity(todo).build();
    }

    @GET
    @Path("/{id}")
    public Response getById(@PathParam("id") long id) {
        return todos.stream()
                .filter(t -> t.getId() == id)
                .findFirst()
                .map(Response::ok)
                .orElse(Response.status(Response.Status.NOT_FOUND))
                .build();
    }

    @PUT
    @Path("/{id}")
    public Response update(@PathParam("id") long id, @Valid ToDo updated) {
        for (int i = 0; i < todos.size(); i++) {
            ToDo t = todos.get(i);
            if (t.getId().equals(id)) {
                updated.setId(id);
                updated.setUrl(t.getUrl());
                todos.set(i, updated);
                return Response.ok(updated).build();
            }
        }
        return Response.status(Response.Status.NOT_FOUND).build();
    }

    @DELETE
    @Path("/{id}")
    public Response delete(@PathParam("id") long id) {
        boolean removed = todos.removeIf(t -> t.getId().equals(id));
        return removed ? Response.noContent().build() : Response.status(Response.Status.NOT_FOUND).build();
    }

    @DELETE
    public Response deleteAll() {
        todos.clear();
        return Response.noContent().build();
    }
}

```
  
# Erwarteter Outputs
Erstelle mir eine .md Datein welche einen identischen Aufbau wie die Eingbabe und die Beispiel hat:
1. Einen Projektbaum im `.md`-Format, der die neue Quarkus-Projektstruktur zeigt
2. Danach jede Datei im Tree mit:
   - Pfad im Projekt
   - Quellcode der Datei (vollständig) 
