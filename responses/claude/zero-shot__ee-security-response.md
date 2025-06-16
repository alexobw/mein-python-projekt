# Quarkus-Migration des ee-security Projekts

## Projektstruktur

```
ee-security-quarkus
├── mvnw
├── mvnw.cmd
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
        │                       ├── SecurityFactory.java
        │                       └── TestAuthenticationMechanism.java
        └── resources
            ├── application.properties
            └── META-INF
                └── resources
                    └── index.html
```

## Dateien

### `pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.jboss.as.quickstarts</groupId>
    <artifactId>ee-security-quarkus</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <name>Quickstart: ee-security (Quarkus)</name>
    <description>This project demonstrates using EE security with Quarkus</description>

    <licenses>
        <license>
            <name>Apache License, Version 2.0</name>
            <url>http://www.apache.org/licenses/LICENSE-2.0.html</url>
            <distribution>repo</distribution>
        </license>
    </licenses>

    <properties>
        <compiler-plugin.version>3.11.0</compiler-plugin.version>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id>
        <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id>
        <quarkus.platform.version>3.11.1</quarkus.platform.version>
        <skipITs>true</skipITs>
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
        <!-- Core dependencies -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-arc</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive</artifactId>
        </dependency>
        
        <!-- Security dependencies -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-security</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-elytron-security</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-security-jpa</artifactId>
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
    <profiles>
        <profile>
            <id>native</id>
            <activation>
                <property>
                    <name>native</name>
                </property>
            </activation>
            <properties>
                <skipITs>false</skipITs>
                <quarkus.package.type>native</quarkus.package.type>
            </properties>
        </profile>
    </profiles>
</project>
```

### `src/main/java/org/jboss/as/quickstarts/ee_security/ElytronIdentityStore.java`

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

import io.quarkus.security.identity.SecurityIdentity;

/**
 * Identity store implementation for Quarkus
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
    SecurityIdentity securityIdentity;

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

### `src/main/java/org/jboss/as/quickstarts/ee_security/SecuredResource.java`

```java
package org.jboss.as.quickstarts.ee_security;

import jakarta.annotation.security.RolesAllowed;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

import io.quarkus.security.identity.SecurityIdentity;

/**
 * A secured JAX-RS resource
 */
@Path("/secured")
public class SecuredResource {

    @Inject
    SecurityIdentity securityIdentity;

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    @RolesAllowed("Users")
    public String secured() {
        return "SecuredResource - doGet()\n" +
               String.format("Identity as available from SecurityIdentity '%s'", securityIdentity.getPrincipal().getName());
    }
}
```

### `src/main/java/org/jboss/as/quickstarts/ee_security/SecurityFactory.java`

```java
package org.jboss.as.quickstarts.ee_security;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.inject.Produces;

import io.quarkus.security.identity.SecurityIdentity;
import io.quarkus.security.runtime.SecurityIdentityAssociation;
import jakarta.inject.Inject;

/**
 * Factory for security-related objects in Quarkus
 */
@ApplicationScoped
public class SecurityFactory {

    @Inject
    SecurityIdentityAssociation securityIdentityAssociation;

    @Produces
    public SecurityIdentity getSecurityIdentity() {
        return securityIdentityAssociation.getIdentity();
    }
}
```

### `src/main/java/org/jboss/as/quickstarts/ee_security/TestAuthenticationMechanism.java`

```java
package org.jboss.as.quickstarts.ee_security;

import jakarta.annotation.Priority;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.inject.Alternative;
import jakarta.inject.Inject;
import jakarta.interceptor.Interceptor;
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

import io.quarkus.security.identity.IdentityProviderManager;
import io.quarkus.security.identity.SecurityIdentity;
import io.quarkus.security.identity.request.AuthenticationRequest;
import io.quarkus.vertx.http.runtime.security.HttpAuthenticationMechanismFactory;
import io.quarkus.vertx.http.runtime.security.HttpSecurityPolicy;
import io.vertx.ext.web.RoutingContext;

/**
 * A custom authentication mechanism for Quarkus
 */
@Alternative
@Priority(Interceptor.Priority.APPLICATION)
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

### `src/main/resources/application.properties`

```properties
# Configure the application
quarkus.application.name=ee-security-quarkus
quarkus.http.port=8080

# Security configuration
quarkus.security.users.embedded.enabled=true
quarkus.security.users.embedded.plain-text=true
quarkus.security.users.embedded.users.quickstartUser=quickstartPwd1!
quarkus.security.users.embedded.roles.quickstartUser=Users

# Enable basic auth for testing
quarkus.http.auth.basic=true

# Logging configuration
quarkus.log.level=INFO
quarkus.log.category."org.jboss.as.quickstarts".level=DEBUG
```

### `src/main/resources/META-INF/resources/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>EE Security Quickstart - Quarkus</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 2em;
            line-height: 1.5;
        }
        h1 {
            color: #4695EB;
        }
        code {
            background-color: #f0f0f0;
            padding: 2px 4px;
            border-radius: 3px;
        }
        pre {
            background-color: #f0f0f0;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>EE Security Quickstart</h1>
    <p>This application demonstrates Jakarta EE Security with Quarkus.</p>
    
    <h2>Testing the application</h2>
    <p>You can access the secured endpoint at <a href="/secured">/secured</a> using the following credentials:</p>
    <ul>
        <li>Username: <code>quickstartUser</code></li>
        <li>Password: <code>quickstartPwd1!</code></li>
    </ul>
    
    <h2>Using custom headers</h2>
    <p>You can also use custom headers to authenticate:</p>
    <pre>
curl -v -H "X-USERNAME: quickstartUser" -H "X-PASSWORD: quickstartPwd1!" http://localhost:8080/secured
    </pre>
</body>
</html>
```

## Migrationserklärung

Die Migration von WildFly zu Quarkus für das ee-security Projekt umfasste folgende Hauptänderungen:

1. **Projektstruktur**: Umstellung auf Quarkus-Projektstruktur mit entsprechenden Maven-Abhängigkeiten.

2. **Sicherheitskomponenten**:
   - Ersetzung von WildFly Elytron durch Quarkus Security-Extensions
   - Anpassung der Authentifizierungsmechanismen an Quarkus-Sicherheitsmodell
   - Konfiguration der Benutzerauthentifizierung in `application.properties`

3. **Servlet zu JAX-RS**:
   - Umwandlung des `SecuredServlet` in eine JAX-RS-Ressource (`SecuredResource`)
   - Verwendung von Quarkus RESTEasy Reactive

4. **Sicherheitsidentität**:
   - Anpassung der `SecurityFactory` zur Verwendung von Quarkus `SecurityIdentity`
   - Integration mit Quarkus-Sicherheitsinfrastruktur

5. **Konfiguration**:
   - Entfernung der WildFly-spezifischen CLI-Skripte
   - Hinzufügung von Quarkus-Konfiguration in `application.properties`

Die Anwendung behält die gleiche Funktionalität bei, nutzt aber nun die Quarkus-Infrastruktur für Sicherheit und Bereitstellung.