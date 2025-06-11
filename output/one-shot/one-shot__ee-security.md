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
Project Path: ee-security

Source Tree:

```txt
ee-security
├── charts
│   └── helm.yaml
├── configure-elytron.cli
├── pom.xml
├── restore-configuration.cli
└── src
    ├── main
    │   ├── java
    │   │   └── org
    │   │       └── jboss
    │   │           └── as
    │   │               └── quickstarts
    │   │                   └── ee_security
    │   │                       ├── ElytronIdentityStore.java
    │   │                       ├── SecuredServlet.java
    │   │                       ├── SecurityFactory.java
    │   │                       └── TestAuthenticationMechanism.java
    │   └── webapp
    │       └── WEB-INF
    │           └── beans.xml
    └── test

```

`ee-security/charts/helm.yaml`:

```yaml
build:
  uri: https://github.com/wildfly/quickstart.git
  ref: main
  contextDir: ee-security
deploy:
  replicas: 1
```

`ee-security/configure-elytron.cli`:

```cli
# CLI script to enable elytron for the quickstart application in the application server

# Disable 'integrated-jaspi' as the quickstart will be managing it's own identities
/subsystem=undertow/application-security-domain=other:write-attribute(name=integrated-jaspi, value=false)

# Reload the server configuration
#reload

```

`ee-security/pom.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
    JBoss, Home of Professional Open Source
    Copyright 2018, Red Hat, Inc. and/or its affiliates, and individual
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

    <artifactId>ee-security</artifactId>
    <version>37.0.0.Beta1-SNAPSHOT</version>
    <packaging>war</packaging>
    <name>Quickstart: ee-security</name>
    <description>This project demonstrates using EE security</description>

    <licenses>
        <license>
            <name>Apache License, Version 2.0</name>
            <url>http://www.apache.org/licenses/LICENSE-2.0.html</url>
            <distribution>repo</distribution>
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

        <!-- Dependencies are included with a scope of 'provided' as they 
        are all available within the application server. -->

        <dependency>
            <groupId>jakarta.enterprise</groupId>
            <artifactId>jakarta.enterprise.cdi-api</artifactId>
            <scope>provided</scope>
        </dependency>

        <dependency>
            <groupId>jakarta.servlet</groupId>
            <artifactId>jakarta.servlet-api</artifactId>
            <scope>provided</scope>
        </dependency>

        <dependency>
            <groupId>jakarta.security.enterprise</groupId>
            <artifactId>jakarta.security.enterprise-api</artifactId>
            <scope>provided</scope>
        </dependency>

        <dependency>
            <groupId>org.wildfly.security</groupId>
            <artifactId>wildfly-elytron</artifactId>
            <scope>provided</scope>
        </dependency>
        

        <!-- Needed for running tests (you may also use TestNG) -->
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
                            <packaging-scripts>
                                <packaging-script>
                                    <scripts>
                                        <script>${basedir}/configure-elytron.cli</script>
                                    </scripts>
                                    <!-- Expressions resolved during server execution -->
                                    <resolve-expressions>false</resolve-expressions>
                                </packaging-script>
                            </packaging-scripts>
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
                            <packaging-scripts>
                                <packaging-script>
                                    <scripts>
                                        <script>${basedir}/configure-elytron.cli</script>
                                    </scripts>
                                    <!-- Expressions resolved during server execution -->
                                    <resolve-expressions>false</resolve-expressions>
                                </packaging-script>
                            </packaging-scripts>
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
                                <include>**/*IT</include>
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

`ee-security/restore-configuration.cli`:

```cli
# CLI script to restore the application server configuration that was modified to run the quickstart

# Activate 'integrated-jaspi' for the 'other' application-security-domain again.
/subsystem=undertow/application-security-domain=other:write-attribute(name=integrated-jaspi, value=true)

# Remove the WildFly Elytron JACC policy
/subsystem=elytron/policy=jacc:remove

# Reload the server configuration
reload

```

`ee-security/src/main/java/org/jboss/as/quickstarts/ee_security/ElytronIdentityStore.java`:

```java
/*
 * Copyright 2018 Red Hat, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.jboss.as.quickstarts.ee_security;

import static jakarta.security.enterprise.identitystore.CredentialValidationResult.INVALID_RESULT;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import org.wildfly.security.auth.server.SecurityDomain;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.security.enterprise.credential.Credential;
import jakarta.security.enterprise.credential.UsernamePasswordCredential;
import jakarta.security.enterprise.identitystore.CredentialValidationResult;
import jakarta.security.enterprise.identitystore.IdentityStore;

/**
 *
 * @author <a href="mailto:darran.lofthouse@jboss.com">Darran Lofthouse</a>
 */
@ApplicationScoped
public class ElytronIdentityStore implements IdentityStore {

    private static final Map<String, User> USERS;

    static {
        Map<String, User> users = new HashMap<>();
        User user = new User("quickstartUser", "quickstartPwd1!".toCharArray(), "Users");
        users.put(user.getUserName(), user);
        USERS = Collections.unmodifiableMap(users);
    }

    @Inject
    private SecurityDomain securityDomain;

    @Override
    public CredentialValidationResult validate(Credential credential) {
        if (credential instanceof UsernamePasswordCredential) {
            UsernamePasswordCredential upc = (UsernamePasswordCredential) credential;

            User candidate = USERS.get(upc.getCaller());
            if (candidate != null && Arrays.equals(candidate.getPassword(), upc.getPassword().getValue())) {
                return new CredentialValidationResult(candidate.getUserName(), candidate.getGroups());
            }
        }

        return INVALID_RESULT;
    }

    private static class User {

        private final String userName;
        private final char[] password;
        private final Set<String> groups;

        User(final String userName, final char[] password, final String... roles) {
            this.userName = userName;
            this.password = password;
            groups = new HashSet<>(Arrays.asList(roles));
        }

        public String getUserName() {
            return userName;
        }

        public char[] getPassword() {
            return password;
        }

        public Set<String> getGroups() {
            return groups;
        }

    }

}

```

`ee-security/src/main/java/org/jboss/as/quickstarts/ee_security/SecuredServlet.java`:

```java
/*
 * Copyright 2018 Red Hat, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.jboss.as.quickstarts.ee_security;

import java.io.IOException;
import java.io.PrintWriter;

import jakarta.inject.Inject;
import jakarta.security.enterprise.SecurityContext;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import org.wildfly.security.auth.server.SecurityIdentity;

/**
 *
 * @author <a href="mailto:darran.lofthouse@jboss.com">Darran Lofthouse</a>
 */
@WebServlet(value="/secured")
public class SecuredServlet extends HttpServlet {

    @Inject
    private SecurityContext securityContext;

    @Inject
    private SecurityIdentity securityIdentity;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        PrintWriter pw = resp.getWriter();
        pw.println("SecuredServlet - doGet()");
        pw.println(String.format("Identity as available from SecurityContext '%s'", securityContext.getCallerPrincipal().getName()));
        pw.println(String.format("Identity as available from injection '%s'", securityIdentity.getPrincipal().getName()));
    }

}

```

`ee-security/src/main/java/org/jboss/as/quickstarts/ee_security/SecurityFactory.java`:

```java
/*
 * Copyright 2018 Red Hat, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.jboss.as.quickstarts.ee_security;

import jakarta.enterprise.inject.Produces;

import org.wildfly.security.auth.server.SecurityDomain;
import org.wildfly.security.auth.server.SecurityIdentity;

/**
 *
 * @author <a href="mailto:darran.lofthouse@jboss.com">Darran Lofthouse</a>
 */
public class SecurityFactory {

    @Produces
    public SecurityDomain getSecurityDomain() {
        return SecurityDomain.getCurrent();
    }

    @Produces
    public SecurityIdentity getSecurityIdentity(SecurityDomain securityDomain) {
        return securityDomain.getCurrentSecurityIdentity();
    }

}

```

`ee-security/src/main/java/org/jboss/as/quickstarts/ee_security/TestAuthenticationMechanism.java`:

```java
/*
 * Copyright 2018 Red Hat, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.jboss.as.quickstarts.ee_security;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.security.enterprise.AuthenticationException;
import jakarta.security.enterprise.AuthenticationStatus;
import jakarta.security.enterprise.authentication.mechanism.http.HttpAuthenticationMechanism;
import jakarta.security.enterprise.authentication.mechanism.http.HttpMessageContext;
import jakarta.security.enterprise.credential.UsernamePasswordCredential;
import jakarta.security.enterprise.identitystore.CredentialValidationResult;
import jakarta.security.enterprise.identitystore.CredentialValidationResult.Status;
import jakarta.security.enterprise.identitystore.IdentityStoreHandler;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 * A simple {@link HttpAuthenticationMechanism} for testing.
 *
 * @author <a href="mailto:darran.lofthouse@jboss.com">Darran Lofthouse</a>
 */
@ApplicationScoped
public class TestAuthenticationMechanism implements HttpAuthenticationMechanism {

    static final String USERNAME_HEADER = "X-USERNAME";
    static final String PASSWORD_HEADER = "X-PASSWORD";
    static final String MESSAGE_HEADER = "X-MESSAGE";
    static final String MESSAGE = "Please resubmit the request with a username specified using the X-USERNAME and a password specified using the X-PASSWORD header.";

    @Inject
    private IdentityStoreHandler identityStoreHandler;

    @Override
    public AuthenticationStatus validateRequest(HttpServletRequest request, HttpServletResponse response,
            HttpMessageContext httpMessageContext) throws AuthenticationException {

        final String username = request.getHeader(USERNAME_HEADER);
        final String password = request.getHeader(PASSWORD_HEADER);

        if (username != null && password != null) {
            UsernamePasswordCredential upc = new UsernamePasswordCredential(username, password);
            CredentialValidationResult cvr = identityStoreHandler.validate(upc);

            if (cvr.getStatus() == Status.VALID) {
                return httpMessageContext.notifyContainerAboutLogin(cvr.getCallerPrincipal(), cvr.getCallerGroups());
            } else {
                return challenge(response, httpMessageContext);
            }
        }

        return challenge(response, httpMessageContext);
    }

    private static AuthenticationStatus challenge(HttpServletResponse response, HttpMessageContext httpMessageContext) {
        response.addHeader(MESSAGE_HEADER, MESSAGE);

        return httpMessageContext.responseUnauthorized();
    }

}

```

`ee-security/src/main/webapp/WEB-INF/beans.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
    JBoss, Home of Professional Open Source
    Copyright 2018, Red Hat, Inc. and/or its affiliates, and individual
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
<!-- Marker file indicating CDI should be enabled -->
<beans xmlns="https://jakarta.ee/xml/ns/jakartaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee https://jakarta.ee/xml/ns/jakartaee/beans_4_0.xsd"
    bean-discovery-mode="all" version="4.0">
</beans>

```
  
# Erwarteter Outputs
Erstelle mir eine .md Datein welche einen identischen Aufbau wie die Eingbabe und die Beispiel hat:
1. Einen Projektbaum im `.md`-Format, der die neue Quarkus-Projektstruktur zeigt
2. Danach jede Datei im Tree mit:
   - Pfad im Projekt
   - Quellcode der Datei (vollständig) 
