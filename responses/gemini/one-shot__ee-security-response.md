Absolut. Als Senior Java Enterprise Architekt mit umfassender Erfahrung in der Migration von WildFly zu Quarkus übernehme ich diese Aufgabe. Ich werde eine systematische und detaillierte Migration des `ee-security`-Projekts durchführen und dabei die Best Practices für Quarkus anwenden.

### Migrationsanalyse und Strategie

1.  **Analyse des WildFly-Projekts (`ee-security`)**:
    *   **Kerntechnologien**: Das Projekt nutzt Jakarta EE Security (JSR 375) mit einer benutzerdefinierten `HttpAuthenticationMechanism` und `IdentityStore`. Es wird durch einen `WebServlet` exponiert.
    *   **Abhängigkeiten**: Die `pom.xml` deklariert `jakarta.servlet-api`, `jakarta.enterprise.cdi-api`, `jakarta.security.enterprise-api` und `wildfly-elytron`. Alle sind `provided`, da sie vom WildFly-Server bereitgestellt werden.
    *   **WildFly-spezifische Implementierungen**:
        *   `SecurityFactory.java`: Diese Klasse produziert WildFly-spezifische Sicherheitsobjekte (`org.wildfly.security.auth.server.SecurityDomain`, `org.wildfly.security.auth.server.SecurityIdentity`). Dies ist ein gängiges Muster in WildFly, um an den zugrundeliegenden Sicherheitskontext zu gelangen.
        *   `ElytronIdentityStore.java` und `SecuredServlet.java`: Diese Klassen injizieren die von `SecurityFactory` produzierten WildFly-Typen.
        *   `configure-elytron.cli`: Dieses Skript modifiziert die WildFly-Konfiguration, was für eine Standalone-Anwendung wie Quarkus irrelevant ist. Die Konfiguration wird in `application.properties` abgebildet.

2.  **Transformationsstrategie für Quarkus**:
    *   **Abhängigkeiten**: Die WildFly-BOM und `provided`-Abhängigkeiten werden durch die Quarkus-BOM und spezifische Quarkus-Erweiterungen ersetzt. Wir benötigen:
        *   `quarkus-resteasy-reactive`: Um den `WebServlet` durch einen modernen, reaktiven JAX-RS-Endpunkt zu ersetzen.
        *   `quarkus-security`: Diese Erweiterung aktiviert das Quarkus-Sicherheitsframework und bietet die Implementierung für die Jakarta Security APIs.
    *   **Code-Transformation**:
        *   `SecuredServlet` -> `SecuredResource`: Der Servlet wird in eine JAX-RS-Ressource umgewandelt. Dies ist der idiomatische Weg in Quarkus.
        *   `SecurityFactory`: Diese Klasse wird überflüssig. Quarkus ermöglicht die direkte Injektion seiner eigenen `io.quarkus.security.identity.SecurityIdentity`. Die WildFly-spezifischen Klassen werden entfernt.
        *   `ElytronIdentityStore` & `TestAuthenticationMechanism`: Diese Klassen implementieren Standard-Jakarta-EE-APIs. Sie können größtenteils beibehalten werden. Die WildFly-spezifische Injektion in `ElytronIdentityStore` wird entfernt. Quarkus erkennt diese CDI-Beans automatisch und integriert sie in seine Sicherheits-Pipeline.
    *   **Konfiguration**: Die Pfadsicherung, die implizit durch die Kombination aus `HttpAuthenticationMechanism` und Servlet erfolgte, wird explizit in `application.properties` konfiguriert. Dies macht die Sicherheitsregeln transparent und zentral verwaltbar.
    *   **Projektstruktur**: Die `webapp`-Struktur und `beans.xml` werden entfernt. Die Konfiguration wandert nach `src/main/resources`.

Diese systematische Transformation stellt sicher, dass die Anwendung nicht nur funktional äquivalent ist, sondern auch den Designprinzipien und Vorteilen von Quarkus entspricht.

---

### Migrationsergebnis: ee-security-quarkus

Project Path: ee-security-quarkus

Source Tree:

```txt
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
        │                       ├── SecuredResource.java
        │                       └── TestAuthenticationMechanism.java
        └── resources
            └── application.properties

```

`ee-security-quarkus/pom.xml`:

```xml
<?xml version="1.0"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd"
         xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.jboss.as.quickstarts</groupId>
    <artifactId>ee-security-quarkus</artifactId>
    <version>1.0.0-SNAPSHOT</version>

    <name>Quarkus - Quickstart: ee-security</name>
    <description>This project demonstrates using EE security in Quarkus</description>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <maven.compiler.release>21</maven.compiler.release>
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
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-security</artifactId>
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
                <version>3.12.1</version>
                <configuration>
                    <compilerArgs>
                        <arg>-parameters</arg>
                    </compilerArgs>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

`ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/ElytronIdentityStore.java`:

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
 * An IdentityStore for authenticating users.
 *
 * MIGRATION NOTE: This class is almost identical to the WildFly version.
 * The WildFly-specific injection of `SecurityDomain` has been removed as it is not
 * available in Quarkus and was not used by the validation logic.
 * Quarkus automatically discovers and uses any CDI bean that implements IdentityStore.
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

`ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/SecuredResource.java`:

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
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.security.enterprise.SecurityContext;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

/**
 * A secured JAX-RS resource.
 *
 * MIGRATION NOTE: The original `SecuredServlet` has been migrated to a JAX-RS resource,
 * which is the idiomatic approach in Quarkus.
 * - `@WebServlet` is replaced with `@Path`.
 * - The `doGet` method is replaced with a `@GET` annotated method.
 * - The injection of the WildFly-specific `org.wildfly.security.auth.server.SecurityIdentity`
 *   is replaced with the Quarkus-native `io.quarkus.security.identity.SecurityIdentity`.
 * - The `SecurityFactory` class is no longer needed and has been removed.
 *
 * @author <a href="mailto:darran.lofthouse@jboss.com">Darran Lofthouse</a>
 */
@Path("/secured")
@ApplicationScoped
public class SecuredResource {

    @Inject
    SecurityContext securityContext;

    @Inject
    SecurityIdentity identity;

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String get() {
        return String.format("SecuredResource - get()%n" +
                        "Identity as available from SecurityContext '%s'%n" +
                        "Identity as available from injection '%s'",
                securityContext.getCallerPrincipal().getName(),
                identity.getPrincipal().getName());
    }
}
```

`ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/TestAuthenticationMechanism.java`:

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
 * MIGRATION NOTE: This class is unchanged from the WildFly version. It implements
 * standard Jakarta EE Security APIs that are fully supported by the `quarkus-security`
 * extension. Quarkus automatically discovers and registers this mechanism because it is
 * an @ApplicationScoped CDI bean that implements the interface.
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

`ee-security-quarkus/src/main/resources/application.properties`:

```properties
# MIGRATION NOTE: This file replaces the WildFly-specific elytron CLI configuration.
# It defines the security policy for the application.
# We declare that the /secured path requires an authenticated user.
# Quarkus Security will then engage the custom TestAuthenticationMechanism
# to challenge the client for credentials.

quarkus.http.auth.permission.default.paths = /secured
quarkus.http.auth.permission.default.policy = authenticated
```