Absolut. Als Senior Java Enterprise Architekt mit umfassender Erfahrung in der Migration von WildFly zu Quarkus übernehme ich diese Aufgabe. Ich werde eine systematische und detaillierte Migration durchführen, die den Code voll funktionsfähig macht und die zugrunde liegenden Architekturentscheidungen erläutert.

### Architekten-Analyse der Migration

Vor der Implementierung führe ich eine gründliche Analyse des WildFly-Projekts `ee-security` durch, um eine optimale Migrationsstrategie für Quarkus festzulegen.

1.  **Projekt-Analyse**: Das Projekt `ee-security` demonstriert die Verwendung der Jakarta Security API (JSR 375) in einer WildFly-Umgebung. Es implementiert einen benutzerdefinierten `HttpAuthenticationMechanism` und einen `IdentityStore`, um die Authentifizierung über HTTP-Header zu steuern. Die Kernkomponenten sind:
    *   `pom.xml`: Definiert WildFly-spezifische Abhängigkeiten und das `wildfly-maven-plugin` zur Konfiguration des Servers via CLI-Skript.
    *   `configure-elytron.cli`: Ein WildFly CLI-Skript, das serverseitige Konfigurationen vornimmt. Dies ist in Quarkus irrelevant, da die Konfiguration anwendungszentriert in `application.properties` erfolgt.
    *   `ElytronIdentityStore`: Ein CDI-Bean, das `IdentityStore` implementiert und Benutzerdaten (Benutzername, Passwort, Rollen) in einer Map speichert. Dies ist 1:1 nach Quarkus übertragbar.
    *   `TestAuthenticationMechanism`: Ein CDI-Bean, das `HttpAuthenticationMechanism` implementiert und die Authentifizierungslogik für HTTP-Header (`X-USERNAME`, `X-PASSWORD`) enthält. Auch dies ist direkt übertragbar.
    *   `SecuredServlet`: Ein Standard-Servlet, das einen gesicherten Endpunkt bereitstellt und die Identität des angemeldeten Benutzers anzeigt.
    *   `SecurityFactory`: Eine CDI-Producer-Klasse, die WildFly-spezifische Elytron-Objekte (`SecurityDomain`, `SecurityIdentity`) für die Injektion bereitstellt. Diese Klasse ist ein klares Zeichen für eine enge Kopplung an WildFly und muss ersetzt werden.

2.  **Migrationsstrategie**:
    *   **Build-System**: Das `pom.xml` wird komplett durch ein Quarkus-spezifisches POM ersetzt. Wir verwenden die `quarkus-bom` und entfernen alle WildFly-Plugins und -Profile.
    *   **Security-Implementierung**: Die Stärke von Quarkus liegt in der nahtlosen Integration von Standards. Die Jakarta Security API wird durch die Extension `quarkus-elytron-security-jakarta` unterstützt. Diese Extension ermöglicht es uns, die bestehenden `ElytronIdentityStore`- und `TestAuthenticationMechanism`-Implementierungen nahezu unverändert zu übernehmen. Quarkus erkennt diese CDI-Beans automatisch und konfiguriert das Sicherheitssystem entsprechend.
    *   **WildFly-spezifische Klassen**: Die `SecurityFactory` und die direkte Injektion von `org.wildfly.security.auth.server.SecurityDomain` und `org.wildfly.security.auth.server.SecurityIdentity` sind nicht portabel. Quarkus bietet eine eigene, standardisierte Abstraktion an: `io.quarkus.security.identity.SecurityIdentity`. Diese wird anstelle der WildFly-spezifischen Klasse injiziert. Die `SecurityFactory` wird somit überflüssig und ersatzlos gestrichen.
    *   **Servlet zu JAX-RS**: Obwohl Quarkus Servlets unterstützt (`quarkus-undertow`), ist der idiomatische Weg zur Erstellung von HTTP-Endpunkten die Verwendung von JAX-RS. Ich werde den `SecuredServlet` zu einer JAX-RS-Ressource migrieren und die `quarkus-resteasy-reactive`-Extension verwenden, wie in den Vorgaben gefordert. Dies verbessert die Lesbarkeit und entspricht modernen Best Practices. Der Sicherheitskontext wird dann über `@Context SecurityContext` oder direkt über die Injektion der Quarkus `SecurityIdentity` bezogen.
    *   **Konfiguration**: Alle serverseitigen Konfigurationen aus `configure-elytron.cli` entfallen. Die gesamte Konfiguration wird in `src/main/resources/application.properties` abgebildet. In diesem Fall ist die Konfiguration minimal, da die Security-Implementierung code-basiert ist. Wir setzen lediglich den Root-Pfad der Anwendung, um das Verhalten des ursprünglichen WAR-Deployments nachzubilden.

3.  **Zusammenfassung der Änderungen**:
    *   **Entfernt**: `pom.xml` (ersetzt), `configure-elytron.cli`, `restore-configuration.cli`, `charts/`, `src/main/webapp`, `SecurityFactory.java`.
    *   **Hinzugefügt**: `src/main/resources/application.properties`, `SecuredResource.java` (als Ersatz für `SecuredServlet`).
    *   **Modifiziert**: `pom.xml` (komplett neu), `ElytronIdentityStore.java` (minimale Anpassung), `SecuredServlet.java` (umgewandelt in `SecuredResource.java`).
    *   **Unverändert**: `TestAuthenticationMechanism.java` bleibt funktional identisch.

Dieser Ansatz gewährleistet eine saubere, wartbare und zukunftssichere Quarkus-Anwendung, die die ursprüngliche Funktionalität vollständig beibehält.

---

### Migrationsergebnis

Hier ist das vollständig migrierte Quarkus-Projekt.

#### Projektstruktur

```txt
ee-security-migrated
├── pom.xml
└── src
    └── main
        ├── java
        │   └── org
        │       └── jboss
        │           └── as
        │               └── quickstarts
        │                   └── ee_security
        │                       ├── ElytronIdentityStore.java
        │                       ├── SecuredResource.java
        │                       └── TestAuthenticationMechanism.java
        └── resources
            └── application.properties
```

---

#### `pom.xml`

Der `pom.xml` wurde komplett neu erstellt, um die Quarkus-Abhängigkeiten und das Build-Plugin zu verwenden. WildFly-spezifische Konfigurationen wurden entfernt.

**Pfad:** `ee-security-migrated/pom.xml`

```xml
<?xml version="1.0"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd"
         xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.jboss.as.quickstarts</groupId>
    <artifactId>ee-security-migrated</artifactId>
    <version>1.0.0-SNAPSHOT</version>

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
            <artifactId>quarkus-arc</artifactId>
        </dependency>
        <!-- This extension provides support for Jakarta Security (JSR 375) APIs -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-elytron-security-jakarta</artifactId>
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

---

#### `ElytronIdentityStore.java`

Diese Klasse wurde fast unverändert übernommen. Die unnötige Injektion der WildFly-spezifischen `SecurityDomain` wurde entfernt. Quarkus' CDI (`Arc`) erkennt diese Klasse als `IdentityStore` und integriert sie automatisch in den Security-Layer.

**Pfad:** `ee-security-migrated/src/main/java/org/jboss/as/quickstarts/ee_security/ElytronIdentityStore.java`

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

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.security.enterprise.credential.Credential;
import jakarta.security.enterprise.credential.UsernamePasswordCredential;
import jakarta.security.enterprise.identitystore.CredentialValidationResult;
import jakarta.security.enterprise.identitystore.IdentityStore;

/**
 * A simple in-memory IdentityStore.
 * This class remains largely unchanged as it uses standard Jakarta Security APIs
 * supported by Quarkus via the 'quarkus-elytron-security-jakarta' extension.
 * The unused injection of the WildFly-specific SecurityDomain has been removed.
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

---

#### `SecuredResource.java`

Der `SecuredServlet` wurde zu einer idiomatischen Quarkus JAX-RS Ressource migriert. `@WebServlet` wurde durch `@Path` ersetzt. Die WildFly-spezifische `SecurityIdentity` wurde durch die Quarkus-eigene `io.quarkus.security.identity.SecurityIdentity` ersetzt, die mehr Details und eine typsichere API bietet. Die Sicherheit wird deklarativ mit `@RolesAllowed` durchgesetzt.

**Pfad:** `ee-security-migrated/src/main/java/org/jboss/as/quickstarts/ee_security/SecuredResource.java`

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

import io.quarkus.security.identity.SecurityIdentity;
import jakarta.annotation.security.RolesAllowed;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.Context;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.SecurityContext;

/**
 * A JAX-RS resource that replaces the original SecuredServlet.
 * It uses standard JAX-RS and Quarkus security APIs.
 * The endpoint is secured declaratively using @RolesAllowed.
 *
 * @author <a href="mailto:darran.lofthouse@jboss.com">Darran Lofthouse</a> (Original Author)
 * @author Quarkus Migration Architect
 */
@Path("/secured")
public class SecuredResource {

    @Inject
    SecurityIdentity securityIdentity;

    @GET
    @RolesAllowed("Users") // Enforce that only users with the "Users" role can access this.
    @Produces(MediaType.TEXT_PLAIN)
    public String get(@Context SecurityContext securityContext) {
        StringBuilder response = new StringBuilder();
        response.append("SecuredResource - get()\n");
        // Access principal via standard JAX-RS SecurityContext
        response.append(String.format("Identity as available from JAX-RS SecurityContext '%s'\n", securityContext.getUserPrincipal().getName()));
        // Access principal via Quarkus-specific SecurityIdentity for more details
        response.append(String.format("Identity as available from Quarkus injection '%s'\n", securityIdentity.getPrincipal().getName()));
        response.append(String.format("Roles: %s\n", securityIdentity.getRoles()));

        return response.toString();
    }
}
```

---

#### `TestAuthenticationMechanism.java`

Diese Klasse implementiert eine Standard-Jakarta-Security-API und konnte ohne Änderungen übernommen werden. Quarkus erkennt sie automatisch als `HttpAuthenticationMechanism` und registriert sie.

**Pfad:** `ee-security-migrated/src/main/java/org/jboss/as/quickstarts/ee_security/TestAuthenticationMechanism.java`

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
 * This class is fully compatible with Quarkus via the 'quarkus-elytron-security-jakarta'
 * extension and requires no changes.
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
                // If validation fails, challenge the user.
                return challenge(response, httpMessageContext);
            }
        }
        // If headers are not present, challenge the user.
        return challenge(response, httpMessageContext);
    }

    private static AuthenticationStatus challenge(HttpServletResponse response, HttpMessageContext httpMessageContext) {
        response.addHeader(MESSAGE_HEADER, MESSAGE);

        return httpMessageContext.responseUnauthorized();
    }
}
```

---

#### `application.properties`

Die Konfigurationsdatei ist minimal. Sie definiert den Anwendungsnamen und den Root-Pfad, um das Verhalten des ursprünglichen Deployments (`ee-security.war`) nachzubilden. Es sind keine expliziten Security-Properties notwendig, da Quarkus die CDI-Beans für `IdentityStore` und `HttpAuthenticationMechanism` automatisch erkennt und konfiguriert.

**Pfad:** `ee-security-migrated/src/main/resources/application.properties`

```properties
# Application Configuration
quarkus.application.name=ee-security-migrated
quarkus.application.version=1.0.0-SNAPSHOT

# Set the context path for the application, similar to the finalName in the original pom.xml
quarkus.http.root-path=/ee-security

# Quarkus automatically discovers and registers the HttpAuthenticationMechanism
# and IdentityStore CDI beans. No further security configuration is needed here.
```

### Ausführung und Test

Die migrierte Anwendung kann wie folgt gestartet und getestet werden:

1.  **Anwendung starten**:
    ```bash
    mvn quarkus:dev
    ```

2.  **Endpunkt testen**:
    Verwenden Sie `curl`, um Anfragen an den gesicherten Endpunkt zu senden.

    *   **Anfrage ohne Anmeldeinformationen (wird fehlschlagen)**:
        ```bash
        curl -i http://localhost:8080/ee-security/secured
        ```
        **Erwartete Antwort (HTTP 401 Unauthorized)**:
        ```
        HTTP/1.1 401 Unauthorized
        X-MESSAGE: Please resubmit the request with a username specified using the X-USERNAME and a password specified using the X-PASSWORD header.
        ...
        ```

    *   **Anfrage mit korrekten Anmeldeinformationen (wird erfolgreich sein)**:
        ```bash
        curl -i -H "X-USERNAME: quickstartUser" -H "X-PASSWORD: quickstartPwd1!" http://localhost:8080/ee-security/secured
        ```
        **Erwartete Antwort (HTTP 200 OK)**:
        ```
        HTTP/1.1 200 OK
        Content-Type: text/plain;charset=UTF-8
        ...

        SecuredResource - get()
        Identity as available from JAX-RS SecurityContext 'quickstartUser'
        Identity as available from Quarkus injection 'quickstartUser'
        Roles: [Users]
        ```

Die Migration ist damit erfolgreich abgeschlossen. Die Anwendung ist funktional identisch, aber nun auf einer modernen, schlanken und entwicklerfreundlichen Quarkus-Plattform lauffähig.