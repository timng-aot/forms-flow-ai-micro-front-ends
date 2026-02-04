# Technology Stack

**Analysis Date:** 2026-02-03

## Languages

**Primary:**
- TypeScript 4.3.5 - 5.8.3 (varies by module) - Core language for most microservices
- JavaScript (ES6+) - Legacy modules and configuration files
- JSX/TSX - React component definitions

**Secondary:**
- SASS/SCSS - Styling across modules
- HTML - Template markup (Storybook, public assets)

## Runtime

**Environment:**
- Node.js (version not explicitly specified, but inferred from npm/webpack configuration)

**Package Manager:**
- npm (primary)
- Lockfile: `package-lock.json` present per module

## Frameworks

**Core:**
- React 17.0.2 - UI component library used across all modules
- Single-SPA 5.9.3 - Micro-frontend framework orchestrating module federation
- single-spa-react 4.3.1 - React-specific Single-SPA integration

**Styling & UI:**
- React Bootstrap 2.10.6 - Bootstrap-based component library
- Material-UI (MUI) 7.3.2 - Advanced data grid and material design components (`forms-flow-components`)
- MUI X-Data-Grid 8.12.1 - Data table component (`forms-flow-components`)
- Bootstrap 5.3.x - CSS framework foundation

**State Management:**
- Redux Toolkit 2.6.0 - 2.8.2 - State management for review/submissions modules
- React Redux 7.2.8 - 7.2.9 - Redux bindings
- Connected React Router 6.9.2 - 6.9.3 - Redux integration with react-router

**Data & API:**
- Axios 1.3.0 - 1.8.4 - HTTP client for REST API calls
- TanStack React Query 4.29.15 - Server state management (`forms-flow-submissions`)
- Keycloak-js 26.1.2 - OAuth2/OpenID Connect authentication client

**Form Building:**
- @aot-technologies/formio-react 1.0.5 - Custom Formio React wrapper for form rendering (`forms-flow-components`, `forms-flow-review`, `forms-flow-submissions`)
- BPMN-js 18.6.2 - BPMN diagram viewer and editor (`forms-flow-components`)

**Routing:**
- React Router DOM 5.1.2 - Client-side routing

**Utilities:**
- moment.js 2.29.4 - Date/time utilities (`forms-flow-service`)
- i18next 21.6.16 - 25.2.1 - Internationalization framework
- i18next-browser-languagedetector 7.0.1 - 8.0.4 - Language detection
- react-i18next 11.15.3 - 12.3.1 - React i18n integration
- react-toastify 9.1.1 - Toast notifications
- sortablejs 1.15.6 - Drag-and-drop functionality
- react-js-pagination 3.0.3 - Pagination component
- react-loading-skeleton 3.5.0 - Loading skeleton UI

**WebSocket & Real-time:**
- @stomp/stompjs 7.0.1 - STOMP WebSocket protocol (`forms-flow-review`)
- sockjs-client 1.6.1 - WebSocket fallback (`forms-flow-review`)

**Utilities:**
- lodash 4.17.21 - Utility library (`forms-flow-review`)
- crypto-js 4.2.0 - Cryptographic utilities (`forms-flow-review`)
- history 4.7.2 - 4.10.1 - History management
- redux-logger 3.0.6 - Redux logging middleware
- react-select 5.8.0 - Select component (`forms-flow-admin`)
- multiselect-react-dropdown 2.0.25 - Multiselect dropdown (`forms-flow-components`)

**Testing:**
- Jest 27.0.6 - Test runner and framework
- @testing-library/react 12.0.0 - React component testing utilities
- @testing-library/jest-dom 5.14.1 - DOM matchers for Jest
- @testing-library/user-event 14.6.1 - User interaction simulation (`forms-flow-components`)

**Documentation & Component Development:**
- Storybook 7.6.20 - Component documentation and development (`forms-flow-components`)
- @storybook/* addons (actions, controls, docs, essentials, interactions, viewport)

## Key Dependencies

**Critical:**
- keycloak-js 26.1.2 - Authentication and authorization via Keycloak server. Essential for secure access control and token management.
- @aot-technologies/formio-react 1.0.5 - Custom form builder integration. Used for dynamic form rendering and submission handling.
- single-spa 5.9.3 - Enables micro-frontend architecture. Core to module orchestration and independent deployments.
- axios 1.3.0+ - HTTP communication with backend APIs and external services.
- @reduxjs/toolkit 2.6.0+ - State container for complex application state in review/submission modules.

**Infrastructure:**
- bpmn-js 18.6.2 - Workflow diagram visualization and interaction
- @tanstack/react-query 4.29.15 - Server state synchronization and caching
- @mui/material - Advanced component library for data-heavy interfaces
- react-bootstrap - Consistent Bootstrap-based component system

## Configuration

**Environment:**
- Environment variables injected via `window._env_` object at runtime
- Configuration files define endpoint mappings and feature flags

**Key Environment Variables:**
- `REACT_APP_KEYCLOAK_URL` - Keycloak server URL
- `REACT_APP_KEYCLOAK_URL_REALM` - Keycloak realm
- `REACT_APP_KEYCLOAK_CLIENT` - Keycloak client ID
- `REACT_APP_WEB_BASE_URL` - Backend API base URL
- `REACT_APP_API_SERVER_URL` - Forms Flow AI API server
- `REACT_APP_API_PROJECT_URL` - Project API endpoint
- `REACT_APP_BPM_URL` - Camunda BPM engine URL
- `REACT_APP_GRAPHQL_API_URL` - GraphQL endpoint
- `REACT_APP_DOCUMENT_SERVICE_URL` - Document export service
- `REACT_APP_CUSTOM_SUBMISSION_URL` - Custom submission handler
- `REACT_APP_WEBSOCKET_ENCRYPT_KEY` - WebSocket encryption key
- `REACT_APP_MULTI_TENANCY_ENABLED` - Multi-tenant mode flag
- `REACT_APP_IS_ENTERPRISE` - Enterprise edition flag

**Build:**
- Babel configuration in `babel.config.json` across all modules
- TypeScript configuration in `tsconfig.json` for TypeScript modules
- Webpack configuration for bundling and development server
- Jest configuration for test running

## Build & Development Tools

**Bundling & Dev Server:**
- Webpack 5.75.0 - Module bundler
- Webpack CLI 4.8.0 - Webpack command-line interface
- Webpack Config Single-SPA 4.0.0 - Single-SPA specific webpack configuration
- Webpack Dev Server 4.0.0 - Development server with hot reload

**Code Quality:**
- ESLint 7.32.0 - JavaScript/TypeScript linting
- eslint-config-prettier 8.3.0 - Disables ESLint rules conflicting with Prettier
- eslint-config-react-important-stuff 3.0.0 - React-specific ESLint rules
- eslint-config-ts-react-important-stuff 3.0.0 - TypeScript + React ESLint rules
- eslint-plugin-prettier 3.4.1 - Prettier integration with ESLint
- eslint-plugin-storybook 0.6.15 - Storybook-specific linting rules (`forms-flow-components`)
- Prettier 2.3.2 - Code formatter
- pretty-quick 3.1.1 - Fast Prettier integration with git hooks

**Babel:**
- @babel/core 7.15.0 - JavaScript transpiler
- @babel/preset-env 7.15.0 - ES2015+ transpilation
- @babel/preset-react 7.14.5 - JSX transpilation
- @babel/preset-typescript 7.15.0 - TypeScript transpilation
- @babel/plugin-transform-runtime 7.15.0 - Runtime helpers optimization

**Other:**
- concurrently 6.2.1 - Run multiple npm scripts in parallel
- cross-env 7.0.3 - Cross-platform environment variable setting
- identity-obj-proxy 3.0.0 - Mock CSS modules in tests

## Platform Requirements

**Development:**
- Node.js (version not explicitly pinned, recommend 16+)
- npm or compatible package manager
- Modern browser with ES2015+ support

**Production:**
- Static hosting or CDN-based deployment for frontend modules
- Backend services:
  - Keycloak server for authentication
  - Forms Flow AI API backend
  - Camunda BPM engine for workflow
  - Document service for PDF export
  - WebSocket server for real-time updates

---

*Stack analysis: 2026-02-03*
