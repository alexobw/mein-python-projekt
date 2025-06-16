# Quarkus Migration

## Projektbaum

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

## Dateien

### `ee-security-quarkus/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://www.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>org.jboss.quickstarts</groupId>
    <artifactId>ee-security-quarkus</artifactId>
    <version>1.0.0</version>
    <properties>
        <quarkus.version>3.11.1</quarkus.version>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
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
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-elytron-security</artifactId>
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

### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/ElytronIdentityStore.java`

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

### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/SecuredServlet.java`

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

### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/SecurityFactory.java`

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

### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/TestAuthenticationMechanism.java`

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

### `ee-security-quarkus/src/main/resources/application.properties`

```properties
# Quarkus application properties
quarkus.http.port=8080
quarkus.http.cors=true
quarkus.security.users.embedded.enabled=true
quarkus.security.users.embedded.plain-text=true
quarkus.security.users.embedded.users.quickstartUser=quickstartPwd1!
quarkus.security.users.embedded.roles.quickstartUser=Users
```

Diese Migration umfasst die Umstellung der Jakarta EE-Sicherheitskonfigurationen und -Abhängigkeiten auf Quarkus-Äquivalente, wobei die Sicherheitslogik beibehalten wird. Die Elytron-spezifischen Konfigurationen wurden durch Quarkus-Sicherheitskonfigurationen ersetzt, die in der `application.properties` definiert sind.