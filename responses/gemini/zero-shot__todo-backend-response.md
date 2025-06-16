Absolut. Als Senior Java Enterprise Architekt führe ich Sie durch die Migration des WildFly `todo-backend`-Projekts nach Quarkus.

### Migrationsstrategie

Die Migration von WildFly nach Quarkus erfolgt in mehreren Schritten, um eine moderne, performante und Cloud-native Anwendung zu schaffen.

1.  **Analyse der Abhängigkeiten:** Die `pom.xml` wird von WildFly-spezifischen, `provided`-Abhängigkeiten (`jakarta.ws.rs-api`) befreit. Wir ersetzen diese durch die Quarkus Bill of Materials (BOM) und spezifische Quarkus-Extensions.
2.  **Build-System-Transformation:** Das Packaging wird von `war` auf `jar` umgestellt. Das `maven-war-plugin` wird durch das `quarkus-maven-plugin` ersetzt, welches den Build-Lebenszyklus für Quarkus steuert.
3.  **JAX-RS-Konfiguration:** Die JAX-RS `Application`-Klasse (`ToDoBackendApplication.java` und `Resources.java`), die in WildFly zur Aktivierung von JAX-RS und zur Definition des Basispfads dient, wird entfernt. In Quarkus wird dies deklarativ in der `application.properties` über `quarkus.resteasy-reactive.path` konfiguriert.
4.  **Komponentenmodell-Anpassung:** Der `ToDoController` wird von einem implizit durch JAX-RS verwalteten Objekt zu einem expliziten CDI-Bean durch Hinzufügen der `@ApplicationScoped`-Annotation. Dies ist der Standard in Quarkus und ermöglicht eine nahtlose Integration in das Quarkus-Ökosystem.
5.  **API-Umstellung:** Die Anwendung nutzt bereits Standard-Jakarta-EE-APIs (JAX-RS, Bean Validation). Wir stellen sicher, dass die Quarkus-Äquivalente (`quarkus-resteasy-reactive`, `quarkus-hibernate-validator`) verwendet werden, die für eine optimale Performance mit RESTEasy Reactive und Vert.x im Hintergrund sorgen.

Das Ergebnis ist eine schlanke, voll funktionsfähige Quarkus-Anwendung, die mit `mvn quarkus:dev` gestartet werden kann und die exakt gleiche Funktionalität wie das ursprüngliche WildFly-Projekt bietet.

---

### Projektstruktur (Quarkus)

```txt
todo-backend
├── pom.xml
├── src
│   └── main
│       ├── java
│       │   └── org
│       │       └── wildfly
│       │           └── quickstarts
│       │               └── todos
│       │                   ├── ToDo.java
│       │                   └── ToDoController.java
│       └── resources
│           └── application.properties
└── summary.md
```

### `pom.xml`

Der `pom.xml` wurde grundlegend überarbeitet, um die Quarkus-Build-Logik zu integrieren. Die Quarkus BOM (`quarkus-bom`) verwaltet die Versionen der Quarkus-Abhängigkeiten. Explizite Abhängigkeiten wie `hibernate-validator` wurden durch Quarkus-Extensions (`quarkus-hibernate-validator`, `quarkus-resteasy-reactive-jackson`) ersetzt. Das Packaging ist nun `jar`.

```xml
<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.wildfly.quickstarts</groupId>
    <artifactId>todo-backend-quarkus</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <compiler-plugin.version>3.13.0</compiler-plugin.version>
        <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id>
        <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id>
        <quarkus.platform.version>3.11.1</quarkus.platform.version>
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
        <!-- JAX-RS, JSON-B und Validierungs-APIs werden durch diese Extensions bereitgestellt -->
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
        <finalName>todo-backend</finalName>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>${compiler-plugin.version}</version>
                <configuration>
                    <source>${maven.compiler.source}</source>
                    <target>${maven.compiler.target}</target>
                    <encoding>${project.build.sourceEncoding}</encoding>
                </configuration>
            </plugin>
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
        </plugins>
    </build>
</project>
```

### `src/main/java/org/wildfly/quickstarts/todos/ToDo.java`

Das Datenmodell `ToDo.java` ist ein einfaches POJO mit Jakarta Validation Annotations. Es ist vollständig kompatibel mit Quarkus und erfordert keine Änderungen.

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

### `src/main/java/org/wildfly/quickstarts/todos/ToDoController.java`

Der JAX-RS Controller wurde minimal angepasst. Durch Hinzufügen von `@ApplicationScoped` wird die Klasse zu einem CDI-Bean, was dem Standard-Programmiermodell von Quarkus entspricht. Die restlichen JAX-RS-Annotationen und die Geschäftslogik bleiben unverändert.

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

    private static final List<ToDo> todos = Collections.synchronizedList(new ArrayList<>());
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

### `src/main/resources/application.properties`

Diese neue Datei ersetzt die `ToDoBackendApplication.java`. Sie konfiguriert den Basispfad der JAX-RS-Anwendung und setzt grundlegende Anwendungsinformationen.

```properties
# Anwendungs-Konfiguration
quarkus.application.name=todo-backend
quarkus.application.version=1.0.0

# HTTP-Konfiguration
quarkus.http.port=8080

# RESTEasy Reactive Konfiguration
# Setzt den globalen Basispfad für alle JAX-RS Endpunkte.
# Dies ersetzt die @ApplicationPath("/") Annotation aus der WildFly-Version.
quarkus.resteasy-reactive.path=/
```