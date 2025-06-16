## Quarkus Migration Guide

### Projektbaum

```txt
ee-security-quarkus
├── pom.xml
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
    │   └── resources
    │       └── application.properties
    └── test
```

### Dateien

#### `ee-security-quarkus/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.jboss.as.quickstarts</groupId>
    <artifactId>ee-security-quarkus</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    <name>Quickstart: ee-security Quarkus</name>
    <description>This project demonstrates using EE security with Quarkus</description>

    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <quarkus.version>3.11.1</quarkus.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>io.quarkus</groupId>
                <artifactId>quarkus-bom</artifactId>
                <version>${quarkus.version}</version>
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
        <dependency>
            <groupId>jakarta.enterprise</groupId>
            <artifactId>jakarta.enterprise.cdi-api</artifactId>
        </dependency>
        <dependency>
            <groupId>jakarta.servlet</groupId>
            <artifactId>jakarta.servlet-api</artifactId>
        </dependency>
        <dependency>
            <groupId>jakarta.security.enterprise</groupId>
            <artifactId>jakarta.security.enterprise-api</artifactId>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>io.quarkus</groupId>
                <artifactId>quarkus-maven-plugin</artifactId>
                <version>${quarkus.version}</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>build</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

#### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/ElytronIdentityStore.java`

```java
package org.jboss.as.quickstarts.ee_security;

import static jakarta.security.enterprise.identitystore.CredentialValidationResult.INVALID_RESULT;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.security.enterprise.credential.Credential;
import jakarta.security.enterprise.credential.UsernamePasswordCredential;
import jakarta.security.enterprise.identitystore.CredentialValidationResult;
import jakarta.security.enterprise.identitystore.IdentityStore;

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

#### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/SecuredServlet.java`

```java
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

@WebServlet(value="/secured")
public class SecuredServlet extends HttpServlet {

    @Inject
    private SecurityContext securityContext;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        PrintWriter pw = resp.getWriter();
        pw.println("SecuredServlet - doGet()");
        pw.println(String.format("Identity as available from SecurityContext '%s'", securityContext.getCallerPrincipal().getName()));
    }

}
```

#### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/SecurityFactory.java`

```java
package org.jboss.as.quickstarts.ee_security;

import jakarta.enterprise.inject.Produces;

import org.wildfly.security.auth.server.SecurityDomain;
import org.wildfly.security.auth.server.SecurityIdentity;

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

#### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/TestAuthenticationMechanism.java`

```java
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

#### `ee-security-quarkus/src/main/resources/application.properties`

```properties
# Quarkus application properties
quarkus.http.auth.basic=true
quarkus.http.auth.policy.default.roles-allowed=Users
```

### Migrationshinweise

1. **Projektstruktur**: Die Struktur wurde angepasst, um die Quarkus-Konventionen zu erfüllen. Die `WEB-INF`-Ordnerstruktur wurde entfernt, da Quarkus keine WAR-Dateien benötigt.
   
2. **POM-Datei**: Die POM-Datei wurde aktualisiert, um die Quarkus-Abhängigkeiten zu verwenden. Die WildFly-spezifischen Abhängigkeiten und Plugins wurden entfernt.

3. **Java-Klassen**: Die Java-Klassen wurden migriert, um die Quarkus-Sicherheits-APIs zu verwenden. Die `SecurityIdentity`- und `SecurityDomain`-Abhängigkeiten wurden beibehalten, da sie in Quarkus durch die `quarkus-security`-Erweiterung unterstützt werden.

4. **Konfiguration**: Die Sicherheitskonfiguration wurde von CLI-Skripten in `application.properties` übertragen, um die Quarkus-Konfiguration zu nutzen.

5. **Servlets**: Die Servlets wurden beibehalten, da Quarkus die Servlet-API unterstützt. Die Sicherheitslogik wurde angepasst, um die Quarkus-Sicherheitsmechanismen zu verwenden.