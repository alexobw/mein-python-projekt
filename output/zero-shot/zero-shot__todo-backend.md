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
Migriere das folgende WildFly-Projekt vollständig zu Quarkus. Das bedeutet, dass alle Aspekte der aktuellen WildFly-Implementierung, einschließlich Konfigurationen, Abhängigkeiten und Jakarta EE (ehemals Java EE) APIs, so umgewandelt werden müssen, dass sie nativ in einer Quarkus-Umgebung funktionieren. Berücksichtige dabei die bestmöglichen Quarkus-Äquivalente und -Pattern für jede Komponente.
  
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
