# Architecture

**Analysis Date:** 2026-02-03

## Pattern Overview

**Overall:** Micro-frontend architecture using single-spa for application composition and orchestration

**Key Characteristics:**
- Single-spa module federation at runtime (not webpack)
- Each module (admin, nav, review, submissions, etc.) is independently deployable
- Pub/Sub event system for inter-module communication
- Redux for state management in complex modules
- Centralized services module for shared business logic
- Keycloak-based authentication with token management
- Multitenancy support throughout the stack

## Layers

**Micro Frontend Modules (Application Layer):**
- Purpose: Self-contained, independently deployable applications
- Location: `/forms-flow-admin`, `/forms-flow-review`, `/forms-flow-submissions`, `/forms-flow-nav`, `/forms-flow-integration`
- Contains: React components, local state management (Redux in review/submissions), route handling, feature-specific logic
- Depends on: `@formsflow/service`, `@formsflow/components`, `@formsflow/theme`
- Used by: Root configuration in external repository (forms-flow-web-root-config)

**Shared Services Layer:**
- Purpose: Centralized business logic, API communication, authentication, storage
- Location: `/forms-flow-service/src`
- Contains: Keycloak authentication, storage abstraction, HTTP request management, router helpers, i18n setup
- Depends on: axios, keycloak-js, connected-react-router
- Used by: All micro-frontend modules

**Component Library (UI Layer):**
- Purpose: Reusable React components and UI patterns
- Location: `/forms-flow-components/src`
- Contains: Custom components, SVG assets, custom hooks, Storybook documentation
- Depends on: React, Bootstrap, Material-UI, Formio
- Used by: All micro-frontend modules

**Theme Layer (Styling):**
- Purpose: Centralized CSS variables and theming
- Location: `/forms-flow-theme/scss`
- Contains: SCSS variables, utility classes, theme configuration
- Depends on: Bootstrap, SCSS
- Used by: All micro-frontend modules

## Data Flow

**Initialization Flow:**

1. Root config loads single-spa applications and provides props containing `publish` and `subscribe` methods
2. Each micro-frontend bootstraps via single-spa lifecycle (bootstrap → mount → unmount)
3. Keycloak authentication is initialized in root or individual module
4. User roles and permissions are stored via StorageService
5. Redux store is configured per module (review, submissions) with async thunks for API calls

**Inter-Module Communication:**

1. Modules publish events via `props.publish("EVENT_KEY", payload)`
2. Other modules subscribe via `props.subscribe("EVENT_KEY", callback)`
3. Common events:
   - `FF_AUTH`: Auth instance propagation
   - `ES_ROUTE`: Route/navigation announcements
   - `ES_CHANGE_LANGUAGE`: Internationalization updates
   - `ES_TENANT`: Tenant data sharing
   - `FF_PUBLIC`: Public context announcement

**API Request Flow:**

1. Component dispatches Redux action (review/submissions) or calls service directly
2. Action creator calls API service method
3. Service method uses `RequestService.makeRequest()` (axios wrapper)
4. RequestService interceptor:
   - Attaches JWT token from Keycloak to Authorization header
   - On 401 response, refreshes token via KeycloakService.updateToken()
   - Retries original request with new token
5. Response transformed and dispatched to Redux or returned to component

**State Management:**

- **Global UI State (Redux):** Task list, filters, form data in review/submissions modules
- **Auth State:** Keycloak instance managed via single-spa props, user roles in StorageService
- **Tenant State:** Stored in localStorage and localStorage, propagated via Redux in review/submissions
- **Transient State:** Form values, modal visibility, pagination in component state

## Key Abstractions

**KeycloakService:**
- Purpose: Manage Keycloak authentication lifecycle, token refresh, user info
- Examples: `forms-flow-service/src/keycloak/KeycloakService.ts`
- Pattern: Singleton with getInstance() factory, event-driven token refresh
- Interaction: Called from modules via `props.getKcInstance()` or imported from @formsflow/service

**StorageService:**
- Purpose: Unified storage API (localStorage, sessionStorage) with key constants
- Examples: `forms-flow-service/src/storage/storageService.ts`
- Pattern: Static methods for save/get/delete with namespaced keys (e.g., `StorageService.User.USER_ROLE`)
- Usage: Roles, tenant data, language preferences, cache

**RequestService:**
- Purpose: HTTP client with automatic token handling and retry logic
- Examples: `forms-flow-service/src/request/requestService.ts`
- Pattern: Axios wrapper with response/error interceptors
- Features: JWT attachment, 401 retry with refresh, error propagation

**Router Helpers:**
- Purpose: Centralized navigation paths and URL construction
- Examples: `forms-flow-service/src/routerServices/routerHelper.ts`
- Pattern: Functions like `navigateToTaskListing()`, `navigateToSubmissionDetail()` return routes
- Usage: Decouples navigation logic from component implementation

**Redux Actions & Reducers (review/submissions):**
- Purpose: Manage complex application state (task lists, filters, form data)
- Examples:
  - `forms-flow-review/src/actions/taskActions.ts`
  - `forms-flow-review/src/reducers/taskReducer.ts`
  - `forms-flow-submissions/src/reducers/analizeSubmissionReducer.ts`
- Pattern: Redux Toolkit with async thunks calling API services
- State: Task details, pagination, filters, assignments

**API Service Modules:**
- Purpose: Encapsulate specific domain API calls
- Examples:
  - `forms-flow-review/src/api/services/bpmTaskServices.ts`
  - `forms-flow-submissions/src/api/services/submissionServices.ts`
- Pattern: Exported functions returning promises (axios calls wrapped in RequestService)
- Constants: API endpoints defined in `src/api/endpoints.ts` per module

## Entry Points

**forms-flow-admin:**
- Location: `forms-flow-admin/src/formsflow-admin.tsx`
- Triggers: Single-spa bootstrap/mount lifecycle
- Responsibilities: Register single-spa lifecycle hooks, export bootstrap/mount/unmount
- Mount Point: `forms-flow-admin/src/root.component.tsx` wraps admin logic in layout

**forms-flow-review:**
- Location: `forms-flow-review/src/formsflow-review.tsx`
- Triggers: Single-spa bootstrap/mount lifecycle
- Responsibilities: Register single-spa lifecycle, provide Redux Provider setup
- Mount Point: `forms-flow-review/src/root.component.tsx` with Redux store and connected-react-router

**forms-flow-submissions:**
- Location: `forms-flow-submissions/src/formsflow-submissions.tsx`
- Triggers: Single-spa bootstrap/mount lifecycle
- Responsibilities: Register single-spa lifecycle
- Mount Point: `forms-flow-submissions/src/root.component.tsx` with Redux/React Query providers

**forms-flow-nav:**
- Location: `forms-flow-nav/src/formsflow-nav.js`
- Triggers: Single-spa bootstrap/mount lifecycle
- Responsibilities: Navigation bar rendering and routing
- Mount Point: `forms-flow-nav/src/Navbar.jsx` with multi-language support

**forms-flow-components:**
- Location: `forms-flow-components/src/formsflow-components.ts`
- Triggers: Module import (not a micro-frontend, a library)
- Responsibilities: Export all component/hook definitions
- No lifecycle, consumed as npm package

**forms-flow-service:**
- Location: `forms-flow-service/src/formsflow-services.ts`
- Triggers: Module import (not a micro-frontend, a library)
- Responsibilities: Export all services and router helpers
- No lifecycle, consumed as npm package

## Error Handling

**Strategy:** Layered error handling with fallbacks

**Patterns:**

- **Auth Errors (401):** RequestService interceptor triggers token refresh; if refresh fails, error propagates to component
- **API Errors:** Caught in Redux thunks with error state dispatch; components render error UI based on state
- **Component Errors:** single-spa errorBoundary hooks in `formsflow-*.tsx` files return null (silently fail)
- **Validation Errors:** Form validation in components before submission; API response validation in reducers
- **Storage Errors:** Try-catch blocks around JSON.parse in StorageService usage (e.g., tenant data parsing in review index.tsx)

## Cross-Cutting Concerns

**Logging:** console.* calls throughout; no centralized logging infrastructure

**Validation:**
- Form validation via Formio (custom form renderer)
- API response structure checked in Redux thunks
- User role-based access control checked before rendering modules

**Authentication:**
- Keycloak OIDC via keycloak-js
- Token stored by Keycloak, refreshed automatically by RequestService
- Roles stored in StorageService after login
- Tenant context includes role scope

**Internationalization:**
- i18next with browser language detector
- resourceBundles directory per module contains language JSON files
- Switched via `i18n.changeLanguage()` and persisted to localStorage
- Subscribed to ES_CHANGE_LANGUAGE event for cross-module sync

**Styling:**
- CSS variables from `/forms-flow-theme/scss` injected globally
- SCSS modules in component directories (e.g., `index.scss` co-located)
- Bootstrap 5 for layout/components
- Material-UI for data grid/tables in submissions

---

*Architecture analysis: 2026-02-03*
