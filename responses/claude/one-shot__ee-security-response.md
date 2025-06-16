# Migration von WildFly zu Quarkus: ee-security

## Projektstruktur

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
        │                       ├── SecurityFactory.java
        │                       └── TestAuthenticationMechanism.java
        └── resources
            ├── META-INF
            │   └── resources
            │       └── index.html
            └── application.properties
```

## Dateien

### `ee-security-quarkus/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.jboss.as.quickstarts</groupId>
    <artifactId>ee-security</artifactId>
    <version>1.0.0</version>
    <name>Quickstart: ee-security</name>
    <description>This project demonstrates using EE security</description>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id>
        <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id>
        <quarkus.platform.version>3.11.1</quarkus.platform.version>
        <maven.compiler.release>21</maven.compiler.release>
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
        <!-- RESTEasy Reactive -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-resteasy-reactive</artifactId>
        </dependency>
        
        <!-- Security -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-security</artifactId>
        </dependency>
        
        <!-- CDI -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-arc</artifactId>
        </dependency>
        
        <!-- Jakarta Security API -->
        <dependency>
            <groupId>jakarta.security.enterprise</groupId>
            <artifactId>jakarta.security.enterprise-api</artifactId>
        </dependency>
    </dependencies>

    <build>
        <finalName>${project.artifactId}</finalName>
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
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <release>${maven.compiler.release}</release>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/ElytronIdentityStore.java`

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

### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/SecuredResource.java`

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

import jakarta.inject.Inject;
import jakarta.security.enterprise.SecurityContext;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

import io.quarkus.security.identity.SecurityIdentity;

/**
 * @author <a href="mailto:darran.lofthouse@jboss.com">Darran Lofthouse</a>
 */
@Path("/secured")
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
                securityContext.getCallerPrincipal() != null ? 
                securityContext.getCallerPrincipal().getName() : "null"));
        response.append(String.format("Identity as available from injection '%s'", 
                securityIdentity != null ? 
                securityIdentity.getPrincipal().getName() : "null"));
        return response.toString();
    }
}
```

### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/SecurityFactory.java`

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
import jakarta.enterprise.inject.Produces;

import io.quarkus.security.identity.SecurityIdentity;

/**
 * @author <a href="mailto:darran.lofthouse@jboss.com">Darran Lofthouse</a>
 */
@ApplicationScoped
public class SecurityFactory {

    // In Quarkus, SecurityIdentity is automatically injectable
    // This producer is kept for compatibility but is not strictly necessary
    @Produces
    public SecurityIdentity getSecurityIdentity(SecurityIdentity securityIdentity) {
        return securityIdentity;
    }
}
```

### `ee-security-quarkus/src/main/java/org/jboss/as/quickstarts/ee_security/TestAuthenticationMechanism.java`

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

/**
 * A simple {@link HttpAuthenticationMechanism} for testing.
 *
 * @author <a href="mailto:darran.lofthouse@jboss.com">Darran Lofthouse</a>
 */
@ApplicationScoped
@Alternative
@Priority(Interceptor.Priority.APPLICATION)
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

### `ee-security-quarkus/src/main/resources/META-INF/resources/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>EE Security Example</title>
    <meta http-equiv="Refresh" content="0; URL=secured">
</head>
<body>
    <p>Redirecting to secured endpoint...</p>
</body>
</html>
```

### `ee-security-quarkus/src/main/resources/application.properties`

```properties
# Configure the application
quarkus.application.name=ee-security
quarkus.http.port=8080

# Security configuration
quarkus.security.auth.enabled=true

# Logging configuration
quarkus.log.level=INFO
quarkus.log.category."org.jboss.as.quickstarts".level=DEBUG
```