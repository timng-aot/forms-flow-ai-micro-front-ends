# External Integrations

**Analysis Date:** 2026-02-03

## APIs & External Services

**Authentication & Identity:**
- Keycloak - Identity provider and authorization server
  - SDK/Client: `keycloak-js` v26.1.2
  - Auth: Configured via `REACT_APP_KEYCLOAK_URL`, `REACT_APP_KEYCLOAK_URL_REALM`, `REACT_APP_KEYCLOAK_CLIENT`
  - Implementation: `forms-flow-service/src/keycloak/KeycloakService.ts`
  - Features: OAuth2/OpenID Connect, token refresh, SSO check, multi-tenant support via tenantId

**Workflow & BPM:**
- Camunda BPM Engine - Business process management and task execution
  - Base URL: `REACT_APP_BPM_URL`
  - Endpoints:
    - Process definitions: `/engine-rest-ext/v1/process-definition`
    - Task management: `/engine-rest-ext/v1/task/*` (detail, variables, submit-form, claim, unclaim, assignee)
    - Task filters: `/engine-rest-ext/v1/task-filters`
    - Activity instances: `/engine-rest-ext/v1/process-instance/<id>/activity-instances`
  - Real-time: Socket.IO at `/forms-flow-bpm-socket` for live task updates
  - Implementation: `forms-flow-review/src/api/services/bpmTaskServices.ts`

**Form Building & Submission:**
- Formio - Dynamic form builder and submission handler
  - SDK: @aot-technologies/formio-react v1.0.5 (custom AOT wrapper)
  - Used by: `forms-flow-components`, `forms-flow-review`, `forms-flow-submissions`
  - Features: Form rendering, validation, submission capture

**Forms Flow AI Backend:**
- REST API Server - Primary application backend
  - Base URLs:
    - Web services: `REACT_APP_WEB_BASE_URL` (forms-flow API)
    - Project API: `REACT_APP_API_PROJECT_URL` (form definitions)
    - GraphQL: `REACT_APP_GRAPHQL_API_URL` (default: http://localhost:5500/queries)
  - Endpoints:
    - Forms: `{WEB_BASE_URL}/form`, `{API_PROJECT_URL}/form`
    - Applications: `{WEB_BASE_URL}/application/<id>`, `{WEB_BASE_URL}/application/<id>/history`
    - Users: `{WEB_BASE_URL}/user`, `{WEB_BASE_URL}/user/default-filter`
    - Submissions filter: `{WEB_BASE_URL}/submissions-filter`
    - Filters: `{WEB_BASE_URL}/filter`, `{WEB_BASE_URL}/filter/<id>`, `{WEB_BASE_URL}/filter/filter-preference`
    - Roles: `{WEB_BASE_URL}/roles`, `{WEB_BASE_URL}/formio/roles`
    - Tasks: `{WEB_BASE_URL}/tasks/<task_id>/complete`
    - Processes: `{WEB_BASE_URL}/process/key/<process_key>`
    - Bundles: `{WEB_BASE_URL}/form/<mapper_id>/bundles/execute-rules`
  - Transport: HTTP via axios with Bearer token auth
  - Implementation: `forms-flow-service/src/request/requestService.ts`

**Document Service:**
- External Document Export Service - PDF generation and export
  - Base URL: `REACT_APP_DOCUMENT_SERVICE_URL`
  - Endpoints:
    - Export form to PDF: `{DOCUMENT_SERVICE_URL}/form/<form_id>/submission/<submission_id>/export/pdf`
  - Feature flag: `REACT_APP_EXPORT_PDF_ENABLED`
  - Implementation: `forms-flow-components/src/api/endpoints.ts`, `forms-flow-components/src/api/config.ts`

**Custom Submission Handler:**
- Custom Submission Service - Alternative submission processing
  - Base URL: `REACT_APP_CUSTOM_SUBMISSION_URL`
  - Endpoints:
    - Custom submission: `{CUSTOM_SUBMISSION_URL}/form/<form_id>/submission`
  - Enabled via: `REACT_APP_CUSTOM_SUBMISSION_ENABLED` flag
  - Used by: `forms-flow-review`, `forms-flow-submissions`

**Multi-Tenancy Admin:**
- MT Admin Service - Multi-tenant administration
  - Base URL: `REACT_APP_MT_ADMIN_BASE_URL`
  - Version: `REACT_APP_MT_ADMIN_BASE_URL_VERSION` (default: v1)
  - Endpoints:
    - Tenant data: `{MT_ADMIN_BASE_URL}/{version}/tenant`
  - Enabled via: `REACT_APP_IS_ENTERPRISE`, `REACT_APP_MULTI_TENANCY_ENABLED` flags

## Data Storage

**Databases:**
- Backend managed (not directly accessed from frontend)
- Data accessed via REST/GraphQL APIs through Forms Flow AI backend

**File Storage:**
- Document Service handles file storage for PDFs and exports
- Custom Submission Service may handle file uploads for alternative flows

**Caching:**
- TanStack React Query (forms-flow-submissions) - Client-side caching of server state
- Redux state store (forms-flow-review, forms-flow-submissions) - Client state caching
- Local storage via StorageService for:
  - AUTH_TOKEN - Keycloak JWT token
  - USER_ROLE - User roles from Keycloak
  - USER_DETAILS - User information from Keycloak
  - Filter preferences and user settings

## Authentication & Identity

**Auth Provider:**
- Keycloak (OAuth2/OpenID Connect)
  - Implementation: `forms-flow-service/src/keycloak/KeycloakService.ts`
  - Features:
    - Singleton instance pattern for OAuth client
    - Check-SSO mode for seamless authentication
    - PKCE flow (S256 method) for security
    - Automatic token refresh before expiration
    - Silent check-SSO with redirect URI: `/silent-check-sso.html`
    - Multi-tenant support (tenant ID prefixed to client ID if provided)
  - Token Management:
    - Token stored in local storage with key `AUTH_TOKEN`
    - Token refresh scheduled before expiration
    - Automatic retry on 401 with token refresh via RequestService
    - Token validity extracted from JWT `exp` and `iat` claims

**Authorization:**
- Role-based access control (RBAC) from Keycloak token claims
- User roles stored in local storage with key `USER_ROLE`
- Roles sourced from token's `roles`, `role`, or `client_roles` fields
- Role validation performed before authentication completion

## Monitoring & Observability

**Error Tracking:**
- Not detected - Application logs errors to browser console

**Logs:**
- Console logging for authentication, token refresh, and API errors
- Redux Logger (redux-logger) v3.0.6 for state change logging in review/submission modules
- Structured logging available via RequestService for HTTP calls
- No centralized error tracking service configured

## CI/CD & Deployment

**Hosting:**
- Static frontend hosting (SPA/micro-frontend modules)
- Modules deployed independently via Webpack bundling
- Single-SPA orchestration at application shell level

**CI Pipeline:**
- Not detected - Configuration files suggest local npm scripts available
- GitHub Actions workflows likely present (`.github/` directory exists)

**Build Scripts:**
- `npm run build` - Production build with webpack optimization
- `npm run build:webpack` - Webpack-specific build
- `npm run build:types` - TypeScript type declaration generation
- `npm run start` - Development server with hot reload
- `npm run lint` - ESLint code quality checks
- `npm run format` - Prettier code formatting
- `npm run test` - Jest test execution
- `npm run coverage` - Test coverage reporting

## Environment Configuration

**Required env vars:**
- `REACT_APP_KEYCLOAK_URL` - Keycloak server base URL
- `REACT_APP_KEYCLOAK_URL_REALM` - Keycloak realm name
- `REACT_APP_KEYCLOAK_CLIENT` - Keycloak client ID
- `REACT_APP_WEB_BASE_URL` - Forms Flow AI backend base URL
- `REACT_APP_API_SERVER_URL` - Forms Flow API server URL (fallback: http://127.0.0.1:3001)
- `REACT_APP_API_PROJECT_URL` - Project API URL
- `REACT_APP_BPM_URL` - Camunda BPM engine base URL

**Optional env vars:**
- `REACT_APP_KEYCLOAK_URL_HTTP_RELATIVE_PATH` - Keycloak auth path (default: /auth)
- `REACT_APP_WEB_BASE_CUSTOM_URL` - Custom web base URL override
- `REACT_APP_GRAPHQL_API_URL` - GraphQL endpoint (default: http://localhost:5500/queries)
- `REACT_APP_DOCUMENT_SERVICE_URL` - Document export service
- `REACT_APP_CUSTOM_SUBMISSION_URL` - Custom submission handler
- `REACT_APP_CUSTOM_SUBMISSION_ENABLED` - Enable custom submissions (boolean)
- `REACT_APP_EXPORT_PDF_ENABLED` - Enable PDF export feature (boolean)
- `REACT_APP_MT_ADMIN_BASE_URL` - Multi-tenant admin API
- `REACT_APP_MT_ADMIN_BASE_URL_VERSION` - Multi-tenant API version (default: v1)
- `REACT_APP_MULTI_TENANCY_ENABLED` - Enable multi-tenancy (boolean)
- `REACT_APP_IS_ENTERPRISE` - Enterprise edition flag (boolean)
- `REACT_APP_WEBSOCKET_ENCRYPT_KEY` - WebSocket encryption key
- `REACT_APP_PUBLIC_WORKFLOW_ENABLED` - Public workflow access (boolean)
- `REACT_APP_ENABLE_APPLICATIONS_MODULE` - Enable applications module (boolean)
- `REACT_APP_ENABLE_DASHBOARDS_MODULE` - Enable dashboards module (boolean)
- `REACT_APP_ENABLE_FORMS_MODULE` - Enable forms module (boolean)
- `REACT_APP_ENABLE_PROCESSES_MODULE` - Enable processes module (boolean)
- `REACT_APP_ENABLE_TASKS_MODULE` - Enable tasks module (boolean)
- `REACT_APP_ENABLE_INTEGRATION_PREMIUM` - Premium integrations flag (boolean)
- `REACT_APP_DRAFT_ENABLED` - Enable draft submissions (boolean)
- `REACT_APP_DRAFT_POLLING_RATE` - Draft auto-save polling interval (ms)
- `REACT_APP_APPLICATION_NAME` - Application display name
- `REACT_APP_LANGUAGE` - Default language
- `REACT_APP_USER_NAME_DISPLAY_CLAIM` - JWT claim for username display

**Secrets location:**
- Environment variables injected via container/deployment platform
- Keycloak secrets managed by Keycloak server
- JWT tokens stored in browser local storage (client-side)
- No secrets stored in source code

**Configuration injection:**
- `window._env_` object injected at runtime (not build-time)
- Supports dynamic configuration changes without rebuild
- Fallback to `process.env` for development mode
- Configuration accessed via declared global interface in type files

## Webhooks & Callbacks

**Incoming:**
- Not detected - Application is consumer-only

**Outgoing:**
- STOMP/WebSocket callbacks from Camunda BPM for real-time task updates
  - Protocol: Socket.IO
  - Endpoint: `{BPM_URL}/forms-flow-bpm-socket`
  - Purpose: Real-time task list updates in task review module
  - Implementation: `forms-flow-review` uses sockjs-client and @stomp/stompjs

**Custom Submission Callbacks:**
- Custom submission handler may implement webhooks for alternative workflows
- Configuration: `REACT_APP_CUSTOM_SUBMISSION_URL`

## Data Flow & Integration Patterns

**Request/Response:**
- All REST API calls use axios with Bearer token authentication
- Token injected from Keycloak session via RequestService
- Automatic token refresh on 401 with retry logic
- Error handling via promise rejection with axios AxiosError

**State Synchronization:**
- TanStack React Query manages server state synchronization (submissions module)
- Redux manages application state (review, submissions modules)
- Connected React Router keeps URL in sync with Redux state

**Real-time Updates:**
- WebSocket via Socket.IO for BPM task notifications
- STOMP protocol for message delivery
- Encryption key: `REACT_APP_WEBSOCKET_ENCRYPT_KEY`

---

*Integration audit: 2026-02-03*
