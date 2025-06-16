Absolut. Als Senior Java Enterprise Architekt übernehme ich die Migration des WildFly `todo-backend`-Projekts nach Quarkus. Hier ist die detaillierte Analyse, die Migrationsanleitung und der vollständige, lauffähige Quarkus-Code.

### Migrationsanalyse und Strategie

1.  **Analyse der WildFly-Abhängigkeiten und APIs:**
    *   **JAX-RS (`jakarta.ws.rs-api`):** Das Projekt nutzt JAX-RS für die REST-Endpunkte. Dies wird in Quarkus durch die Extension `quarkus-resteasy-reactive` abgedeckt. Da das Projekt bereits `jakarta.*`-APIs verwendet, ist keine Namespace-Migration (`javax` -> `jakarta`) notwendig.
    *   **Bean Validation (`jakarta.validation-api`, `hibernate-validator`):** Die Validierung des `ToDo`-Objekts wird verwendet. Quarkus bietet hierfür die `quarkus-hibernate-validator`-Extension, die diese Funktionalität nahtlos integriert.
    *   **JAX-RS Application Class (`ToDoBackendApplication.java`, `Resources.java`):** Das Projekt definiert zwei Klassen, die von `jakarta.ws.rs.core.Application` erben. In Quarkus ist dies nicht notwendig. Quarkus scannt den Classpath automatisch nach JAX-RS-Ressourcen (Klassen mit `@Path`). Die beiden `Application`-Klassen können ersatzlos entfernt werden, was den Code vereinfacht. Der `ApplicationPath` `@ApplicationPath("/")` entspricht dem Standardverhalten von Quarkus.
    *   **Packaging (`war`):** Das WildFly-Projekt ist als `.war`-Archiv gepackt. Quarkus-Anwendungen werden standardmäßig als ausführbare `.jar`-Dateien gepackt. Das Packaging im `pom.xml` wird entsprechend auf `jar` umgestellt.
    *   **Controller-Lifecycle:** Der `ToDoController` ist eine einfache POJO ohne Scope-Annotation. In WildFly wird der Lifecycle vom JAX-RS-Container verwaltet. In Quarkus ist es Best Practice, REST-Ressourcen zu CDI-Beans zu machen. Ich werde den Controller mit `@ApplicationScoped` annotieren, um ihn als Singleton-Bean zu deklarieren. Dies stellt sicher, dass die In-Memory-Liste (`todos`) über alle Anfragen hinweg erhalten bleibt.

2.  **Transformationsplan:**
    *   **`pom.xml`:**
        *   Das Packaging wird von `war` auf `jar` geändert.
        *   Die `quarkus-bom` wird im `<dependencyManagement>`-Abschnitt hinzugefügt, um die Versionen der Quarkus-Abhängigkeiten zentral zu verwalten.
        *   Die expliziten Abhängigkeiten (`jakarta.ws.rs-api`, `hibernate-validator`, etc.) werden durch die entsprechenden Quarkus-Extensions ersetzt: `quarkus-resteasy-reactive`, `quarkus-resteasy-reactive-jackson` (für JSON-Serialisierung) und `quarkus-hibernate-validator`.
        *   Der `maven-war-plugin` wird entfernt und durch den `quarkus-maven-plugin` ersetzt.
        *   Die Java-Version wird auf `21` aktualisiert, wie in den Vorgaben gefordert.
    *   **Java-Code:**
        *   Die Klassen `ToDoBackendApplication.java` und `Resources.java` werden gelöscht.
        *   Die Klasse `ToDoController.java` wird mit `@jakarta.enterprise.context.ApplicationScoped` annotiert.
        *   Die Klasse `ToDo.java` bleibt unverändert, da sie nur ein Datenmodell mit Standard-Annotations ist.
    *   **Konfiguration:**
        *   Eine neue Konfigurationsdatei `src/main/resources/application.properties` wird erstellt. Da das ursprüngliche Projekt keine externe Konfiguration (wie `standalone.xml` oder `persistence.xml`) verwendet, bleibt diese Datei zunächst leer oder enthält nur grundlegende Einstellungen wie den HTTP-Port.

Dieser systematische Ansatz stellt sicher, dass alle Funktionalitäten erhalten bleiben, während die Anwendung idiomatisch auf der Quarkus-Plattform läuft und von deren Vorteilen wie schnellerem Start und Live-Reloading (`quarkus:dev`) profitiert.

---

### Migriertes Quarkus-Projekt

Hier ist die vollständige, migrierte und lauffähige Quarkus-Anwendung.

### Projektstruktur

```txt
todo-backend-quarkus
├── pom.xml
└── src
    └── main
        ├── java
        │   └── org
        │       └── wildfly
        │           └── quickstarts
        │               └── todos
        │                   ├── ToDo.java
        │                   └── ToDoController.java
        └── resources
            └── application.properties
```

---

### `pom.xml`

**Pfad:** `todo-backend-quarkus/pom.xml`

```xml
<?xml version="1.0"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd"
         xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.wildfly.quickstarts</groupId>
    <artifactId>todo-backend-quarkus</artifactId>
    <version>1.0.0</version>

    <properties>
        <compiler-plugin.version>3.13.0</compiler-plugin.version>
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
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive-jackson</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-hibernate-validator</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-arc</artifactId>
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

### `ToDo.java`

**Pfad:** `todo-backend-quarkus/src/main/java/org/wildfly/quickstarts/todos/ToDo.java`

```java
package org.wildfly.quickstarts.todos;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

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

    public ToDo() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public int getOrder() {
        return order;
    }

    public void setOrder(int order) {
        this.order = order;
    }
}
```

### `ToDoController.java`

**Pfad:** `todo-backend-quarkus/src/main/java/org/wildfly/quickstarts/todos/ToDoController.java`

```java
package org.wildfly.quickstarts.todos;


import jakarta.enterprise.context.ApplicationScoped;
import jakarta.validation.Valid;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.Context;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.core.UriInfo;

import java.net.URI;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;


@Path("/todos")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
@ApplicationScoped
public class ToDoController {

    private final List<ToDo> todos = Collections.synchronizedList(new ArrayList<>());
    private final AtomicLong idGenerator = new AtomicLong(1);

    public ToDoController() {
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

### `application.properties`

**Pfad:** `todo-backend-quarkus/src/main/resources/application.properties`

```properties
# Quarkus Application Configuration
# This file is intentionally left empty for this simple application.
# You can configure properties like the HTTP port here:
# quarkus.http.port=8080
```