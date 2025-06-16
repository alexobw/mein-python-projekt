# Migrationsergebnis: WildFly zu Quarkus

## Projektstruktur

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

## Dateien

### `todo-backend-quarkus/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>org.wildfly.quickstarts</groupId>
    <artifactId>todo-backend-quarkus</artifactId>
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
        
        <!-- Validation -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-hibernate-validator</artifactId>
        </dependency>
    </dependencies>
    
    <build>
        <finalName>todo-backend-quarkus</finalName>
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

### `todo-backend-quarkus/src/main/java/org/wildfly/quickstarts/todos/ToDo.java`

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

### `todo-backend-quarkus/src/main/java/org/wildfly/quickstarts/todos/ToDoController.java`

```java
package org.wildfly.quickstarts.todos;

import jakarta.validation.Valid;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;

import java.net.URI;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

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

### `todo-backend-quarkus/src/main/resources/application.properties`

```properties
# HTTP configuration
quarkus.http.port=8080
quarkus.http.root-path=/

# Logging configuration
quarkus.log.level=INFO
quarkus.log.console.enable=true

# Disable unused features
quarkus.arc.remove-unused-beans=true
```