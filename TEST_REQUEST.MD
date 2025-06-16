# Migration von WildFly zu Quarkus: ee-security

## Projektstruktur nach der Migration

```
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
        │                       ├── SecurityFactory.java
        │                       └── TestAuthenticationMechanism.java
        └── resources
            ├── META-INF
            │   └── resources
            │       └── index.html
            └── application.properties
```

## Dateien im migrierten Projekt

### `pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>org.jboss.as.quickstarts</groupId>
    <artifactId>ee-security-quarkus</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    
    <name>Quarkus: ee-security</name>
    <description>This project demonstrates using EE security with Quarkus</description>
    
    <properties>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        
        <quarkus.platform.version>3.11.1</quarkus.platform.version>
        <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id>
        <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id>
        
        <compiler-plugin.version>3.13.0</compiler-plugin.version>
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
        <!-- Core Quarkus dependencies -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-arc</artifactId>
        </dependency>
        
        <!-- REST API -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive</artifactId>
        </dependency>
        
        <!-- Security -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-security</artifactId>
        </dependency>
        
        <!-- Jakarta Security API -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-security-jakarta</artifactId>
        </dependency>
        
        <!-- Jakarta EE Security -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-elytron-security</artifactId>
        </dependency>
    </dependencies>
    
    <build>
        <finalName>${project.artifactId}</finalName>
        <plugins>
            <plugin>
                <groupId>io.quarkus</groupId>
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
import jakarta.security.enterprise.credential.Credential;
import jakarta.security.enterprise.credential.UsernamePasswordCredential;
import jakarta.security.enterprise.identitystore.CredentialValidationResult;
import jakarta.security.enterprise.identitystore.IdentityStore;

/**
 * Identity store implementation that validates credentials against a predefined set of users.
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

### `src/main/java/org/jboss/as/quickstarts/ee_security/SecuredResource.java`

```java
package org.jboss.as.quickstarts.ee_security;

import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Inject;
import jakarta.security.enterprise.SecurityContext;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

import io.quarkus.security.identity.SecurityIdentity;

/**
 * A secured JAX-RS resource that replaces the original servlet.
 */
@Path("/secured")
@RequestScoped
public class SecuredResource {

    @Inject
    private SecurityContext securityContext;

    @Inject
    private SecurityIdentity securityIdentity;

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String getSecuredInfo() {
        StringBuilder response = new StringBuilder();
        response.append("SecuredResource - getSecuredInfo()\n");
        response.append(String.format("Identity as available from SecurityContext '%s'\n", 
                securityContext.getCallerPrincipal().getName()));
        response.append(String.format("Identity as available from injection '%s'", 
                securityIdentity.getPrincipal().getName()));
        
        return response.toString();
    }
}
```

### `src/main/java/org/jboss/as/quickstarts/ee_security/SecurityFactory.java`

```java
package org.jboss.as.quickstarts.ee_security;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.inject.Produces;

import io.quarkus.security.identity.SecurityIdentity;

/**
 * Factory for security-related objects.
 */
@ApplicationScoped
public class SecurityFactory {

    @Produces
    public SecurityIdentity getSecurityIdentity(SecurityIdentity securityIdentity) {
        return securityIdentity;
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
 * A custom HTTP authentication mechanism that uses headers for authentication.
 */
@ApplicationScoped
@Alternative
@Priority(1)
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
# General configuration
quarkus.application.name=ee-security-quarkus
quarkus.http.port=8080

# Security configuration
quarkus.security.jakarta.enabled=true

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
    <title>EE Security Quickstart</title>
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
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
        }
        .instructions {
            background-color: #f9f9f9;
            padding: 15px;
            border-left: 4px solid #4695EB;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>EE Security Quickstart</h1>
    
    <div class="instructions">
        <h2>How to test the application</h2>
        <p>To access the secured endpoint, send a request to <code>/secured</code> with the following headers:</p>
        <ul>
            <li><code>X-USERNAME: quickstartUser</code></li>
            <li><code>X-PASSWORD: quickstartPwd1!</code></li>
        </ul>
        <p>You can use curl to test it:</p>
        <pre>curl -H "X-USERNAME: quickstartUser" -H "X-PASSWORD: quickstartPwd1!" http://localhost:8080/secured</pre>
    </div>
    
    <p>This application demonstrates Jakarta EE Security with Quarkus.</p>
</body>
</html>
```