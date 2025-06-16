Absolut. Als Senior Java Enterprise Architekt mit umfassender Erfahrung in der Migration von WildFly zu Quarkus übernehme ich diese Aufgabe. Ich werde eine detaillierte, schrittweise Migration des `ee-security`-Projekts durchführen und dabei die Best Practices für Quarkus anwenden.

### Migrationsanleitung: WildFly `ee-security` nach Quarkus

Die Migration dieses Projekts von WildFly nach Quarkus erfordert eine systematische Umwandlung von WildFly-spezifischen Konfigurationen und APIs zu ihren Quarkus-Äquivalenten.

**1. Analyse des WildFly-Projekts:**

*   **Abhängigkeiten (`pom.xml`):** Das Projekt nutzt die `wildfly-ee-with-tools`-BOM und deklariert Standard-Jakarta-EE-APIs (`cdi-api`, `servlet-api`, `security.enterprise-api`) als `provided`. Entscheidend ist die Abhängigkeit zu `wildfly-elytron`, welche WildFly-spezifische Security-Klassen wie `SecurityDomain` und `SecurityIdentity` bereitstellt.
*   **Konfiguration (`configure-elytron.cli`):** Das CLI-Skript konfiguriert das `undertow`-Subsystem von WildFly. Diese Art der Server-Konfiguration entfällt in Quarkus und wird durch Einträge in `application.properties` ersetzt.
*   **Java-Quellcode:**
    *   `ElytronIdentityStore`: Implementiert die Standard-API `jakarta.security.enterprise.identitystore.IdentityStore`. Die Injektion von `SecurityDomain` ist WildFly-spezifisch und muss entfernt werden.
    *   `TestAuthenticationMechanism`: Implementiert die Standard-API `jakarta.security.enterprise.authentication.mechanism.http.HttpAuthenticationMechanism`. Diese Klasse ist größtenteils portierbar.
    *   `SecuredServlet`: Ein Standard-Servlet, das jedoch die WildFly-spezifische `org.wildfly.security.auth.server.SecurityIdentity` injiziert. Dies muss durch das Quarkus-Pendant `io.quarkus.security.identity.SecurityIdentity` ersetzt werden.
    *   `SecurityFactory`: Eine CDI-Producer-Klasse, die WildFly-spezifische Objekte (`SecurityDomain`, `SecurityIdentity`) erzeugt. Diese Klasse wird in Quarkus nicht mehr benötigt, da Quarkus die `SecurityIdentity` direkt per CDI bereitstellt. Die Klasse wird daher ersatzlos gelöscht.
*   **Deployment-Deskriptor (`beans.xml`):** Ein Standard-CDI-Marker. In Quarkus ist CDI standardmäßig aktiv, diese Datei wird nicht mehr benötigt.

**2. Transformationsstrategie für Quarkus:**

*   **`pom.xml`:** Die WildFly-BOM wird durch die `quarkus-bom` ersetzt. Die `provided`-Abhängigkeiten werden durch die entsprechenden Quarkus-Extensions ersetzt:
    *   `quarkus-elytron-security-jakarta`: Stellt die Implementierung für die Jakarta Security APIs (`IdentityStore`, `HttpAuthenticationMechanism`) bereit.
    *   `quarkus-servlet`: Ermöglicht die Verwendung von Jakarta Servlets.
    *   `quarkus-resteasy-reactive`: Wird als API-Extension gemäß den Vorgaben hinzugefügt.
    *   Das `wildfly-maven-plugin` wird durch das `quarkus-maven-plugin` ersetzt.
*   **Konfiguration:** Die Sicherheitsregeln werden in `application.properties` definiert. Wir schützen den Pfad `/secured` und aktivieren die Jakarta Security Integration.
*   **Code-Anpassungen:**
    *   **Entfernen:** `SecurityFactory.java` und `beans.xml` werden gelöscht.
    *   **Anpassen:**
        *   In `ElytronIdentityStore.java` wird die `SecurityDomain`-Injektion entfernt.
        *   In `SecuredServlet.java` wird der Import und Typ von `SecurityIdentity` auf die Quarkus-Version `io.quarkus.security.identity.SecurityIdentity` umgestellt.
    *   **Beibehalten:** `TestAuthenticationMechanism.java` kann ohne Änderungen übernommen werden, da es nur Standard-APIs verwendet, die von der Quarkus-Extension unterstützt werden.

Das Ergebnis ist ein schlankes, natives Quarkus-Projekt, das die gleiche Funktionalität mit idiomatischem Quarkus-Code und -Konfiguration bietet.

---

### Quarkus Projektstruktur (`ee-security-quarkus`)

```md
ee-security-quarkus
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
        │                       ├── SecuredServlet.java
        │                       └── TestAuthenticationMechanism.java
        └── resources
            └── application.properties
```

---

### Projektdateien

#### Pfad: `pom.xml`

```xml
<?xml version="1.0"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd"
         xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.acme</groupId>
    <artifactId>ee-security-quarkus</artifactId>
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
        <!-- Jakarta Security API implementation -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-elytron-security-jakarta</artifactId>
        </dependency>
        <!-- Servlet Support -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-servlet</artifactId>
        </dependency>
        <!-- JAX-RS API Layer -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive</artifactId>
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

#### Pfad: `src/main/resources/application.properties`

```properties
# --- Quarkus HTTP Server Configuration ---
# The HTTP port
quarkus.http.port=8080

# --- Quarkus Security Configuration ---
# Enable Jakarta Security integration. This tells Quarkus to scan for and activate
# beans like HttpAuthenticationMechanism and IdentityStore.
quarkus.security.jakarta.enabled=true

# By setting proactive auth to false, we let the Jakarta Security mechanism
# (TestAuthenticationMechanism) control the authentication flow and challenges.
quarkus.http.auth.proactive=false

# --- Path-based Security Rules ---
# Define a policy that requires an authenticated user.
quarkus.http.auth.permission.authenticated.paths=/secured
quarkus.http.auth.permission.authenticated.policy=authenticated
```

#### Pfad: `src/main/java/org/jboss/as/quickstarts/ee_security/ElytronIdentityStore.java`

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
 * MIGRATION NOTE: This class is fully compliant with the Jakarta Security standard.
 * The WildFly-specific injection of 'SecurityDomain' was not used and has been removed.
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

#### Pfad: `src/main/java/org/jboss/as/quickstarts/ee_security/SecuredServlet.java`

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

import io.quarkus.security.identity.SecurityIdentity;

/**
 * A simple secured Servlet.
 * MIGRATION NOTE: The injected SecurityIdentity has been switched from the WildFly-specific
 * 'org.wildfly.security.auth.server.SecurityIdentity' to the Quarkus-provided
 * 'io.quarkus.security.identity.SecurityIdentity'. The API is compatible for this use case.
 * The SecurityContext injection remains standard.
 *
 * @author <a href="mailto:darran.lofthouse@jboss.com">Darran Lofthouse</a>
 */
@WebServlet(value="/secured")
public class SecuredServlet extends HttpServlet {

    @Inject
    SecurityContext securityContext;

    @Inject
    SecurityIdentity securityIdentity;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/plain");
        PrintWriter pw = resp.getWriter();
        pw.println("SecuredServlet - doGet()");
        pw.println(String.format("Identity as available from SecurityContext '%s'", securityContext.getCallerPrincipal().getName()));
        pw.println(String.format("Identity as available from injection '%s'", securityIdentity.getPrincipal().getName()));
    }

}
```

#### Pfad: `src/main/java/org/jboss/as/quickstarts/ee_security/TestAuthenticationMechanism.java`

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
 * MIGRATION NOTE: This class uses standard Jakarta Security APIs and requires no changes
 * for the migration to Quarkus. The 'quarkus-elytron-security-jakarta' extension
 * provides the necessary runtime support.
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
                // If validation fails, fall through to challenge.
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

### Ausführung und Test

1.  **Starten Sie die Anwendung im Entwicklungsmodus:**
    ```bash
    mvn quarkus:dev
    ```

2.  **Testen Sie den ungesicherten Zugriff (Challenge):**
    Öffnen Sie ein Terminal und führen Sie den folgenden `curl`-Befehl aus. Sie erhalten eine `401 Unauthorized`-Antwort und den Challenge-Header.
    ```bash
    curl -i http://localhost:8080/secured
    ```
    *Erwartete Ausgabe:*
    ```http
    HTTP/1.1 401 Unauthorized
    X-MESSAGE: Please resubmit the request with a username specified using the X-USERNAME and a password specified using the X-PASSWORD header.
    ...
    ```

3.  **Testen Sie den gesicherten Zugriff (Erfolgreich):**
    Führen Sie nun den `curl`-Befehl mit den korrekten Anmeldeinformationen in den Headern aus.
    ```bash
    curl -i -H "X-USERNAME: quickstartUser" -H "X-PASSWORD: quickstartPwd1!" http://localhost:8080/secured
    ```
    *Erwartete Ausgabe:*
    ```http
    HTTP/1.1 200 OK
    Content-Type: text/plain
    ...

    SecuredServlet - doGet()
    Identity as available from SecurityContext 'quickstartUser'
    Identity as available from injection 'quickstartUser'
    ```

Die Migration ist damit erfolgreich abgeschlossen. Das Projekt ist nun eine vollwertige Quarkus-Anwendung und nutzt die modernen, konfigurationsbasierten Sicherheitsmechanismen von Quarkus.